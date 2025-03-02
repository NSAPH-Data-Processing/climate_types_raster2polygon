#!/bin/bash
#
#SBATCH -p shared # partition (queue)
#SBATCH -c 12 # number of cores 
#SBATCH --mem 96GB # memory 
#SBATCH -t 0-01:00 # time (D-HH:MM)

snakemake --cores 6