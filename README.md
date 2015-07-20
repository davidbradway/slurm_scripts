SLURM scripts
=============
Local workstation functions to remotely launch SLURM commands on the cluster
from the workstation.  These commands will need SSH public keys to be in place
on the cluster and some local key manager to avoid having to enter passwords
all over the place.

*Note: these were originally SGE scripts, and not all of the commands have been
migrated, and many of the example scripts definitely have not been migrated.
If it starts with a 'q' or ends with a '.sge', then it still needs to be
converted.*

Useful SLURM URLs
=================
https://wiki.duke.edu/display/SCSC/SLURM+Queueing+System
http://www.uppmax.uu.se/sge-vs-slurm-comparison
https://rc.fas.harvard.edu/resources/documentation/convenient-slurm-commands
http://www.ibm.com/developerworks/library/l-slurm-utility
