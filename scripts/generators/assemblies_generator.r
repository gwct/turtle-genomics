############################################################
# For turtles web, 07.21
# This generates the file "assemblies.html"
############################################################


cat("Rendering assemblies.rmd/html\n")
Sys.setenv(RSTUDIO_PANDOC="C:/Program Files/RStudio/bin/pandoc/")
library(rmarkdown)
setwd("C:/bin/turtle-genomics/scripts/generators/")
output_dir = "../.."
render("../markdown/assemblies.rmd", output_dir = output_dir, params = list(output_dir = output_dir), quiet = TRUE)