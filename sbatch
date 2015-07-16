#!/usr/bin/env python
"""
To make this really useful, you'll need to have public key ssh authentication
setup.

USAGE: sbatch job_script.sh

Mark Palmeri
mlp6@duke.edu
2015-04-29
"""

import os
import sys
import argparse as ap

p = ap.ArgumentParser(description="Submit SLURM jobs via sbatch over ssh "
                      "command tunnel from workstation",
                      formatter_class=ap.ArgumentDefaultsHelpFormatter)
p.add_argument("--python",
               help="use python command interpretation instead of bash",
               action="store_true",
               default=False)
p.add_argument("SLURM_JOB",
               help="SLURM job command line arguments and script file",
               default=None)
#p.add_argument("--SLURM_TMP_DIR",
#               help="SLURM tmp directory (STDOUT/STDERR)",
#               default='sgetmp')
p.add_argument("--cluster_headnode",
               help="cluster head node",
               default='durmstrang.egr.duke.edu')
args = p.parse_args()

python = args.python
cluster_headnode = args.cluster_headnode
#SLURM_TMP_DIR = args.SLURM_TMP_DIR

try:
    SLURM_JOB = args.SLURM_JOB
except:
    sys.exit('SLURM_JOB not defined')

# define the current working directory
CWD = os.getcwd()

# test to make sure that the SLURM job script exists (last item of the potential
# multi-item string)
SLURM_SCRIPT = SLURM_JOB.split()[-1]
if not os.path.exists(SLURM_SCRIPT):
    print "ERROR: %s script does not exist" % SLURM_SCRIPT
    sys.exit()

# create the SLURM tmp directory if it doesn't exist
#if not os.path.isdir(SLURM_TMP_DIR):
#    os.mkdir(SLURM_TMP_DIR)
#    print "SLURM output/error directory created: %s" % SLURM_TMP_DIR

# define the ssh commandline to execute
if python:
    print('PYTHON SCRIPTS NOT SUPPORTED YET')
    #SSH_CMD = "cd %s; sbatch -S /usr/bin/python -o %s -e %s -V -cwd %s;" % \
    #    (CWD, SLURM_TMP_DIR, SLURM_TMP_DIR, SLURM_JOB)
else:
    SSH_CMD = "cd %s; sbatch %s;" % \
        (CWD, SLURM_JOB)

# display the command being run
print('EXECUTING: %s\n' % SSH_CMD)

# run the ssh command
os.system("ssh %s '%s'" % (cluster_headnode, SSH_CMD))
