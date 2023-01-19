############################################################
# For personal site, 03.20
# This generates the file "index.html"
############################################################

import sys, os
sys.path.append(os.path.abspath('../lib/'))
import read_chunks as RC

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

	<div class="sep_div"></div>

	<div class="row">
		<div class="col-2-24" id="margin"></div>
		<div class="col-20-24" id="main_col">
            <h2>The team:</h2>
			<ul>
				<li>LaDeana Hillier</li>
				<li>Patrick Minx</li>
				<li><a href="https://www.wtamu.edu/academics/college-agriculture-natural-sciences/department-life-earth-environmental-sciences/faculty/Peter-Scott-bio.html" target="_blank">Peter Scott</a></li>
				<li>Andrew Shedlock</li>
				<li><a href="https://sites.lifesci.ucla.edu/eeb-shafferlab/" target="_blank">Brad Shaffer</a></li>
				<li><a href="https://gwct.github.io/" target="_blank">Gregg Thomas</a></li>
			</ul>
		</div>
        <div class="col-2-24" id="margin"></div>
	</div>

	<div class="sep_div"></div>

    {footer}
</body>
"""

######################
# Main block
######################
pagefile = "people.html";
print("Generating " + pagefile + "...");
title = "Turtle genomics - links"

head = RC.readHead(title, pagefile);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));