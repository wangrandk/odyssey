#!/bin/bash
#SBATCH --job-name=EHRMamba_Pretrain
#SBATCH --output=EHRMamba_Pretrain_%j.out
#SBATCH --error=EHRMamba_Pretrain_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your_email_address

# Load necessary modules
module load python/3.9

# Activate virtual environment
source .venv/bin/activate

# Run your pretraining script
python pretrain.py --config config.yaml