#!/bin/bash
#SBATCH --job-name=turtle_liftoff_amar2_cpic
#SBATCH --output=%x-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=gthomas@g.harvard.edu
#SBATCH --partition=holy-info,shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32g
#SBATCH --time=10:00:00

# ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Pcastaneus/Pelusios_castaneus.Pelusios_castaneus-1.0.dna_sm.toplevel.fa
# gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Pcastaneus/Pelusios_castaneus.Pelusios_castaneus-1.0.104.gff3.gz

# target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Pexpansa/GCA_007922195.1_Podocnemis_expansa-1.0/GCA_007922195.1_Podocnemis_expansa-1.0_genomic.fna

# tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

# outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Pexpansa-liftoff/pexpansa-pcastaneus-liftoff.gff
# unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Pexpansa-liftoff/pexpansa-pcastaneus-liftoff-unmapped.gff

# liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref

#############

# ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Pcastaneus/Pelusios_castaneus.Pelusios_castaneus-1.0.dna_sm.toplevel.fa
# gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Pcastaneus/Pelusios_castaneus.Pelusios_castaneus-1.0.104.gff3.gz

# target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Mtuberculata/GCA_007922155.1_Mesoclemmys_tuberculata-1.0/GCA_007922155.1_Mesoclemmys_tuberculata-1.0_genomic.fna

# tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

# outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Mtuberculata-liftoff/mtuberculata-pcastaneus-liftoff.gff
# unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Mtuberculata-liftoff/mtuberculata-pcastaneus-liftoff-unmapped.gff

# liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref

#############

# ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Pcastaneus/Pelusios_castaneus.Pelusios_castaneus-1.0.dna_sm.toplevel.fa
# gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Pcastaneus/Pelusios_castaneus.Pelusios_castaneus-1.0.104.gff3.gz

# target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Esubglobosa/GCA_007922225.1_Emydura_subglobosa-1.0/GCA_007922225.1_Emydura_subglobosa-1.0_genomic.fna

# tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

# outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Esubglobosa-liftoff/esubglobosa-pcastaneus-liftoff.gff
# unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Esubglobosa-liftoff/esubglobosa-pcastaneus-liftoff-unmapped.gff

# liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref

#############

# ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Psinensis/Pelodiscus_sinensis.PelSin_1.0.dna_sm.toplevel.fa
# gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Psinensis/Pelodiscus_sinensis.PelSin_1.0.104.gff3.gz

# target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Rswinhoei/GCA_019425775.1_ASM1942577v1/GCA_019425775.1_ASM1942577v1_genomic.fna

# tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

# outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Rswinhoei-liftoff/rswinhoei-psinensis-liftoff.gff
# unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Rswinhoei-liftoff/rswinhoei-psinensis-liftoff-unmapped.gff

# liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref

#############

# ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Psinensis/Pelodiscus_sinensis.PelSin_1.0.dna_sm.toplevel.fa
# gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Psinensis/Pelodiscus_sinensis.PelSin_1.0.104.gff3.gz

# target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Cinsculpta/GCA_007922185.1_Carettochelys_insculpta-1.0/GCA_007922185.1_Carettochelys_insculpta-1.0_genomic.fna

# tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

# outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Cinsculpta-liftoff/cinsculpta-psinensis-liftoff.gff
# unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Cinsculpta-liftoff/cinsculpta-psinensis-liftoff-unmapped.gff

# liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref

#############

# ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Cserpentina/Chelydra_serpentina.Chelydra_serpentina-1.0.dna_sm.toplevel.fa
# gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Cserpentina/Chelydra_serpentina.Chelydra_serpentina-1.0.104.gff3.gz

# target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Dmawii/GCA_007922305.1_Dermatemys_mawii-1.0/GCA_007922305.1_Dermatemys_mawii-1.0_genomic.fna

# tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

# outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Dmawii-liftoff/dmawii-cserpentina-liftoff.gff
# unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Dmawii-liftoff/dmawii-cserpentina-liftoff-unmapped.gff

# liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref

#############

ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Cpicta/Chrysemys_picta_bellii.Chrysemys_picta_bellii-3.0.3.dna_sm.toplevel.fa
gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Cpicta/Chrysemys_picta_bellii.Chrysemys_picta_bellii-3.0.3.104.gff3.gz

target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Amarmorata/GCA_022086475.1_rActMar1.p/GCA_022086475.1_rActMar1.p_genomic.fna

tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Amarmorata-liftoff/amarmorata-cpicta-liftoff.gff
unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Amarmorata-liftoff/amarmorata-cpicta-liftoff-unmapped.gff

liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref

# #############

# ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Cpicta/Chrysemys_picta_bellii.Chrysemys_picta_bellii-3.0.3.dna_sm.toplevel.fa
# gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Cpicta/Chrysemys_picta_bellii.Chrysemys_picta_bellii-3.0.3.104.gff3.gz

# target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Mterrapin/GCA_001728815.2_terp_v2_2/GCA_001728815.2_terp_v2_2_genomic.fna

# tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

# outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Mterrapin-liftoff/mterrapin-cpicta-liftoff.gff
# unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Mterrapin-liftoff/mterrapin-cpicta-liftoff-unmapped.gff

# liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref

# #############

# ref=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Mreevesii/GCF_016161935.1_ASM1616193v1/GCF_016161935.1_ASM1616193v1_genomic.fna
# gff=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Mreevesii/GCF_016161935.1_ASM1616193v1/GCF_016161935.1_ASM1616193v1_genomic.gff.gz

# target=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Cmccordii/GCA_003846335.1_ASM384633v1/GCA_003846335.1_ASM384633v1_genomic.fna

# tmpdir=/n/holylfs05/LABS/informatics/Users/gthomas/tmp/

# outfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Cmccordii-liftoff/cmccordii-mreevesii-liftoff.gff
# unmappedfile=/n/holylfs05/LABS/informatics/Users/gthomas/turtles/liftoff/Cmccordii-liftoff/cmccordii-mreevesii-liftoff-unmapped.gff

# liftoff -g $gff -o $outfile -u $unmappedfile -dir $tmpdir -p 16 $target $ref
