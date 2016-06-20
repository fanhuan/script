#Function list
#tree_scaler

tree_scaler <- function (treefile, scale){
    library(ape)
    original_tree<-read.tree(treefile)
    new_tree<-original_tree
    new_tree$edge.length <- original_tree$edge.length*scale
    write.tree(new_tree,file=paste0(scale,treefile))##
}

