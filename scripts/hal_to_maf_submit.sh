#!/bin/bash
#SBATCH --job-name=turtle-hal2maf
#SBATCH --output=%x-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=greggwct@gmail.com
#SBATCH --partition=bigmem
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=400g
#SBATCH --time=48:00:00

hal="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/turtles.hal"
ref="Dcoriacea"
maf="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/00-maf-rmdups/turtles"
cactus_path="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/cactus_v2.2.0.sif"
outdir="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/00-maf-rmdups/"
tmpdir="/n/holylfs05/LABS/informatics/Users/gthomas/tmp/"

cd $outdir

singularity exec --nv --cleanenv --bind $tmp:/tmp $cactus_path hal2mafMP.py --numProc 46 --splitBySequence --noDupes --refGenome $ref $hal $maf