library(Rcpp)
library(opencv)


# Sys.setenv(PKG_CXXFLAGS = "-std=c++17") linux
# Sys.setenv(PKG_LIBS = "$(pkg-config --libs opencv4)")
# Sys.setenv(PKG_CPPFLAGS = "$(pkg-config --cflags opencv4)")

Sys.setenv(PKG_CXXFLAGS = "-std=c++17")
Sys.setenv(PKG_CPPFLAGS = "-II:/ratt/opencv/build/include")
Sys.setenv(PKG_LIBS = "-LI:/ratt/opencv/build/x64/vc16/lib -lopencv_world500")


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


