#!/bin/bash
#SBATCH --job-name=turtle_aa_busco
#SBATCH --output=%x-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=gthomas@g.harvard.edu
#SBATCH --partition=holy-info,shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32g
#SBATCH --time=10:00:00

projectdir="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/"
db="/n/holyscratch01/external_repos/INFORMATICS/BUSCO/sauropsida_odb10"
tmpdir="/n/holylfs05/LABS/informatics/Users/gthomas/tmp/"
query="Amarmorata"
ref="Dcoriacea"
indir="$projectdir/$query-to-$ref/"
infile="$query-aa-longest.fa"
out="$query-aa-busco"

cd $indir
echo $indir
echo $infile
echo $out

busco -i $infile -c 16 -m prot -l $db -t $tmpdir -o $out