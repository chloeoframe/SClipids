import random
import math

import hoomd
#from hoomd_script import util;
#from hoomd_script import globals;
#from hoomd_script import data; 


SUPPORTED_DISTRIBUTIONS = ['gaussian']

## Initialize a velocity distribution
def init_velocity(group=None, T=None, seed=12345, distribution='gaussian',
        zero=True):
#    util.print_status_line()
#
#    if group == None:
#        globals.msg.error("Must give a group of particles to initialize velocity.\n")
#        raise RuntimeError('Error initializing velocities.')

#    if T == None:
#        globals.msg.error("Must give a temperature to initialize velocity.\n")
#        raise RuntimeError('Error initializing velocities.')
#    if distribution not in SUPPORTED_DISTRIBUTIONS:
#        globals.msg.error('Unsupported velocity distribution.\n')
#        raise RuntimeError('Unsupported velocity distribution, supported distributions are: {0}\n'.format(', '.join(SUPPORTED_DISTRIBUTIONS)))

    random.seed(seed)
    px = py = pz = 0.0
    for p in group:
        mass = p.mass
    if distribution == 'gaussian':
        vx = random.gauss(0, math.sqrt(T/mass))
        vy = random.gauss(0, math.sqrt(T/mass))
        vz = random.gauss(0, math.sqrt(T/mass))
        p.velocity = (vx, vy, vz)
        px += mass * vx
        py += mass * vy
        pz += mass * vz
            
   # zero out the total system momentum if specified
    if zero == True:
        px /= len(group)
        py /= len(group)
        pz /= len(group)
        for p in group:
            mass = p.mass
            v = p.velocity
            p.velocity = (v[0] - px/mass, v[1] - py/mass, v[2] - pz/mass)
