import numpy as np
import pickle as pickle
import hoomd
import hoomd.md
import hoomd.deprecated
from hoomd import _hoomd
from hoomd import deprecated
import os
import sys
from velocity import init_velocity
from bond_angle import load_bonded_coeffs
from pair_table import set_pair_potentials
from units import get_units
import math

N = 2200	# number of lipids
n_leaflets = 6 # number of leaflets

units = get_units()
hoomd.context.initialize()

start_file = 'start.hoomdxml'
system = hoomd.deprecated.init.read_xml(filename=start_file, wrap_coordinates=True)
#start_file = 'restart.gsd'
#system = hoomd.init.read_gsd(filename=start_file)

nl = hoomd.md.nlist.cell()
table = hoomd.md.pair.table(width=121, nlist = nl)
nl.reset_exclusions(exclusions = ['1-2', '1-3', 'bond', 'angle'])
all = hoomd.group.all()
ff_dir = '/users/cf2067/forcefields/cg'
set_pair_potentials(table, ff_dir)
bond_pot, angle_pot = hoomd.md.bond.harmonic(), hoomd.md.angle.harmonic()
bond_pot, angle_pot = load_bonded_coeffs(system, bond_pot, angle_pot,
    '/users/cf2067/forcefields/cg/cg-bond-coeffs_stiff-tails-v3.p',
    units['D'], units['E'])

# output files
thermo_log = hoomd.analyze.log(filename='thermo.txt',
        quantities=['temperature', 'pressure', 'volume', 'potential_energy',
              'lx', 'ly', 'lz'],
        period=1e3, header_prefix='#', overwrite=False)
all_dcd = hoomd.dump.dcd(filename="traj.dcd", period=5e4, overwrite=False,
        unwrap_full=True)
gsd_restart = hoomd.dump.gsd(filename='restart.gsd', group=all, truncate=True, period=10000, phase=0)

# run stuff
hoomd.md.integrate.mode_standard(dt=10.0/units['t'])
zeroer = hoomd.md.update.zero_momentum(period=1e4)
current = 0

# short nve run with limit to get rid of overlaps - 105 K
steps = 1e3
init_velocity(group=all, T=105.0/units['T'])
nve_int = hoomd.md.integrate.nve(group=all, limit=0.001)
hoomd.run_upto(current+steps, limit_multiple=1e3)
nve_int.disable()
current = current + steps

# short nve run with limit to get rid of overlaps - 305 K
steps = 1e3
init_velocity(group=all, T=305.0/units['T'])
nve_int = hoomd.md.integrate.nve(group=all, limit=0.01)
hoomd.run_upto(current+steps, limit_multiple=1e3)
nve_int.disable()
current = current + steps

# short npt volume equilibration
steps = 1e6
npt_int = hoomd.md.integrate.npt(group=all, kT=305/units['T'], tau=1000/units['t'],
        P=1.0/units['P'], tauP=10000/units['t'], couple='xyz')
hoomd.run_upto(current+steps, limit_multiple=1e3)
npt_int.disable()
current = current + steps

# nvt run with box resizing to accelerate self-assembly
tr = 20e6
steps = 3*tr
T_high = 305 / units['T']
T_points = [(0, T_high), (2*tr, T_high), (3*tr, 305/units['T'])]
T_ramp = hoomd.variant.linear_interp(points=T_points, zero=current)
L0 = [system.box.Lx, system.box.Ly, system.box.Lz]
vol0 = np.prod(L0)
l_apl = np.sqrt((N*34)/n_leaflets)/6	#expected Lx: 34 = apl, 2 = #layers, 6 = unit corr.
xpts = [(0, L0[0]), (tr, L0[0]*np.sqrt(2.0)), (2*tr, l_apl)]
ypts = [(0, L0[1])]
zpts = [(0, L0[2])]
for a, b in xpts[1:]:
    ypts.append((a, b))
    zpts.append((a, vol0/b**2))
Lx, Ly, Lz = [hoomd.variant.linear_interp(points=x, zero=current) for x in (xpts, ypts, zpts)]
resizer = hoomd.update.box_resize(Lx=Lx, Ly=Ly, Lz=Lz, period=1000)
nvt_int = hoomd.md.integrate.nvt(group=all, kT=T_ramp, tau=1000/units['t'])
hoomd.run_upto(current+steps, limit_multiple=1e3)
nvt_int.disable()
resizer.disable()
current = current + steps

# npt warm
steps = 30e6
tr = 5e6
T_high = 450 / units['T']
T_points = [(0, 305.0/units['T']), (2*tr, T_high), (3*tr, 305.0/units['T']), (4*tr, 305/units['T'])]
T_ramp = hoomd.variant.linear_interp(points=T_points, zero=current)
npt_int = hoomd.md.integrate.npt(group=all, kT=T_ramp, tau=1000/units['t'],
        P=1.0/units['P'], tauP=10000/units['t'], couple='xy')
hoomd.run_upto(current+steps, limit_multiple=1e3)
current = current + steps
npt_int.disable()

# relax
steps = 10e6
npt_int = hoomd.md.integrate.npt(group=all, kT=305/units['T'], tau=1000/           units['t'],P=1.0/units['P'], tauP=10000/units['t'], couple='xy')
hoomd.run_upto(current+steps, limit_multiple=1e3)
current = current + steps
npt_int.disable()

# Final production run 200ns for 200 frames
steps = 20e6

prod_dcd = hoomd.dump.dcd(filename='prod_short.dcd', period=1e5, overwrite=False,
        unwrap_full=True)

npt_int = hoomd.md.integrate.npt(group=all, kT=305/units['T'], tau=1000/units['t'],P=1.0/units['P'], tauP=10000/units['t'], couple='xy')
hoomd.run_upto(current+steps, limit_multiple=1e3)
current = current + steps
npt_int.disable()

# post-run
output_xml = hoomd.deprecated.dump.xml(group=all)
output_xml.set_params(all=True)
output_xml.write(filename="final.hoomdxml")
