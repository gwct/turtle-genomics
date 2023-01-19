#!/usr/bin/python
############################################################
# For turtles genomes, 01.2023
# Build a table of windows and assess filters (e.g. missing
# data, repeats) from a whole genome alignment of multiple
# species
############################################################

import sys, os, argparse, core, seqparse as SEQ

############################################################

def isPosFloat(x, x_min=0.0, x_max=1.0):
    try:
        x = float(x);
    except:
        return False;

    if x < x_min or x > x_max:
        return False;
    else:
        return True;

#########################

def countNongapLength(seqs, missing_filter, repeat_filter):
# This function goes through every sequence in an alignment and calculates
# the average length of each sequence excluding gaps/missing data and counts
# how many seqs above filter thresholds.

    missing_chars = "-NnXx";
    repeat_chars = "atcgnx";
    # Strings of missing and repeat/softmask characters

    len_sum, num_seqs, num_missing_seqs, num_repeat_seqs = 0, 0, 0, 0;
    for seq in seqs:
        num_seqs += 1;
        full_len = len(seqs[seq]);

        no_missing_len = len( [ site for site in seqs[seq] if site not in missing_chars ] );
        len_sum += no_missing_len;

        if 1 - (no_missing_len / full_len) > missing_filter:
            num_missing_seqs += 1;
        # If the number of gaps in the sequence (calculated as 1 - the fraction of non-gap length to full length)
        # is above some threshold, mark it as gappy

        no_repeat_len = len( [ site for site in seqs[seq] if site not in repeat_chars ] );

        if 1 - (no_repeat_len / full_len) > repeat_filter:
            num_repeat_seqs += 1;
        # If the number of repeat chars in the sequence (calculated as 1 - the fraction of non-repeat length to full length)
        # is above some threshold, mark it as a repeat seq

    return len_sum / num_seqs, num_missing_seqs, num_repeat_seqs;

#########################

def countUniqIdentSeqs(seqs):
# This function goes through every sequence in an alignment and counts how 
# many sequences are unique or identical.

    uniq_seqs, ident_seqs, found = 0, 0, [];
    seq_list_raw = list(seqs.values());
    seq_list = [ seq.replace("-", "") for seq in seq_list_raw ];
    for seq in seq_list:
        if seq_list.count(seq) == 1:
            uniq_seqs += 1;
        if seq_list.count(seq) != 1 and seq not in found:
            ident_seqs += 1;
            found.append(seq);

    return uniq_seqs, ident_seqs;

#########################

def siteCount(seqs, aln_len, missing_filter):
# This function goes through every site in an alignment to check for invariant sites, gappy sites, 
# and stop codons.

    missing_chars = "-NnXx";

    invar_sites, sites_w_missing, high_missing_sites, all_missing_sites = 0, 0, 0, 0;
    informative_sites = 0;
    # Counts

    seq_list = list(seqs.values());
    num_spec = len(seq_list);

    for i in range(aln_len):
    # Loop over every site

        site = [];
        for j in range(num_spec):
            site.append(seq_list[j][i]);
        # Get the current (ith) site from every sequence (j)

        if site.count(site[0]) == len(site):
            invar_sites += 1;
        # If all the nts at the site match the first one, it is invariant

        num_missing = len([ allele for allele in site if allele in missing_chars ]);
        # Count the number of gaps at the current site

        allele_counts = { allele : site.count(allele) for allele in site if allele not in missing_chars };
        # Count the occurrence of each allele in the site

        if len(allele_counts) > 1:
            multi_allele_counts = [ allele for allele in allele_counts if allele_counts[allele] >= 2 ];
            # Count the number of alleles present in at least 2 species

            if len(multi_allele_counts) >= 2:
                informative_sites += 1;
            # If 2 or more alleles are present in 2 or more species, this site is informative

        if num_missing > 1:
            sites_w_missing += 1;
            # Increment by one if there is at least one gap

            if (num_missing / len(site)) > missing_filter:
                high_missing_sites += 1;
            # Count if the number of gaps at this site is above some threshold

        perc_sites_w_missing = sites_w_missing / aln_len;
        if sites_w_missing == len(site):
            all_missing_sites += 1;
    ## End site loop

    return invar_sites, informative_sites, sites_w_missing, perc_sites_w_missing, high_missing_sites, all_missing_sites;

############################################################

parser = argparse.ArgumentParser(description="Get rodent chromosome window coordinates");
parser.add_argument("-i", dest="indir", help="The input directory, containing subdirectories for each reference scaffold that contain window alignments.", default=False);
parser.add_argument("-w", dest="window_size", help="The size of the sliding window in kb.", type=int, default=False);
parser.add_argument("-r", dest="repeat_thresh", help="Windows that have a proportion of their sequence overlapping with repeats greater than this will be excluded. Default: 0.5", type=float, default=0.5);
parser.add_argument("-m", dest="missing_thresh", help="Windows that have a proportion of their sequence that is missing data (Ns) greater than this will be excluded. Default: 0.5", type=float, default=0.5);
parser.add_argument("-o", dest="outfile", help="A file to output the csv values and log info to.", default="get-windows-default.csv");
parser.add_argument("--overwrite", dest="overwrite", help="A file to output the csv values and log info to.", action="store_true", default=False);
# parser.add_argument("-p", dest="procs", help="The number of processes the script should use. Default: 1.", type=int, default=1);
args = parser.parse_args();

#########################

if not os.path.isdir(args.indir):
    sys.exit(" * Error 1: Input directory (-i) not found.");
else:
    indir = os.path.abspath(args.indir);

#####

if not args.window_size:
    sys.exit(" * Error 2: Window size in kb (-w) must be defined.");
if args.window_size < 1:
    sys.exit(" * Error 3: Window size in kb (-w) must be a positive integer.");
else:
    wsize_str = str(args.window_size);

#####

if not isPosFloat(args.repeat_thresh):
    sys.exit(" * Error 4: Repeat threshold (-r) must be a value between 0 and 1.");

if not isPosFloat(args.missing_thresh):
    sys.exit(" * Error 5: Missing data threshold (-m) must be a value between 0 and 1.");

#####

outfilename = os.path.abspath(args.outfile);

if os.path.isfile(outfilename) and not args.overwrite:
    sys.exit(" * Error 6: Output file already exists. Please move the current file or specify to --overwrite it.");

#########################

headers = [ "window", "scaffold", "start", "end", "aln.len", "seqs.above.repeat", "seqs.above.missing", "avg.seq.len.wo.missing", "uniq.seqs", "ident.seqs", "invariant.sites", "informative.sites", "sites.w.missing" "percent.sites.with.missing", "sites.high.missing", "sites.all.missing" ];

#########################

pad = 40;
header_pad = 40;
with open(outfilename, "w") as outfile:
    core.runTime(writeout=outfile);
    core.PWS(core.spacedOut("# Window size (-w):", pad) + wsize_str + "kb", outfile);
    core.PWS(core.spacedOut("# Input directory:", pad) + indir, outfile);
    core.PWS(core.spacedOut("# Repeat threshold:", pad) + str(args.repeat_thresh), outfile);
    core.PWS(core.spacedOut("# Missing data threshold:", pad) + str(args.missing_thresh), outfile);
    core.PWS(core.spacedOut("# Output file:", pad) + outfilename, outfile);
    core.PWS("# ----------------", outfile);
    # Run time info for logging.
    ###################

    outfile.write("# HEADER INFO:\n");
    outfile.write(core.spacedOut("# window:", header_pad) + "Unique window ID (scaffold:start-end)\n");
    outfile.write(core.spacedOut("# scaffold:", header_pad) + "Scaffold ID of window\n");
    outfile.write(core.spacedOut("# start:", header_pad) + "The start coordinate of the window (0-based)\n");
    outfile.write(core.spacedOut("# end:", header_pad) + "The end coordinate of the window\n");
    outfile.write(core.spacedOut("# aln.len:", header_pad) + "The length of the alignment, including indels\n");
    outfile.write(core.spacedOut("# seqs.above.repeat:", header_pad) + "The number of sequences in the alignment with a percentage of sites above the specified repeat threshold (-r)\n");
    outfile.write(core.spacedOut("# seqs.above.missing:", header_pad) + "The number of sequences in the alignment with a percentage of sites above the specified missing data threshold (-m)\n");
    outfile.write(core.spacedOut("# avg.seq.len.wo.missing:", header_pad) + "The average length of all sequences in the alignment while excluding gaps or missing data (-, X, N)\n");
    outfile.write(core.spacedOut("# uniq.seqs:", header_pad) + "The number of unique sequences in the alignment\n");
    outfile.write(core.spacedOut("# ident.seqs:", header_pad) + "The number of identical sequences in the alignment\n");
    outfile.write(core.spacedOut("# invariant.sites:", header_pad) + "The number of sites in the alignment with only 1 allele\n");
    outfile.write(core.spacedOut("# informative.sites:", header_pad) + "The number of sites in the alignment that have at least 2 alleles that are present in 2 species\n");
    outfile.write(core.spacedOut("# sites.w.missing:", header_pad) + "The number of sites in the alignment with at least one missing data character (-, X, N)\n");
    outfile.write(core.spacedOut("# percent.sites.with.missing:", header_pad) + "The percent of sites in the alignment with at least one missing data character (-, X, N)\n");
    outfile.write(core.spacedOut("# sites.high.missing:", header_pad) + "The number of sites in the alignment that are made up of a high percentage of missing data characters (over -m)\n");
    outfile.write(core.spacedOut("# sites.all.missing:", header_pad) + "The number of sites in the alignment that are made up of all missing data characters\n");
    outfile.write("# ----------------\n");

    outfile.write(",".join(headers) + "\n");

    # Header info
    ###################

    scaff_dirs = [ os.path.join(indir, d) for d in os.listdir(indir) ];
    # Get the list of all scaffold directories to loop over
    
    num_scaffs = len(scaff_dirs);
    cur_scaff_num = 1;
    # Counting for status updates

    for scaff_dir in scaff_dirs:
        scaff_dir_base = os.path.basename(scaff_dir);
        print("# " + core.getDateTime() + " | " + str(cur_scaff_num) + " / " + str(num_scaffs) + " - " + scaff_dir_base);
        # Status update

        scaff_aln_files = os.listdir(scaff_dir);
        # Get the list of all alignments for the current scaffold

        num_alns = len(scaff_aln_files);
        cur_aln_num = 1;
        # Counting for status updates

        for scaff_aln_file in scaff_aln_files:
            print("# " + core.getDateTime() + " | " + str(cur_scaff_num) + " / " + str(num_scaffs) + " - " + scaff_dir_base + " > " + str(cur_aln_num) + " / " + str(num_alns) + " - " + scaff_aln_file);
            # Status update

            file_base = os.path.splitext(scaff_aln_file)[0];
            file_list = file_base.split(":");
            scaff = file_list[0]
            start, end = file_list[1].split("-");
            # Parse the window info out of the alignment file name

            cur_outline = [file_base, scaff, start, end];
            # Add the window info to the output list

            cur_aln_raw = SEQ.fastaReadSeqs(os.path.join(scaff_dir, scaff_aln_file));
            cur_aln = { header : cur_aln_raw[header] for header in cur_aln_raw if "Anc" not in header };
            aln_len = len(cur_aln[list(cur_aln.keys())[0]]);
            # Read the alignment and remove ancestral sequences

            avg_no_missing_len, num_missing, num_repeat = countNongapLength(cur_aln, args.missing_thresh, args.repeat_thresh);
            num_uniq, num_ident = countUniqIdentSeqs(cur_aln);
            # Count aln stats by sequence

            invariant_sites, informative_sites, sites_w_missing, perc_sites_w_missing, high_missing_sites, all_missing_sites = siteCount(cur_aln, aln_len, args.missing_thresh);
            # Count aln stats by site

            cur_outline += [ aln_len, num_repeat, num_missing, avg_no_missing_len, num_uniq, num_ident, invariant_sites, informative_sites, sites_w_missing, perc_sites_w_missing, high_missing_sites, all_missing_sites ];
            cur_outline_str = [ str(col) for col in cur_outline ];
            outfile.write(",".join(cur_outline_str) + "\n");            
            # Add stats to output list, convert all entries to strings, and write to file

            cur_aln_num += 1;
            # Increment aln counter
        ## End aln loop

        cur_scaff_num += 1;
        # Increment scaffold counter
    ## End scaff loop
## Close output file
        