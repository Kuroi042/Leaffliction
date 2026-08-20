library(Rcpp)
# library(opencv)


# check if is a folder do all this , if just a file esecute the fuction directly

Sys.setenv(PKG_CXXFLAGS = paste0(system("pkg-config --cflags opencv5", intern=TRUE)))
Sys.setenv(PKG_LIBS     = paste0(system("pkg-config --libs opencv5",   intern=TRUE)))



args = commandArgs(trailingOnly=TRUE)


if(length(args) != 1)
{
    stop("error in arguments")
}
input_path <- args[1]



dir_list <- list.dirs(path = input_path ,recursive = FALSE)


file_list <- list()

 class_name <- basename(dirname(input_path))
  file_list[[class_name]] <- input_path

# for( i in dir_list)
# {
#     folder_name <- basename(i)
#     files <- list.files(path = i, full.names = TRUE) #, full.names = TRUE bach i3ti absolute path
#     file_list[[folder_name]] <- files
    
    
# }


# hh <- as.data.frame(file_list)

# print(datatoplot)
max_len <- lengths(file_list)
 target <- max(max_len)
datatoplot <- data.frame(classnames = names(file_list) , count = max_len , stringsAsFactors = FALSE)
rownames(datatoplot) <- NULL
print(datatoplot)
print(max_len)
# stop()

sourceCpp("test.cpp")

cppmain(max_len,file_list,target)


