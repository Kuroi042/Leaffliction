library(ggplot2)
library(patchwork)


args = commandArgs(trailingOnly=TRUE)

# length(args)


if(length(args) != 1)
{
    stop("error in arguments")
}

extract_data <- function(args)
{
dir_list <- list.dirs(path = args ,recursive = FALSE)


file_list <- list()

for( i in dir_list)
{
    print( basename(i) )
    folder_name <- basename(i)
    files <- list.files(path = i)
    file_list[[folder_name]] <- files
    cat( "in the folder ", i ," found ", length(files) , "\n")

}

    max_len <- max(lengths(file_list))
    file_list <- sapply(file_list, `length<-`, max_len)

    return(as.data.frame(file_list))
}
data <- extract_data(args)


total <- sum(colSums(!is.na(data)))

# stop(total)

datatoplot <- data.frame(classnames = colnames(data) , count = colSums(!is.na(data)) , percent = round((colSums(!is.na(data))/total) *100,digits = 2)  ,stringsAsFactors = FALSE)
rownames(datatoplot) <- NULL

# datatoplot$classnames <- 


# datatoplot$count <- colSums(!is.na(data))

print(datatoplot)



# print(colSums(!is.na(data)))

p1 <- ggplot(datatoplot, aes( x = classnames ,y = count , fill = classnames )) + geom_col()

ggsave("distribution.png")


p2 <- ggplot(datatoplot, aes( x="" ,y = percent , fill = classnames )) + geom_bar(stat="identity", width=1, color="white") +
  coord_polar("y", start=0)+ theme_light() + geom_text(aes(label = paste0(percent,"%")), position = position_stack(vjust = 0.5))
ggsave("pie.png")

combined <- p1 | p2

ggsave(paste0(basename(args),"_combined.png"), plot = combined, width = 12, height = 6)
