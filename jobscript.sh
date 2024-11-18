#!/bin/sh
### General options
### –- specify queue --
#BSUB -q gpua100
### -- set the job Name --
#BSUB -J testjob
### -- ask for number of cores (default: 1) --
#BSUB -n 8
### -- Select the resources: 1 gpu in exclusive process mode --
#BSUB -gpu "num=2:mode=exclusive_process"
### -- set walltime limit: hh:mm --  maximum 24 hours for GPU-queues right now
#BSUB -W 1:00
# request 16GB of system-memory
#BSUB -R "rusage[mem=16GB]"

#BSUB -R "select[gpu32gb]"

#BSUB -R "select[sxm2]"

### -- set the email address --
# please uncomment the following line and put in your e-mail address,
# if you want to receive e-mail notifications on a non-default address
##BSUB -u s111503@dtu.dk
### -- send notification at start --
#BSUB -B
### -- send notification at completion--
#BSUB -N
### -- Specify the output and error file. %J is the job-id --
### -- -o and -e mean append, -oo and -eo mean overwrite --
#BSUB -o gpu_%J.out
#BSUB -e gpu_%J.err
# -- end of LSF options --

nvidia-smi
# Load the cuda module
module load cuda/11.6
# Load the necessary modules
module load python/3.9

/appl/cuda/11.6.0/samples/bin/x86_64/linux/release/deviceQuery
# Activate the virtual environment
source /zhome/e1/5/68452/odyssey/.venv/Script/activate

# Run the Python script
python /zhome/e1/5/68452/odyssey/jobscript.py