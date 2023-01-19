#!/bin/bash
#SBATCH --job-name=turtle-axtChain
#SBATCH --output=%x-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=greggwct@gmail.com
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --mem=60g
#SBATCH --time=48:00:00

hal="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/turtles.hal"
ref="Dcoriacea"
cactus_path="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/cactus_v2.2.0.sif"
cactusdir="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/"

cd $cactusdir

cat 00-etc/unnannotated-genomes.txt | parallel -j 8 "axtChain -psl -linearGap=loose 03-psl/{}-to-$ref.psl 01-2bit/$ref.2bit 01-2bit/{}.2bit 04-chain/{}-to-$ref.chain"