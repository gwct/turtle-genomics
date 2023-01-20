############################################################
# For turtles web, 01.23
# This generates the file "windows.html"
############################################################


cat("Rendering windows.rmd/html\n")
Sys.setenv(RSTUDIO_PANDOC="C:/Program Files/RStudio/bin/pandoc/")
library(rmarkdown)
library(here)
setwd(here("docs", "scripts", "generators"))
print(getwd())
output_dir = "../.."
render("../markdown/windows.rmd", output_dir = output_dir, params = list(output_dir = output_dir), quiet = TRUE)