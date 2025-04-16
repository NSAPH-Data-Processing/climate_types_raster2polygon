#!/bin/bash
#
#SBATCH -p sapphire # partition (queue)
#SBATCH -c 30 # number of cores 
#SBATCH --mem 330GB # memory 
#SBATCH -t 0-04:00 # time (D-HH:MM)

snakemake --cores 3