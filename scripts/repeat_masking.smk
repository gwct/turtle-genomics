#############################################################################
# Pipeline for read mapping simulations with varying divergence
#############################################################################

import os
import re

#############################################################################
# Example cmd

# snakemake -p -s repeat_masking.smk --configfile lkemp-rm-cfg.yaml --profile profiles/slurm_profile/ --dryrun

#############################################################################
# Input and output info

spec = config["spec"];

input_dir = config["input_dir"];
batches = os.listdir(input_dir);
batches = batches[1];
print(batches);

repeat_library = config["repeat_library"];

#############################################################################
# Final rule - rule that depends on final expected output file and initiates all
# the other rules

localrules: all

rule all:
    input:
        expand(os.path.join(input_dir, "{batch}", "{batch}.fa.masked"), batch=batches)
        # Expected output from rule repeat_mask

## The final expected outputs should be listed in this rule. Only necessary to list final output from final rule, but I found it useful to list them 
## for all rules for debugging (can comment out outputs for rules you don't want to run), though there's also probably a better way to do this

#############################################################################
# Pipeline rules

rule repeat_mask:
    input:
        os.path.join(input_dir, "{batch}", "{batch}.fa")
    output:
        os.path.join(input_dir, "{batch}", "{batch}.fa.masked")
    params:
        LIB = repeat_library
    log:
        os.path.join("logs", "spec-{batch}-repeat-masking.log")
    shell:
        """
        singularity exec /cvmfs/singularity.galaxyproject.org/r/e/repeatmasker:4.1.2.p1--pl5321hdfd78af_1 RepeatMasker -xsmall -pa 8 -gff -q -species chicken {input}
        """
# Run each batch through RepeatMasker
# singularity exec /cvmfs/singularity.galaxyproject.org/r/e/repeatmasker:4.1.2.p1--pl5321hdfd78af_1 RepeatMasker -xsmall -pa 8 -gff -q -lib {params.LIB} {input}