#!/bin/bash -l
#SBATCH --job-name=ns-test
#SBATCH --mail-type=START,END,FAIL
#SBATCH --mail-user=chloe.o.frame@vanderbilt.edu
#SBATCH --nodes=1 
#SBATCH --ntasks=8
#SBATCH --time=1-00:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2
#SBATCH --qos=eps_comsel
cd $SLURM_SUBMIT_DIR
echo $SLURM_JOB_ID $SLURM_SUBMIT_DIR >> ~/job-id-dirs.txt
flight env activate gridware
module load apps/anaconda3/2023.03/bin
module load libs/hoomdblue/2.9.7+sp
export PYTHONPATH=$HOME/programs/hoomd-funcs:$PYTHONPATH

# for smaller systems only use one GPU:
srun -n 2 python run.py &> run.log
conda activate wrap
wrap_traj -f prod_short.dcd -c start.hoomdxml -o done.dcd

