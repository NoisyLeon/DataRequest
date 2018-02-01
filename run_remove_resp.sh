#!/bin/bash

#SBATCH -J RESP
#SBATCH -o RESP_%j.out
#SBATCH -e RESP_%j.err
#SBATCH -N 1
#SBATCH --ntasks-per-node=24
#SBATCH --time=100:00:00
#SBATCH --mem=MaxMemPerNode
#SBATCH --mail-user=lili.feng@colorado.edu
#SBATCH --mail-type=ALL


cd /projects/life9360/code/DataRequest
python remove_response_DMT.py
