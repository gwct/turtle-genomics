#!/usr/bin/env python3
#############################################################################
# Splits a genome for faster repeat masking
#
# Gregg Thomas
# Spring 2022
#############################################################################

import sys, os, random, core, seqparse as seq

#############################################################################

infilename = "/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Lkempii/LepKem1/LepKem1-11Jun2020.fasta";
outdir = "/n/holylfs05/LABS/informatics/Users/gthomas/turtles/genomes/Lkempii/LepKem1/repeat-masking/batches/";

batch_size = 1000;

print("Reading genome...");

seqs = seq.fastaReadSeqs(infilename);
scaffold_list = list(seqs.keys());

print(str(len(scaffold_list)) + " scaffolds read");

#print(scaffold_list[:10])
random.shuffle(scaffold_list);
#print(scaffold_list[:10])

batch_num = 1;
for batch in core.chunks(scaffold_list, batch_size):
    print(batch_num, len(batch));

    cur_outdir = os.path.join(outdir, str(batch_num));
    if not os.path.isdir(cur_outdir):
        os.makedirs(cur_outdir);

    cur_outfilename = os.path.join(cur_outdir, str(batch_num) + ".fa");
    with open(cur_outfilename, "w") as outfile:
        for scaffold in batch:
            outfile.write(">" + scaffold + "\n");
            outfile.write(seqs[scaffold] + "\n");

    batch_num += 1;


# batch_num = 1;
# cur_scaff = 1;

# for scaffold in scaffold_list:
#     if cur_scaff == batch_size:

#         batch_num += 1;


