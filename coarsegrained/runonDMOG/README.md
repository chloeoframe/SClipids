2.	On DMOG in your home directory, make the three directories (simulation, forcefield, programs). “mkdir name” is the command you will use.
a.	Now locally, (see helpful commands below)
i.	scp the “cg” force field directory in the directory you made
ii.	scp the “hoomd-funcs” to the programs directory you made
iii.	scp the start files, run.py, and submit bash to the simulation study directory you made
3.	Change all of the directory paths to connect properly with the right path for your account on DMOG (my account is cf2067).
a.	Two lines in run.py (FF path)
ff_dir = '/users/cf2067/forcefields/cg' # all the .txt files are the non bonded parameters between that bead combination
bond_pot, angle_pot = load_bonded_coeffs(system, bond_pot, angle_pot, '/users/cf2067/forcefields/cg /cg-bond-coeffs_stiff-tails-v3.p', units['D'], units['E'])
b.	in submit.bash (email)
4.	All the pieces should be there and connected so you can run a simulation by typing
 “sbatch submit.bash”

Useful terminal commands:

•	ls: list or show me what is in that directory

•	mkdir foldername: make a directory

•	cd path: to move around from folder to folder

•	pwd: to figure out which directory you are in

•	vim run.py: vim allows you to read into the file run.py; you can type “a” or “i” to start inserting text. To save and close out type “:wq”. To close out and not save changes type “:q!”.

•	sbatch submit.bash: “sbatch” is the submit to the cluster command so “sbatch submit.bash” submits the whole process to the cluster to run

•	squeue -u (your ID name): this will tell you if your job is running and for how long. For example: “squeue -u cf2067” will tell me which jobs are running

•	this is locally, so not on DMOG, opening another terminal window: to push up a file (for example run.py) from your computer up to the cluster where you want to put it:
scp run.py cf2067@dmog.hw.ac.uk:/users/cf2067/simulation/cernscholffa24

•	scp -r cg cf2067@dmog.hw.ac.uk:/users/cf2067/forcefields

•	scp -r hoomd-funcs cf2067@dmog.hw.ac.uk:/users/cf2067/programs

**scp -r (you need a -r anytime you move around a directory)

•	To push a file up to the cluster: scp file username@cluster:/path
•	To pull a file down from the cluster: scp username@cluster:/path/file locallocation
o	For example, pulling down a trajectory that is done running:
scp username@cluster:/path/traj.dcd /Users/chloeframe/McCabeResearch/buildingfiles/cernscholffa24/trial1/

