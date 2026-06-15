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



dir_list <- list.dirs(path = args ,recursive = FALSE)


file_list <- list()

for( i in dir_list)
{
    folder_name <- basename(i)
    files <- list.files(path = i, full.names = TRUE) #, full.names = TRUE bach i3ti absolute path
    file_list[[folder_name]] <- files
    
}
sourceCpp("test.cpp")

cppmain("courage",file_list)


