"""
p42_cardiac.py - setup sge scripts to launch sims on the cluster
"""

__author__ = 'Mark Palmeri'
__date__ = '2012-05-01'

import os

# Run sims of the P42 for David that have different stiffnesses, focal depths and attenuations (cardiac).

# define some stuff
#run = 'local'
run = 'sge'
YM = [4.5,36]
Freq = [1.75,2.00,2.25,2.50]
Fnum = [1.5,2.0,2.5,3.0,3.5]
FD = [0.03,0.04,0.05,0.06,0.07]
alpha = [0.3,0.4,0.5,0.6]

root = '/getlab/mlp6/p42_cardiac_sims'
p42dyn='p42_cardiac.dyn'
SGE_FILENAME = 'p42_cardiac.sge'

for i in range(len(Freq)):
    for j in range(len(Fnum)):
        for k in range(len(FD)):
            for l in range(len(alpha)):
                for m in range(len(YM)):

                    field_path = '%s/field/dyna-I-f%.2f-F%.1f-FD%.2f-a%.1f.mat' % (root,Freq[i],Fnum[j],FD[k],alpha[l])

                    if os.path.exists(field_path):

                        sim_path = '%s/E%.1fkPa/%.2fMHz/F%.1f/FD%.2fcm/a%.1f/' % (root,YM[m],Freq[i],Fnum[j],FD[k],alpha[l]) 

                        if not os.path.exists(sim_path):
                            os.makedirs(sim_path)

                        os.chdir(sim_path)
                        print(os.getcwd())

                        if not os.path.exists('res_sim.mat'):
                            os.system('cp %s/%s .' % (root,p42dyn))
                            os.system("sed -i -e 's/YM/%.1f/' %s" % (YM[m]*10000.0,p42dyn))
                            os.system("sed -i -e 's/FREQ/%.2f/' %s" % (Freq[i],p42dyn))
                            os.system("sed -i -e 's/FNUM/%.1f/' %s" % (Fnum[j],p42dyn))
                            os.system("sed -i -e 's/FOCDEPTH/%.2f/' %s" % (FD[k],p42dyn))
                            os.system("sed -i -e 's/ALPHA/%.1f/' %s" % (alpha[l],p42dyn))
                            os.system("sed -i -e 's/TOFF1/%.1f/' %s" % (960/Freq[i],p42dyn))
                            os.system("sed -i -e 's/TOFF2/%.1f/' %s" % ((960/Freq[i])+1,p42dyn))

                            if run == 'sge':
                                # create sge output file
                                SGE_FILE = open('%s' % SGE_FILENAME,'w')
                                SGE_FILE.write('#!/bin/bash\n')
                                SGE_FILE.write('#$ -S /bin/bash\n')
                                SGE_FILE.write('#$ -o sgetmp\n')
                                SGE_FILE.write('#$ -e sgetmp\n')
                                SGE_FILE.write('#$ -V\n')
                                SGE_FILE.write('#$ -cwd\n')
                                SGE_FILE.write('#$ -l num_proc=24\n')
                                SGE_FILE.write('#$ -l mem_free=4G\n')
                                SGE_FILE.write('#$ -pe smp 8\n')
                                #SGE_FILE.write('#$ -R y\n')
                                
                                SGE_FILE.write('date\n')
                                SGE_FILE.write('hostname\n')

                                SGE_FILE.write('export DISPLAY=\n')
                                SGE_FILE.write('ls-dyna-sR5 ncpu=$NSLOTS i=%s\n' % (p42dyn))
                                SGE_FILE.write('/krnlab/mlp6/fem/dyna/StructPost %s %s/mesh/nodes.asc\n' % (p42dyn,root))
                                SGE_FILE.write('if [ -e res_sim.mat ]; then rm d3*; fi\n')
                                SGE_FILE.write('if [ -e res_sim.mat ]; then rm disk8*; fi\n')
                                SGE_FILE.write('if [ -e disp.dat ]; then xz disp.dat; fi\n')
                                SGE_FILE.close()

                                os.system('qsub %s' % (SGE_FILENAME))
                            else:
                                os.system('ls-dyna-sR5 ncpu=7 i=gaussian.dyn')
                                os.system('/krnlab/mlp6/fem/dyna/StructPost gaussian.dyn /getlab/mlp6/p42_cardiac_sims/mesh/nodes.asc')
                                os.system('if [ -e res_sim.mat ]; then rm d3*; fi\n');
                                os.system('if [ -e res_sim.mat ]; then rm disk8*; fi\n')
                                os.system('if [ -e disp.dat ]; then xz disp.dat; fi\n')
                        else:
                            print('res_sim.mat already exists')
