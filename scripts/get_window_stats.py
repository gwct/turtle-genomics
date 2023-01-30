#!/usr/bin/python
############################################################
# For turtles genomes, 01.2023
# Build a table of windows and assess filters (e.g. missing
# data, repeats) from a whole genome alignment of multiple
# species
############################################################

import sys, os, argparse, core, seqparse as SEQ
import multiprocessing as mp

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

def processScaff(scaff_item):

    scaff_dir, cur_scaff_num, num_scaffs = scaff_item;
    scaff_outlines = [];

    scaff_dir_base = os.path.basename(scaff_dir);
    #print("# " + core.getDateTime() + " | " + str(cur_scaff_num) + " / " + str(num_scaffs) + " - " + scaff_dir_base);
    # Status update

    scaff_aln_files = os.listdir(scaff_dir);
    # Get the list of all alignments for the current scaffold

    num_alns = len(scaff_aln_files);
    cur_aln_num = 1;
    # Counting for status updates

    for scaff_aln_file in scaff_aln_files:
        print("# " + core.getDateTime() + " | " + scaff_dir_base + " > " + str(cur_aln_num) + " / " + str(num_alns) + " - " + scaff_aln_file);
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

        avg_no_missing_len, num_missing, num_repeat, num_gappy = countNonMissingLength(cur_aln, args.missing_thresh, args.gap_thresh);
        num_uniq, num_ident = countUniqIdentSeqs(cur_aln);
        # Count aln stats by sequence

        invariant_sites, informative_sites, sites_w_missing, perc_sites_w_missing, high_missing_sites, all_missing_sites, sites_w_gap, perc_sites_w_gap, high_gap_sites, all_gap_sites = siteCount(cur_aln, aln_len, args.missing_thresh, args.gap_thresh);
        # Count aln stats by site

        filtered_aln, gappy_cols = windowSiteFilter(cur_aln, aln_len, args.gap_thresh);
        filtered_aln_len = len(cur_aln[list(filtered_aln.keys())[0]]);

        cur_outline += [ aln_len, num_missing, avg_no_missing_len, num_gappy, gappy_cols, num_uniq, num_ident, invariant_sites, informative_sites, sites_w_missing, perc_sites_w_missing, high_missing_sites, all_missing_sites, sites_w_gap, perc_sites_w_gap, high_gap_sites, all_gap_sites ];

        ###################

        avg_no_missing_len_f, num_missing_f, num_repeat_f, num_gappy_f = countNonMissingLength(filtered_aln, args.missing_thresh, args.gap_thresh);
        num_uniq_f, num_ident_f = countUniqIdentSeqs(filtered_aln);
        # Count aln stats by sequence

        invariant_sites_f, informative_sites_f, sites_w_missing_f, perc_sites_w_missing_f, high_missing_sites_f, all_missing_sites_f, sites_w_gap_f, perc_sites_w_gap_f, high_gap_sites_f, all_gap_sites_f = siteCount(filtered_aln, filtered_aln_len, args.missing_thresh, args.gap_thresh);
        # Count aln stats by site

        cur_outline += [ filtered_aln_len, num_missing_f, avg_no_missing_len_f, num_gappy_f, num_uniq_f, num_ident_f, invariant_sites_f, informative_sites_f, sites_w_missing_f, perc_sites_w_missing_f, high_missing_sites_f, all_missing_sites_f, sites_w_gap_f, perc_sites_w_gap_f, high_gap_sites_f, all_gap_sites_f ];
        
        ###################

        cur_outline_str = [ str(col) for col in cur_outline ];
        scaff_outlines.append(cur_outline_str);          
        # Add stats to output list, convert all entries to strings, and write to file

        cur_aln_num += 1;
        # Increment aln counter
    ## End aln loop


    return scaff_outlines;

#########################

def countNonMissingLength(seqs, missing_filter, gap_filter):
# This function goes through every sequence in an alignment and calculates
# the average length of each sequence excluding gaps/missing data and counts
# how many seqs above filter thresholds.

    repeat_filter = 0.5;

    gap_chars = "-";
    missing_chars = "NnXx";
    repeat_chars = "atcgnx";
    # Strings of missing and repeat/softmask characters

    len_sum, num_seqs, num_missing_seqs, num_repeat_seqs, num_gappy_seqs = 0, 0, 0, 0, 0;
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

        no_gap_len = len( [ site for site in seqs[seq] if site not in gap_chars ] );

        if 1 - (no_gap_len / full_len) > gap_filter:
            num_gappy_seqs += 1;
        # If the number of repeat chars in the sequence (calculated as 1 - the fraction of non-repeat length to full length)
        # is above some threshold, mark it as a repeat seq

    return len_sum / num_seqs, num_missing_seqs, num_repeat_seqs, num_gappy_seqs;

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

def siteCount(seqs, aln_len, missing_filter, gap_filter):
# This function goes through every site in an alignment to check for invariant sites, gappy sites, 
# and stop codons.

    gap_chars = "-";
    missing_chars = "NnXx";

    invar_sites, sites_w_missing, high_missing_sites, all_missing_sites, sites_w_gap, high_gap_sites, all_gap_sites = 0, 0, 0, 0, 0, 0, 0;
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

        num_gaps = len([ allele for allele in site if allele in gap_chars ]);

        allele_counts = { allele : site.count(allele) for allele in site if allele not in missing_chars+gap_chars };
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

            if num_missing == len(site):
                all_missing_sites += 1;
            # Check if the site is all missing

        #####

        if num_gaps > 1:
            sites_w_gap += 1;
            # Increment by one if there is at least one gap

            if (num_gaps / len(site)) > gap_filter:
                high_gap_sites += 1;
            # Count if the number of gaps at this site is above some threshold

            if num_gaps == len(site):
                all_gap_sites += 1;
            # Check if the site is all gaps
        #####
    ## End site loop

    perc_sites_w_missing = sites_w_missing / aln_len;
    perc_sites_w_gap = sites_w_gap / aln_len;
    # Calculate the percentage of sites that have at least one missing character or one gap

    return invar_sites, informative_sites, sites_w_missing, perc_sites_w_missing, high_missing_sites, all_missing_sites, sites_w_gap, perc_sites_w_gap, high_gap_sites, all_gap_sites;

#########################

def windowSiteFilter(seqs, aln_len, gap_filter):
# This function takes a sliding window along a codon alignment and filters windows
# where 2 or more codons have 2 or more gaps.

    window_size = 5;
    gappy_window = 3;

    num_seqs = len(seqs);

    exclude_sites = [];
    # The indices of the sites to filter

    i = 0;
    while i < (aln_len - window_size):
    # Loop over every codon in the alignment, stopping at the last possible 3 codon window

        seq_exclude = 0;
        # The number of sequences at the current window that are too gappy

        for seq in seqs:
        # Go over every sequence in the alignment

            cur_window = seqs[seq][i:i+window_size]
            # For every sequence get the current window of <window_size> nucleotides

            if cur_window.count("-") >= gappy_window:
                seq_exclude += 1;
            # If there are <gappy_window> or more positions that are gaps in the window in the current sequence, add to the
            # list of exclude sequences for this window
        ## End seq loop

        if seq_exclude / num_seqs > gap_filter:
            exclude_sites += [pos for pos in range(i, i+window_size)];
        # If the total number of sequences excluded for being gappy at these sites is over some threshold,
        # add all <window_size> sites to the list of excluded sites for this alignment

        i += 1;
    ## End site loop

    exclude_sites_sorted = sorted(list(set(exclude_sites)), reverse=True);
    # Reverse sort the excluded sites to remove with del()

    for seq in seqs:
        seqs[seq] = list(seqs[seq]);
        for site in exclude_sites_sorted:
            del(seqs[seq][site]);
        seqs[seq] = "".join(seqs[seq]);
    #     seqs_filtered = { seq : i for seq,i in seqs.items() }
    #    seqs[seq] = [ seqs[seq][i] for i in range(aln_len) if i not in exclude_sites ];
    # From every sequence, remove the sites from windows determined to be gappy in too many sequences above

    return seqs, len(exclude_sites_sorted);
    #return codon_seqs, len(list(set(exclude_sites)));

############################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Get rodent chromosome window coordinates");
    parser.add_argument("-i", dest="indir", help="The input directory, containing subdirectories for each reference scaffold that contain window alignments.", default=False);
    parser.add_argument("-w", dest="window_size", help="The size of the sliding window in kb.", type=int, default=False);
    parser.add_argument("-g", dest="gap_thresh", help="In sliding windows of 5 columns, if the proportion of sequences that have 3 or more gaps is greater than this threshold, remove all 5 columns of the alignment from every sequence. Default: 0.5", type=float, default=0.5);
    parser.add_argument("-m", dest="missing_thresh", help="Windows that have a proportion of their sequence that is missing data (Ns) greater than this will be excluded. Default: 0.5", type=float, default=0.5);
    parser.add_argument("-o", dest="outfile", help="A file to output the csv values and log info to.", default="get-windows-default.csv");
    parser.add_argument("-d", dest="outdir", help="If provided, a directory to write the filtered sequences to.", default=False);
    parser.add_argument("-p", dest="procs", help="The number of processes to use. Default: 1", type=int, default=1);
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

    if not isPosFloat(args.gap_thresh):
        sys.exit(" * Error 4: Gap threshold (-g) must be a value between 0 and 1.");

    if not isPosFloat(args.missing_thresh):
        sys.exit(" * Error 5: Missing data threshold (-m) must be a value between 0 and 1.");

    #####

    outfilename = os.path.abspath(args.outfile);

    if os.path.isfile(outfilename) and not args.overwrite:
        sys.exit(" * Error 6: Output file (-o) already exists. Please move the current file or specify to --overwrite it.");

    #####

    if args.outdir:
        if not os.path.isdir(args.outdir):
            os.makedirs(args.outdir);
        elif not args.overwrite:
            sys.exit(" * Error 7: Output directory (-d) already exists. Please move the current directory or specify to --overwrite it.");


    proc_pool = mp.Pool(processes=args.procs);

    #########################

    headers = [ "window", "scaffold", "start", "end", "aln.len", "seqs.above.missing", "avg.seq.len.wo.missing", "seqs.above.gappy", "gappy.cols", "uniq.seqs", "ident.seqs", "invariant.sites", "informative.sites", "sites.w.missing", "percent.sites.w.missing", "sites.high.missing", "sites.all.missing", "sites.w.gap", "percent.sites.w.gap", "sites.high.gap", "sites.all.gap" ];
    headers += ["aln.len.filter", "seqs.above.missing.filter", "avg.seq.len.wo.missing.filter", "seqs.above.gappy.filter", "uniq.seqs.filter", "ident.seqs.filter", "invariant.sites.filter", "informative.sites.filter", "sites.w.missing.filter", "percent.sites.w.missing.filter", "sites.high.missing.filter", "sites.all.missing.filter", "sites.w.gap.filter", "percent.sites.w.gap.filter", "sites.high.gap.filter", "sites.all.gap.filter" ];

    #########################

    pad = 40;
    header_pad = 40;
    with open(outfilename, "w") as outfile, proc_pool as pool:
        core.runTime(writeout=outfile);
        core.PWS("# Window size (-w):\t" + wsize_str + "kb", outfile);
        core.PWS("# Input directory:\t" + indir, outfile);
        core.PWS("# Gap threshold:\t" + str(args.gap_thresh), outfile);
        core.PWS("# Missing data threshold:\t" + str(args.missing_thresh), outfile);
        core.PWS("# Output file:\t" + outfilename, outfile);
        core.PWS("# ----------------", outfile);
        # Run time info for logging.
        ###################

        outfile.write("# HEADER INFO:\n");
        outfile.write("# window:\t" + "Unique window ID (scaffold:start-end)\n");
        outfile.write("# scaffold:\t" + "Scaffold ID of window\n");
        outfile.write("# start:\t" + "The start coordinate of the window (0-based)\n");
        outfile.write("# end:\t" + "The end coordinate of the window\n");
        outfile.write("# aln.len:\t" + "The length of the alignment, including indels\n");
        outfile.write("# seqs.above.missing:\t" + "The number of sequences in the alignment with a percentage of sites above the specified missing data threshold (-m)\n");
        outfile.write("# avg.seq.len.wo.missing:\t" + "The average length of all sequences in the alignment while excluding gaps or missing data (X, N)\n");
        outfile.write("# seqs.above.gappy:\t" + "The number of sequences in the alignment with a percentage of sites above the specified gap threshold (-g)\n");
        outfile.write("# gappy.cols:\t" + "The number of alignment columns that exist in 5 bp windows that have 3 or more gaps in at least -g fraction of sequences in the alignment\n");
        outfile.write("# uniq.seqs:\t" + "The number of unique sequences in the alignment\n");
        outfile.write("# ident.seqs:\t" + "The number of identical sequences in the alignment\n");
        outfile.write("# invariant.sites:\t" + "The number of sites in the alignment with only 1 allele\n");
        outfile.write("# informative.sites:\t" + "The number of sites in the alignment that have at least 2 alleles that are present in 2 species\n");
        outfile.write("# sites.w.missing:\t" + "The number of sites in the alignment with at least one missing data character (X, N)\n");
        outfile.write("# percent.sites.with.missing:\t" + "The percent of sites in the alignment with at least one missing data character (X, N)\n");
        outfile.write("# sites.high.missing:\t" + "The number of sites in the alignment that are made up of a high percentage of missing data characters (over -m)\n");
        outfile.write("# sites.all.missing:\t" + "The number of sites in the alignment that are made up of all missing data characters\n");
        outfile.write("# sites.w.gap:\t" + "The number of sites in the alignment with at least one gap\n");
        outfile.write("# percent.sites.with.gap:\t" + "The percent of sites in the alignment with at least one gap\n");
        outfile.write("# sites.high.gap:\t" + "The number of sites in the alignment that are made up of a high percentage of gaps (over -g)\n");
        outfile.write("# sites.all.gap:\t" + "The number of sites in the alignment that are made up of all gaps\n");
        outfile.write("# .filter:\t" + "Columns with the .filter suffix have the same definition as those defined above, but are counted after the window filter (gappy.cols filter)\n");
        outfile.write("# ----------------\n");

        outfile.write("\t".join(headers) + "\n");

        # Header info
        ###################

        scaff_dirs = [ os.path.join(indir, d) for d in os.listdir(indir) ];
        # Get the list of all scaffold directories to loop over
        
        num_scaffs = len(scaff_dirs);
        cur_scaff_num = 1;
        # Counting for status updates

        for result in pool.imap_unordered(processScaff, ((scaff_dir, cur_scaff_num, num_scaffs) for scaff_dir in scaff_dirs)):
            for outline in result:
                outfile.write("\t".join(outline) + "\n");
            cur_scaff_num += 1;
            # Increment scaffold counter
        ## End scaff loop
    ## Close output file


############################################################