from __future__ import division
import numpy as np
import os
import mbuild as mb
from lipids.cg_molecules.ffac16 import FFAC16 as FFA16
from lipids.cg_molecules.ffac18 import FFAC18 as FFA18
from lipids.cg_molecules.ffac20 import FFAC20 as FFA20
from lipids.cg_molecules.ffac22 import FFAC22 as FFA22
from lipids.cg_molecules.ffac24 import FFAC24 as FFA24

from lipids.cg_molecules.cer3_24 import Cer3_24 as Cer3 #NP
from lipids.cg_molecules.cer6_24 import Cer6_24 as Cer6 #AP
from lipids.cg_molecules.cer2_24 import Cer2_24 as Cer2 #NS
from lipids.cg_molecules.cer3_16 import Cer3_16 as Cer3_16 #NP
from lipids.cg_molecules.cer5_24 import Cer5_24 as Cer5 #AS

from lipids.cg_molecules.chol import Chol
from lipids.cg_molecules.water import Water
from mbuild.formats.hoomdxml import write_hoomdxml
import xml.etree.ElementTree as ET
import copy as cp


def build_system(n_lipids, n_water, lipids, ppl, apl, ff_file,
        n_leaflets=2, water_density=0.8,
        lipid_density=0.7, overlap=0.001, seed=12345, sys_num=0):
    """Build a mixed lipid system

    Args
    ----
    n_lipids : int
        Total number of lipids to include
    n_water : int
        Total number of water beads to include
    parts_cer : int
        Relative fraction of lipids that are CER
    parts_chol : int
        Relative fraction of lipids that are CHOL
    parts_ffa : int
        Relative fraction of lipids that are FFA
    ff_file : str, path
        Path to Foyer xml force field file
    n_leaflets : int
        Number of leaflets, determines the APL (2 for bilayer, 4 for stacked bilayer)
    apl_cer : float
        Weight APL by this much * fraction of CER, in angstrom^2
    apl_chol : float
        Weight APL by this much * fraction of CHOL, in angstrom^2
    apl_ffa : float
        Weight APL by this much * fraction of FFA, in angstrom^2
    water_density : float
        Density at which to add water to outside of lipids, in g/mL
    lipid_density : float
        Density at which to add lipids, in g/mL
    overlap : float
        Overlap tolerance for packing molecules
    """
    # first figure out how much of everything to add
    total_parts = sum(ppl)
    n_each_lipid = [round(n_lipids * parts / total_parts) for parts in ppl]
    lipidlist = list(zip(lipids, n_each_lipid))
    for index, item in reversed(list(enumerate(list(lipidlist)))):
        if item[1] == 0:
            lipidlist.pop(index)
    lipidlist += [(Water(), n_water)]
    # make the list of molecules to add
    molecules = [x[0] for x in lipidlist[:-1]]
    molecules.append(lipidlist[-1][0])
    molecules.append(lipidlist[-1][0])
    n_each_lipid = [x[1] for x in lipidlist[:-1]]
    n_each_lipid.append(round(lipidlist[-1][1]/2))
    n_each_lipid.append(round(lipidlist[-1][1]/2))
    # now figure out the box sizes, first with the lipid box...
    lipid_density /= 0.55409730   # into my CG density unit
    lipid_mass = np.sum(np.array([x[0].mass*x[1] for x in lipidlist[:-1]]))  # M_u
    target_vol = lipid_mass / lipid_density  # in D_u^3
    apl = np.sum(np.array(apl) * np.array(ppl) / sum(ppl)) / (6.0**2)
    Lx = (apl * sum([x[1] for x in lipidlist[:-1]]) / n_leaflets)**0.5  # D_u
    Lz = target_vol / Lx**2  # D_u
    print('Lx = {0}, Lz = {1}'.format(Lx, Lz))
    water_density /= 0.55409730  # rho_u
    water_mass = lipidlist[-1][0].mass * lipidlist[-1][1]  # M_u
    top_water_vol = bot_water_vol = water_mass / 2 / water_density  # D_u^3
    water_height = top_water_vol / Lx**2  # D_u
    Lx /= 10  # for mBuild
    Lz /= 10  # for mBuild
    water_height /= 10  # for mBuild
    lipid_box = mb.Box(mins=[-Lx/2, -Lx/2, -Lz/2], maxs=[Lx/2, Lx/2, Lz/2])  # D_u
    boxes = [lipid_box for x in lipidlist[:-1]]  # D_u
    # ...and now for the water boxes
    top_water_box = mb.Box(mins=[-Lx/2, -Lx/2, Lz/2],
            maxs=[Lx/2, Lx/2, Lz/2+water_height])
    bot_water_box = mb.Box(mins=[-Lx/2, -Lx/2, -Lz/2-water_height],
            maxs=[Lx/2, Lx/2, -Lz/2])
    boxes.append(top_water_box)
    boxes.append(bot_water_box)
    system = mb.fill_region(compound=molecules, n_compounds=n_each_lipid,
            region=boxes, overlap=overlap, edge=0.0, seed=seed)
    system.translate_to([0, 0, 0])
    box = system.boundingbox
    #box.lengths = box.lengths + [0.1/6, 0.1/6, 0.1/6]  # a tiny buffer
    filename = 'start.hoomdxml'.format(sys_num)
    system.save(filename, forcefield_files=ff_file, box=box, overwrite=True, ref_distance=0.1, foyer_kwargs={'assert_dihedral_params':False})
    # now get rind of number after ring in types (i.e., ring1 -> ring)
    for i in range(1, 1+4):
        os.system("perl -pi -e 's/ring{0}\n/ring\n/g' {1}".format(i, filename))
    # fix angles for CER NP and CER NS
    tree = ET.parse(filename)
    root = tree.getroot()
    remove_list = []
    for index, child in enumerate(root[0]):
        if child.tag == 'angle':
            old = child.text.split("\n")
            new = []
            for line in old:
                if line.split(" ")[0] == 'mhead2-tail-oh3':
                    oldline = cp.deepcopy(line)
                    newline1 = oldline.replace('mhead2-tail-oh3', 'mhead2-tail-oh3-a')
                    new.append(newline1)
                    oldline = cp.deepcopy(line)
                    newline2 = oldline.replace('mhead2-tail-oh3', 'mhead2-tail-oh3-b')
                    new.append(newline2)
                    print(newline1)
                    print(newline2)
                else:
                    new.append(line)
            new = "\n".join(new)
            root[0][index].text = new
        if child.tag == 'mass':
            mass = [""]
            for val in lipidlist:
                for i in range(int(val[1])):
                    for massval in val[0].masses:
                        mass.append(str(massval))
            mass.append("")
            mass = "\n".join(mass)
            root[0][index].text = mass
        if child.tag in {"pair_coeffs", "bond_coeffs", "angle_coeffs", "dihedral_coeffs"}:
            remove_list.append(child)
    for child in remove_list:
        root[0].remove(child)
    tree.write(filename)

# for CER:CHOL:FFA ratios, let's use
# 1:1:1 (33 mol%), 2:1:2 (20 mol%), 3:1:3 (14 mol%), and 5:1:5 (9 mol%)
n_lipids = 2200
n_wpl = 10
ff_file = '/Users/chloeframe/McCabeResearch/git/lipids/lipids/cg_molecules/cg-force-field.xml'


cer2_frac = 0.4

chol_frac = 0.2

ffa24_frac = 0.1552



lipids = [Cer2(),
          Chol(),
          FFA24()]

ppl = [cer2_frac,
       chol_frac,
       ffa24_frac]

apl = [45.0, 46.0, 24.0]
build_system(n_lipids, int(n_lipids*n_wpl), lipids, ppl, apl, ff_file, lipid_density=0.7, water_density=0.9, n_leaflets=6,seed=41169)

xml_file = mb.load('start.hoomdxml')
xml_file.save('start.gsd')
"""
for i in [3, 4, 5]:
    build_system(n_lipids, n_lipids*n_wpl, lipids, ppl, apl, ff_file, lipid_density=0.7, water_density=0.9, n_leaflets=2, sys_num=i, seed=1234*i)
"""
