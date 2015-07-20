#!/bin/bash
#SBATCH --mem=2048
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=6
#SBATCH --exclude=moab,wasatch

date
hostname

ls-dyna-d ncpu=$SLURM_NTASKS i=$DYNADECK

rm d3*

python $FEMGIT/post/create_disp_dat.py --dat
python $FEMGIT/post/create_res_sim_mat.py --dynadeck $DYNADECK

if [ -e res_sim.mat ];
        then
            rm nodout;
            xz -v disp.dat;
fi
