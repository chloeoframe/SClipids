# CGskin

File and Folder Information: 

# Organizing your home directory on DMOG:
Make 3 main directories:

1.	Directory "forcefield" and within "forcefield" make a directory called "cg": this is where you will keep all the CG force field files

2.	Directory "programs" and within programs make a dir called "hoomd-funcs": this is where you keep some miscellaneous hoomd functions that are needed in the self-assembly script that hoomd didn’t have. This is pointed to in the submit.bash to include these functions.

3.	Directory "simulation": this is where all the experiments I do go. So within simulation, I would make a directory based upon what I’m simulating (based on this system: “mkdir cernscholffa24” . In the cernscholffa24 directory (path: /users/cf2067/simulation/nscholffa24), I would put (scp) the submit.bash, the run.py, and the start files.

## ff
the "ff" dir has readable information on what the bonded and nonbonded params are in there
## cg
in the 'cg' dir, is what you should scp up to DMOG which is the dimensionless .txt files  (tabulated nonbonded params) and the cg-bond-coeffs_stiff-tails-v3.p (bonded pickle file for bond coefficents)

## runonDMOG
Within you "simulation" directory I usually make a dir based upon whatever study I'm working on (i.e. "groen2011" which has a composition based upon the exp. paper from Daniel Groen 2011 in Biophys. J.)

So for example in the study "ternary_ns_212" (the study for the rest of this info), it's a CER NS C24, CHOL, FFA24 mixture in a 1:0.5:1 molar ratio.

On DMOG, to run this system, you need a topology (start.hoomdxml), a bash script to submit to the head node scheduler (submit.bash), and the actual self-assembly md code (run.py)

Submit.bash: this is the submitting a job to the cluster. This basically tells the cluster, hey when you’re ready and have the resources (all the #SBATCH conditions), run the .py script  

Run.py: this is the running molecular dynamics (MD) self-assembly script. So if you look into the script it changes in and out of MD ensembles in various steps. It takes the start file (start.hoomdxml) as the topology and the path to the force field (you need two things to do a simulation: topology and force field) 
**make sure the ff_dir and bond_pot/angle_pot points to YOUR directory

Start.hoomdxml: this is the starting topology for running the simulation using hoomd

Start.gsd: this is the topology you can use vmd to look at since vmd doesn’t like .hoomdxml files on newer macs (not necessary for DMOG but I always keep the .hoomdxml and .gsd together).


# Locally on your Mac:
## buildasystem

Build-random-cg.py: This script builds a CG randomized configuration where lipids are sandwiched between water slabs in the simulation box. When you run this script (typing “python build-random-cg.py” in the terminal window, the output is the two start files (start.hoomdxml and start.gsd). This script requires other files (a directory called lipids that has all the molecules and cg-force-field.xml which is the local FF to build). 
** Make sure within the build script you change the path to where you put the lipids directory. ** Note, in order to build a system, you have to create and run this script in an environment. I will include the lines at the end of this document (as well in conda.txt) you can type to create a conda environment called “building” where you can create systems.

conda create --name building -c conda-forge -c mosdef -c omnia -c -janschulz python=3.7.5 numpy=1.17.3 mbuild=0.10.5 mdtraj=1.9.4 foyer=0.7.4     scipy=1.3.3 parmed=3.2.0 openmm=7.4.1 jupyter openbabel=3.0.0 gsd

Directory "lipids": this is all the CG molecules you use when you run the build-random-cg.py script to make a randomized topology. You can look around (vim) the files if you want. In order to vmd the topologies, you'll need to use the convert.py to convert from .hoomdxml to .gsd because way back in a Mac version Catalina (~2019) the update went from 32-bit to 64-bit making vmd unable to look at .hoomdxml file extensions.

Using VMD on an M2/M3 chip or greater won't work but if working with Intel or M1:
Get this extension to be able to use gsd and vmd 
https://github.com/mphowardlab/gsd-vmd
