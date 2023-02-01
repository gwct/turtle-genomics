#!/usr/bin/python
############################################################
# For turtles genomes, 01.2023
# Remove reference sequences from the three Toga fasta outputs
############################################################

import sys, os, argparse, core, seqparse as SEQ
from collections import defaultdict

############################################################

indir = "/n/holylfs05/LABS/informatics/Users/gthomas/turtles/cactus/turtle-output-smk/05-toga/";
ref = "Dcoriacea";
# File info

indirs = [ d for d in os.listdir(indir) if os.path.isdir(os.path.join(indir, d)) and d.endswith("-to-" + ref) ];
specs = [ d.replace("-to-" + ref, "") for d in os.listdir(indir) if os.path.isdir(d) ];
# Get a list of input directories and query species

####################

for d in indirs:

    spec = d.replace("-to-" + ref, "");
    print(spec);
    # Parse the current species name from the input directory

    isoform_file = os.path.join(indir, d, "query_isoforms.tsv");
    nt_file = os.path.join(indir, d, "nucleotide.fasta");
    cds_file = os.path.join(indir, d, "codon.fasta");
    aa_file = os.path.join(indir, d, "prot.fasta");
    in_files = [nt_file, cds_file, aa_file];
    # Get the current input files

    nt_out_file = os.path.join(indir, d, spec + "-nt.fa");
    cds_out_file = os.path.join(indir, d, spec + "-cds.fa");
    aa_out_file = os.path.join(indir, d, spec + "-aa.fa");
    out_files = [nt_out_file, cds_out_file, aa_out_file];

    nt_longest_out_file = os.path.join(indir, d, spec + "-nt-longest.fa");
    cds_longest_out_file = os.path.join(indir, d, spec + "-cds-longest.fa");
    aa_longest_out_file = os.path.join(indir, d, spec + "-aa-longest.fa");
    out_longest_files = [nt_longest_out_file, cds_longest_out_file, aa_longest_out_file];
    # Get the current output files

    ####################

    gid_to_tid = defaultdict(list);
    tid_to_gid = {};
    # Dicts to associate ids in the isoform file

    first = True;
    for line in open(isoform_file):
        if first:
            first = False;
            continue;
        
        gid, tid = line.strip().split("\t");
        gid_to_tid[gid].append(tid);
        assert tid not in tid_to_gid, "\nduplicate tid: " + tid;
        tid_to_gid[tid] = gid;
    # Read the ids in the isoform file

    ####################

    for i in range(len(in_files)):

        cds_skipped = [];
        # The number of CDS sequences not divisible by 3

        with open(out_files[i], "w") as outfile, open(out_longest_files[i], "w") as outfilelongest:

            print(" > " + in_files[i]);
            seqs = SEQ.fastaReadSeqs(in_files[i]);
            print( " > " + str(len(seqs)) + " seqs read");
            # Read the input sequences for the current file

            query_seqs = {};
            # The sequences with transcript ID as the key

            found = set();
            # A set of transcript IDs read to make sure they are all unique

            for seq in seqs:
                if any(ref_str in seq for ref_str in ["REFERENCE", "ref_"]):
                    continue;
                # Skip reference sequences

                # if i == 0:
                #     seq_len = len(seqs[seq].replace(" ", ""));
                #     assert seq_len % 3 == 0, "\nnot div 3: " + seq + " " + str(seq_len) + "\n" + seqs[seq] + "\n\n"

                raw_seq = seqs[seq].replace(" ", "").replace("X", "").replace("-", "");
                # Remove any alignment characters from the sequence
                
                seq_id = seq.split(" | ")[0];
                if seq_id in found:
                    print("dup id: " + seq_id);
                    continue;
                found.add(seq_id);
                # Parse out just the transcript ID as the new header and check for duplicate IDs

                if i == 1:
                    raw_seq_len = len(raw_seq);
                    if not raw_seq_len % 3 == 0:
                        #print("parsed not div 3: " + seq + " " + str(len(seqs[seq])) + " " + str(raw_seq_len));
                        cds_skipped.append(seq_id);
                        continue;
                    #assert raw_seq_len % 3 == 0, "parsed not div 3: " + seq + " " + str(len(seqs[seq])) + " " + str(raw_seq_len) + "\n" + seqs[seq] + "\n\n" + raw_seq;
                # For CDS sequences, check if divisible by 3

                outfile.write(">" + seq_id + "\n");
                outfile.write(raw_seq + "\n");
                # Write the unaligned sequence to the output file

                query_seqs[seq_id] = raw_seq;
                # Save the sequence in the query seq dict with transcript id as the key
            ## End first seq loop

            if i == 1:
                print(" > " + str(len(cds_skipped)) + " CDS seqs not divisible by 3");
            print(" > " + str(len(query_seqs)) + " seqs retained (expected " + str(((len(seqs)) / 2) - len(cds_skipped)) + ")");

            ####################

            longest_written = 0;
            genes_no_tid = [];
            for gid in gid_to_tid:
                max_tid = "";
                max_tid_len = 0;
                # Set initial values for longest transcript length and id

                for tid in gid_to_tid[gid]:
                    if tid in cds_skipped:
                        continue;
                    # Skip CDS sequences not divisible by 3

                    tid_len = len(query_seqs[tid]);
                    if tid_len > max_tid_len:
                        max_tid = tid;
                        max_tid_len = tid_len;
                # For every transcript isoform of this gene id, check the length and compare to current longest

                #assert max_tid_len != 0, "\nno tid found: " + gid + " " + max_tid + " " + str(gid_to_tid[tid]);
                if not max_tid:
                    genes_no_tid.append(gid);
                    continue;
                # Make sure each gene has a transcript ID

                outfilelongest.write(">" + max_tid + "\n");
                outfilelongest.write(query_seqs[max_tid] + "\n");
                longest_written += 1;
                # Write out the longest transcript found
            ## End longest transcript loop

            if genes_no_tid:
                print(" > " + str(len(genes_no_tid)) + " genes with no transcript");
            print(" > " + str(longest_written) + " longest transcripts written");

            ####################
        ## Close current output file

    ## End input seq loop
## End species loop


# Dmawii
# 0
# 31
# 0
# Cinsculpta
# 0
# 68
# 0
# Cmccordi
# 0
# 9
# 0
# Pexpansa
# 0
# 42
# 0
# Amarmorata
# 0
# 49
# 0
# Mtuberculata
# 0
# 22
# 0
# Rswinhoei
# 0
# 104
# 0
# Esubglobosa
# 0
# 64
# 0