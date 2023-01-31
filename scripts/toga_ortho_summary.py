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

        feature_counts = defaultdict(int);
        feature_lens = [];

        feature_count_file = "../data/feature-counts/" + spec + "-feature-counts-" + ref + "-toga.tab";
        feature_len_file = "../data/feature-counts/" + spec + "-feature-counts-lens-" + ref + "-toga.tab";

        gene_spans_file = os.path.join(indir, d, "query_gene_spans.bed");
        for line in open(gene_spans_file):
            line = line.strip().split("\t");
            feature_lens.append(("gene", str(int(line[2]) - int(line[1]))));
            feature_counts["gene"] += 1;


        transcript_bed_file = os.path.join(indir, d, "query_annotation.bed");
        for line in open(transcript_bed_file):
            line = line.strip().split("\t");
            feature_lens.append(("transcript", str(int(line[2]) - int(line[1]))));
            feature_counts["transcript"] += 1;

            for cds in line[10].split(",")[:-1]:
                feature_lens.append(("CDS", cds));
                feature_counts["CDS"] += 1;

        codon_fasta_file = os.path.join(indir, d, "codon.fasta");
        codon_seqs = SEQ.fastaReadSeqs(codon_fasta_file);

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

        with open(feature_count_file, "w") as countfile:
            countfile.write("feature\tcount\n");
            for feature in feature_counts:
                countfile.write(feature + "\t" + str(feature_counts[feature]) + "\n");

        with open(feature_len_file, "w") as lenfile:
            lenfile.write("feature\tlength\n");
            for ftup in feature_lens:
                lenfile.write(ftup[0] + "\t" + ftup[1] + "\n");


        


