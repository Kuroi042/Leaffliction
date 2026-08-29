library(Rcpp)

Sys.setenv(
    PKG_CXXFLAGS = paste0(system("pkg-config --cflags opencv5", intern = TRUE))
)
Sys.setenv(
    PKG_LIBS = paste0(system("pkg-config --libs opencv5", intern = TRUE))
)


args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) {
    stop("error in arguments")
}
input_path <- args[1]

dir_list <- list.dirs(path = input_path, recursive = FALSE)


file_list <- list()
class_name <- basename(dirname(input_path))
file_list[[class_name]] <- input_path
max_len <- lengths(file_list)
target <- max(max_len)
datatoplot <- data.frame(
    classnames = names(file_list),
    count = max_len,
    stringsAsFactors = FALSE
)
rownames(datatoplot) <- NULL
print(datatoplot)
print(max_len)


sourceCpp("transformain.cpp")

cppmaintranform()
