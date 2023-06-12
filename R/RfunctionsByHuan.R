#Function list
#tree_scaler

tree_scaler <- function (treefile, scale){
    library(ape)
    original_tree<-read.tree(treefile)
    new_tree<-original_tree
    new_tree$edge.length <- original_tree$edge.length*scale
    write.tree(new_tree,file=paste0(scale,treefile))##
}

##################### Metagenomics ############### 
# kraken and bracken
##################################################
read_kraken <- function(file){
    Sample <- strsplit(strsplit(file,'/')[[1]][3],'\\.')[[1]][1]
    design <- strsplit(Sample,'-')[[1]][1]
    df <- read_delim(file, "\t", escape_double = FALSE, col_names = c("percentage_all","read_number_all","read_number_level","level","taxID","name"), trim_ws = TRUE)
    df$sample <- Sample
    df$Type <- design
    return(df)
}

read_bracken <- function(files, level, col2read = 'fraction_total_reads'){
    sample1 <- strsplit(files[1],'\\.')[[1]][1]
    data <- data.frame(read_delim(files[1], "\t", escape_double = FALSE, trim_ws = TRUE))
    data <- data %>% filter(taxonomy_lvl ==level)
    data <- data[,c(col2read, 'name')]
    #data$fraction_total_reads <- as.numeric(data$fraction_total_reads)
    colnames(data) <- c(sample1, level)
    for (file in files[2:length(files)]) {
        sample <- strsplit(file,'\\.')[[1]][1]
        data_new <- data.frame(read_delim(file, "\t", escape_double = FALSE, trim_ws = TRUE))
        data_new <- data_new %>% filter(taxonomy_lvl == level)
        data_new <- data_new[,c(col2read, 'name')]
        colnames(data_new) <- c(sample, level)
        #data_new$Num <- as.numeric(data_new$Num)
        data <- merge(data, data_new, by=level, all=TRUE)
    }
    
    data[is.na(data)] <- 0  
    return(data)
}

