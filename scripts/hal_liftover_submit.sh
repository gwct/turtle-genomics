#!/bin/bash
#SBATCH --job-name=turtle-halLiftover
#SBATCH --output=%x-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=greggwct@gmail.com
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --mem=100g
#SBATCH --time=48:00:00

hal="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/turtles.hal"
ref="Dcoriacea"
cactus_path="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/cactus_v2.2.0.sif"
cactusdir="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/"

cd $cactusdir

cat 00-etc/unnannotated-genomes.txt | parallel -j 8 "singularity exec --cleanenv $cactus_path halLiftover --outPSL $hal {} 02-bed/{}.bed $ref /dev/stdout | pslPosTarget stdin 03-psl/{}-to-$ref.psl"

