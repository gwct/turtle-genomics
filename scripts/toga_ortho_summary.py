#!/usr/bin/python
############################################################
# For turtles genomes, 01.2023
# Summarize orthology output for a set of genomes run
# with TOGA
############################################################

import sys, os, argparse, core

############################################################

indir = "/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/";
outfilename = "../data/dcoriacea-toga-orthology-summary.tsv";
ref = "Dcoriacea";

print(os.listdir(indir));
indirs = [ d for d in os.listdir(indir) if os.path.isdir(os.path.join(indir, d)) and d.endswith("-to-" + ref) ];
print(indirs);
specs = [ d.replace("-to-" + ref, "") for d in os.listdir(indir) if os.path.isdir(d) ];

#transcripts = defaultdict(dict);
headers = ["ref.gene", "ref.transrcipt", "query.gene", "query.transcript", "orth.class", "query.spec" ];

with open(outfilename, "w") as outfile:
    outfile.write("\t".join(headers) + "\n");

    for d in indirs:
        spec = d.replace("-to-" + ref, "");
        print(spec);
        orth_file = os.path.join(indir, d, "orthology_classification.tsv");

        first = True;
        for line in open(orth_file):
            if first:
                first = False;
                continue;
            outfile.write(line.replace("\n", "\t" + spec + "\n"));


