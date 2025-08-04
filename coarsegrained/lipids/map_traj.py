#!/usr/bin/env python
# coding: utf-8

# In[1]:


import copy as cp
import os
import xml.etree.ElementTree as ET

import mdtraj as md
import mbuild as mb

from cg_mapping.mapper import Mapper


traj = md.load("wrap.xtc", top="tip.gro")[-100:]

traj.atom_slice(traj.top.select("not resname tip3p"), inplace=True)

mapper = Mapper()
mapper.load_mapping_dir()
mapper.load_trajectory(traj)

cg_traj = mapper.cg_map()


# In[ ]:





# In[3]:


def save_cg_hoomdxml(traj, filename, ff_file):
    """
    This is for saving a cg_traj to a hoomdxml file.

    """

    # Creates mbuild.Compound and box from last frame
    system = mb.Compound()
    system.from_trajectory(traj[-1])
    box = mb.Box(lengths=traj.unitcell_lengths[-1])

    # Adds '_' to particle names to signify CG particles
    for particle in system.particles():
        if particle.name == "tip3p":
            particle.name = "water"
        particle.name = "_"+ particle.name.strip()

    # Saves to hoomdxml using mbuild and foyer
    system.save(filename,
                forcefield_files=ff_file,
                box=box,
                overwrite=True,
                ref_distance=0.1,
                foyer_kwargs={"assert_dihedral_params":False})

    # now get number after ring in types (i.e., ring1 -> ring)
    for i in range(1, 1+4):
        os.system("perl -pi -e 's/ring{0}\n/ring\n/g' {1}".format(i, filename))

    # Add extra angle for CER NP and CER AP for layered potential
    tree = ET.parse(filename)
    root = tree.getroot()
    remove_list = []
    for index, child in enumerate(root[0]):
        if child.tag == "angle":
            old = child.text.split("\n")
            new = []
            for line in old:
                if line.split(" ")[0] == "mhead2-tail-oh3":
                    oldline = cp.deepcopy(line)
                    newline1 = oldline.replace("mhead2-tail-oh3", "mhead2-tail-oh3-a")
                    new.append(newline1)
                    oldline = cp.deepcopy(line)
                    newline2 = oldline.replace("mhead2-tail-oh3", "mhead2-tail-oh3-b")
                    new.append(newline2)
                else:
                    new.append(line)
            new = "\n".join(new)
            root[0][index].text = new
        if child.tag in {"pair_coeffs", "bond_coeffs", "angle_coeffs", "dihedral_coeffs"}:
            remove_list.append(child)
    for child in remove_list:
        root[0].remove(child)
    tree.write(filename)


# In[4]:


# Scales the trajectory to CG units (1 cg_unit = 6 A)
cg_traj.xyz /= 6
cg_traj.unitcell_lengths /= 6

save_cg_hoomdxml(cg_traj,
                 "cg-traj.hoomdxml",
                 "/Users/chloeframe/McCabeResearch/git/lipids/lipids/cg_molecules/cg-force-field.xml")

cg_traj.save("cg-traj.xtc")


# In[ ]:




