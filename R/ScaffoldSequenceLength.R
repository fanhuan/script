library(rvest)
library(stringr)
library(dplyr)
seqlength=0
seqID=NULL
for (num in (777837:794156)) {
    url = paste("http://www.ebi.ac.uk/ena/data/view/LN", num, "&display=xml", sep = "")
    x = readLines(url)
    xx = grep("sequenceLength", x, value = T)
    y = as.integer(str_replace(xx, "^.*sequenceLength=\\\"([0-9]*).*$", "\\1"))
    if (y>seqlength) {
        seqlength <- y
        seqID<-num
        print(seqID)
        print(seqlength)
    }
}
num = 776248

x = readLines(url)
xx = grep("sequenceLength", x, value = T)
xx
y = str_replace(xx, "^.*sequenceLength=\\\"([0-9]*).*$", "\\1")
str_replace(xx, "^.*accession=\\\"([A-Z0-9]*).*$", "\\1")
