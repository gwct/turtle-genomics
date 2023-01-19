#!/bin/bash

mamba activate toga

cactusdir="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/"
togapath="/n/home07/gthomas/env/pkgs/TOGA"

ref="Dcoriacea"
refcds="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Dcoriacea/GCF_009764565.3_rDerCor1.pri.v4/GCF_009764565.3_rDerCor1.pri.v4_cds.bed"
refiso="/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Dcoriacea/GCF_009764565.3_rDerCor1.pri.v4/GCF_009764565.3_rDerCor1.pri.v4_isoforms.tsv"

query="Rswinhoei"

cd $cactusdir

time -p python $togapath/toga.py 04-chain/$query-to-$ref.chain $refcds 01-2bit/$ref.2bit 01-2bit/$query.2bit --kt --pd 05-toga/$query-to-$ref/ -i $refiso --nc $togapath/nextflow_config_files/ --cb 10,100 --cjn 750




## Amarmorata
# Calling orthology_type_map...
# Extracted 79579 query transcripts
# After filters 62100 transcripts left
# Added 18774 reference genes on graph
# Added 18364 query genes on graph
# Graph contains 61973 connections
# Detected 18454 orthology components
# Orthology class sizes:
# one2one: 16026
# one2zero: 1556
# one2many: 662
# many2many: 136
# many2one: 74
# #### STEP 11: Cleanup: merge parallel steps output files
# Saved results to /n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/Amarmorata-to-Dcoriacea
# real 23849.85
# user 573.18
# sys 157.30

## Cinsculpta
# Calling orthology_type_map...
# Extracted 68318 query transcripts
# After filters 61065 transcripts left
# Added 18774 reference genes on graph
# Added 17584 query genes on graph
# Graph contains 61034 connections
# Detected 18524 orthology components
# Orthology class sizes:
# one2one: 14830
# one2zero: 2347
# one2many: 1176
# many2one: 107
# many2many: 64
# #### STEP 11: Cleanup: merge parallel steps output files
# Saved results to /n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/Cinsculpta-to-Dcoriacea
# real 24466.61
# user 636.99
# sys 121.34

## Cmccordi
# Calling orthology_type_map...
# Extracted 79581 query transcripts
# After filters 61522 transcripts left
# Added 18774 reference genes on graph
# Added 18069 query genes on graph
# Graph contains 61455 connections
# Detected 18442 orthology components
# Orthology class sizes:
# one2one: 15924
# one2zero: 1697
# one2many: 612
# many2many: 129
# many2one: 80
# #### STEP 11: Cleanup: merge parallel steps output files
# Saved results to /n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/Cmccordi-to-Dcoriacea
# real 33188.05
# user 745.40
# sys 190.81

## Dmawii
# Calling orthology_type_map...
# Extracted 68647 query transcripts
# After filters 60223 transcripts left
# Added 18774 reference genes on graph
# Added 17630 query genes on graph
# Graph contains 60194 connections
# Detected 18471 orthology components
# Orthology class sizes:
# one2one: 16003
# one2zero: 1775
# one2many: 505
# many2many: 103
# many2one: 85
# #### STEP 11: Cleanup: merge parallel steps output files
# Saved results to /n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/Dmawii-to-Dcoriacea
# real 59815.64
# user 948.96
# sys 251.72

## Esubglobosa
# Calling orthology_type_map...
# Extracted 69836 query transcripts
# After filters 61948 transcripts left
# Added 18774 reference genes on graph
# Added 17932 query genes on graph
# Graph contains 61875 connections
# Detected 18402 orthology components
# Orthology class sizes:
# one2one: 15955
# one2zero: 1641
# one2many: 592
# many2one: 110
# many2many: 104
# #### STEP 11: Cleanup: merge parallel steps output files
# Saved results to /n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/Esubglobosa-to-Dcoriacea
# real 27539.73
# user 753.86
# sys 155.29

## Mtuberculata
# Calling orthology_type_map...
# Extracted 71371 query transcripts
# After filters 62972 transcripts left
# Added 18774 reference genes on graph
# Added 18232 query genes on graph
# Graph contains 62884 connections
# Detected 18462 orthology components
# Orthology class sizes:
# one2one: 15374
# one2zero: 1793
# one2many: 1115
# many2many: 94
# many2one: 86
# #### STEP 11: Cleanup: merge parallel steps output files
# Saved results to /n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/Mtuberculata-to-Dcoriacea
# real 22156.43
# user 713.72
# sys 133.03

## Pexpansa
# Calling orthology_type_map...
# Extracted 68322 query transcripts
# After filters 60555 transcripts left
# Added 18774 reference genes on graph
# Added 17549 query genes on graph
# Graph contains 60316 connections
# Detected 18477 orthology components
# Orthology class sizes:
# one2one: 16121
# one2zero: 1819
# one2many: 358
# many2many: 99
# many2one: 80
# #### STEP 11: Cleanup: merge parallel steps output files
# Saved results to /n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/Pexpansa-to-Dcoriacea
# real 31253.38
# user 697.51
# sys 170.77

## Rswinhoei
# Calling orthology_type_map...
# Extracted 67551 query transcripts
# After filters 60617 transcripts left
# Added 18774 reference genes on graph
# Added 17607 query genes on graph
# Graph contains 60169 connections
# Detected 18405 orthology components
# Orthology class sizes:
# one2one: 16123
# one2zero: 1780
# one2many: 284
# many2many: 113
# many2one: 105
# #### STEP 11: Cleanup: merge parallel steps output files
# Saved results to /n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/Rswinhoei-to-Dcoriacea
# real 23904.70
# user 878.16
# sys 115.86