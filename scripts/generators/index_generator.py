############################################################
# For personal site, 03.20
# This generates the file "index.html"
############################################################

import sys, os
sys.path.append('..')
import lib.read_chunks as RC

######################
# HTML template
######################

html_template = """
<!doctype html>
    {head}

<body>
	<div class="row" id="top_grid">
		<div class="col-2-24" id="margin"></div>
		<div class="col-20-24" id="main_header">Turtle genomics</div>
		<div class="col-2-24" id="margin"></div>
	</div>

	{nav}

	<div class="row">
		<div class="col-2-24" id="margin"></div>
		<div class="col-20-24" id="main_col">
            <h2>Sample list</h2>
		</div>
        <div class="col-2-24" id="margin"></div>
	</div>

	<center>
		<div id="table_container">
			<table id="table_content">
				{sample_table}
			</table>
		</div>
	</center>

	<div class="row">
		<div class="col-2-24" id="margin"></div>
		<div class="col-12-24">
			<span><em>Note: Last 3 rows are alternates</em></span>
		</div>
		<div class="col-10-24" id="margin"></div>
	</div>

	<div class="sep_div"></div>

    {footer}
</body>
"""

######################
# Main block
######################
pagefile = "index.html";
print("Generating " + pagefile + "...");
title = "Turtle genomics"

head = RC.readHead(title, pagefile);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

samples_file = "../../data/turtles.csv";

sample_table = "";
first = True;
for line in open(samples_file):
	if line.startswith("#"):
		continue;

	line = line.strip().split(",");

	if first:
		sample_table += "<thead>";
		sample_table += "<th>Family</th>";
		sample_table += "<th>Species</th>";
		sample_table += "<th>Assembly</th>";
		sample_table += "<th>Coverage</th>";
		sample_table += "<th>Scaffolds</th>";
		sample_table += "<th>Scaffold N50</th>";
		sample_table += "<th>Annotated</th>";
		sample_table += "<th>Notes</th>";
		sample_table += "</thead>";

		first = False;
		continue;

	sample_table += "<tr>";
	sample_table += "<td>" + line[0] + "</td>";
	sample_table += "<td><em>" + line[1] + " " + line[2] + "</em></td>";
	sample_table += "<td><a href='" + line[7] + "' target='_blank'>" + line[6] + "</a></td>";
	sample_table += "<td>" + line[8] + "X</td>";
	sample_table += "<td>" + line[13] + "</td>";
	sample_table += "<td>" + line[14] + "</td>";
	sample_table += "<td>" + line[15] + "</td>";
	sample_table += "<td>" + line[17] + "</td>";
	sample_table += "</tr>";

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, sample_table=sample_table, footer=footer));