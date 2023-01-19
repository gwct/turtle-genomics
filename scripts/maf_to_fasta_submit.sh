#!/bin/bash
#SBATCH --job-name=turtle_maf2fasta
#SBATCH --output=%x-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=greggwct@gmail.com
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --cpus-per-task=1
#SBATCH --mem=100g
#SBATCH --time=24:00:00

wd="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/windows/phast_scripts/"
mafdir="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/00-maf-rmdups-sorted/"
beddir="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/windows/01-bed/"
outdir="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/windows/02-fasta/"
windowsize="10kb"
ref="Dcoriacea"

cd $wd

ls $mafdir | grep -v index | cut -d "-" -f 1 | cut -d "_" -f 2,3 | parallel -j 20 python maf2fasta.py --maf $mafdir/turtles_{}-sorted.maf --bed $beddir/{}-$windowsize-windows.bed --ref_species $ref --out_folder $outdir/{}-$windowsize-windows/

