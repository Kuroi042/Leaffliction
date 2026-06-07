library(Rcpp)
# install.packages("microbenchmark")
library(microbenchmark)

# Compile the C++ file (this creates the R function dynamically)
sourceCpp("test.cpp")

totot("hh wa hadchi fchkl" ,  102)