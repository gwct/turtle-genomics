#!/usr/bin/python
############################################################
# For turtles genomes, 01.2023
# Summarize orthology output for a set of genomes run
# with TOGA
############################################################

import sys, os, argparse, core, seqparse as SEQ
from collections import defaultdict

############################################################

indir = "/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/";
outfilename = "../data/dcoriacea-toga-orthology-summary.tsv";
# An output file for the orthology info
ref = "Dcoriacea";
# File info

indirs = [ d for d in os.listdir(indir) if os.path.isdir(os.path.join(indir, d)) and d.endswith("-to-" + ref) ];
specs = [ d.replace("-to-" + ref, "") for d in os.listdir(indir) if os.path.isdir(d) ];
# Get a list of input directories and query species

headers = ["ref.gene", "ref.transrcipt", "query.gene", "query.transcript", "orth.class", "query.spec" ];
# Headers for the orthology output file

with open(outfilename, "w") as outfile:
    outfile.write("\t".join(headers) + "\n");
    # Write the headers to the output file

    for d in indirs:

        spec = d.replace("-to-" + ref, "");
        print(spec);
        # Parse the current species name from the input directory

        orth_file = os.path.join(indir, d, "orthology_classification.tsv");
        # Get the current orth file

        first = True;
        for line in open(orth_file):
            if first:
                first = False;
                continue;
            outfile.write(line.replace("\n", "\t" + spec + "\n"));
        # Read the orth file (skipping the header) and writing each line to the main output file
        # with the species label

        feature_counts = defaultdict(int);
        feature_lens = [];
        # Output data for the feature summaries

        feature_count_file = "../data/feature-counts/" + spec + "-feature-counts-" + ref + "-toga.tab";
        feature_len_file = "../data/feature-counts/" + spec + "-feature-counts-lens-" + ref + "-toga.tab";
        # Output files for the feature summaries

        gene_spans_file = os.path.join(indir, d, "query_gene_spans.bed");
        for line in open(gene_spans_file):
            line = line.strip().split("\t");
            feature_lens.append(("gene", str(int(line[2]) - int(line[1]))));
            feature_counts["gene"] += 1;
        # Read through the gene spans file to get gene feature counts and lengths

        transcript_bed_file = os.path.join(indir, d, "query_annotation.bed");
        for line in open(transcript_bed_file):
            line = line.strip().split("\t");
            feature_lens.append(("transcript", str(int(line[2]) - int(line[1]))));
            feature_counts["transcript"] += 1;

            for cds in line[10].split(",")[:-1]:
                feature_lens.append(("CDS", cds));
                feature_counts["CDS"] += 1;
        # Read through the annotation file to get transcript and CDS feature counts and lengths

        #####
        #codon_fasta_file = os.path.join(indir, d, "codon.fasta");
        #codon_seqs = SEQ.fastaReadSeqs(codon_fasta_file);

        # found = set();
        # for seq in codon_seqs:
        #     if "REFERENCE" in seq:
        #         continue;

        #     raw_seq = codon_seqs[seq].replace(" ", "").replace("X", "").replace("-", "");
        #     raw_seq_len = len(raw_seq);
        #     # assert raw_seq_len % 3 == 0, "not div 3: " + seq + " " + str(len(codon_seqs[seq])) + " " + str(raw_seq_len) + "\n" + codon_seqs[seq] + "\n\n" + raw_seq;

        #     seq_id = seq.split(" | ")[0];
        #     if seq_id in found:
        #         print("dup id: " + seq_id);
        #     else:
        #         found.add(seq_id);

        #     feature_lens.append(("CDS", str(raw_seq_len)));
        #     feature_counts["CDS"] += 1;
        # A way to read the CDS sequences directly
        #####

        with open(feature_count_file, "w") as countfile:
            countfile.write("feature\tcount\n");
            for feature in feature_counts:
                countfile.write(feature + "\t" + str(feature_counts[feature]) + "\n");
        # Write out the feature counts

        with open(feature_len_file, "w") as lenfile:
            lenfile.write("feature\tlength\n");
            for ftup in feature_lens:
                lenfile.write(ftup[0] + "\t" + ftup[1] + "\n");
        # Write out the feature lengths
    ## End species loop
## Close orthology output file

        


