#One simulation
#dependencies
#source("http://bioconductor.org/biocLite.R")
#biocLite("Biostrings")
library(phylosim)
library(ape)
library(Biostrings)
setwd("/Users/Huan/Documents/Project/TBSimulation")

#Enable the "fast and careless mode"
PSIM_FAST <- TRUE

#codon freqs for flanking regions are calculated based on 11 rpoB genes in Mycobacterium genus, stored in rpoB_alignment.fa 
#calculates transitions from the frequency: 61 possible codons, excluding the 3 stop codons
codon.freqs.flanking <- c(0.0017830839599969, 0.0276765640747345, 7.75253895650826e-05, 0.0100007752538957, 
                          0.00217071090782231, 0.017830839599969, 0.00186060934956198, 0.0233351422590899, 0.00139545701217149, 
                          0.0186836188851849, 0.00139545701217149, 0.00565935343825103, 0.00767501356694317, 0.0031010155826033, 
                          0.0128692146678037, 0.000930304674780991, 0.0560508566555547, 0.00248081246608264, 0.013101790836499, 
                          0.00240328707651756, 0.0368245600434142, 0.0013179316226064, 0.0174432126521436, 0.00240328707651756, 
                          0.0269788355686487, 0.0106209783704163, 0.0382975424451508, 0.00248081246608264, 0.0179083649895341, 
                          0.00449647259477479, 0.0512442825025196, 0.000387626947825413, 0.0259710055043027, 0.0031010155826033, 
                          0.0369796108225444, 0.00155050779130165, 0.0133343670051942, 0.00186060934956198, 0.0323280874486394, 
                          0.00317854097216838, 0.0396929994573223, 0.0035661679199938, 0.00922552135824482, 0, 0.000697728506085743, 
                          0.00627955655477169, 0.0421738119234049, 0.000930304674780991, 0.0434142181564462, 0.00465152337390495, 
                          0.0372121869912396, 0.00348864253042872, 0.0255058531669122, 0.00814016590433367, 0.062020311652066, 
                          0.0146522986278006, 0.0747344755407396, 0.0240328707651756, 0.0464377083494845, 0.0035661679199938, 
                          0.0103884022017211)

p.flanking <- GY94(codon.freqs = codon.freqs.flanking)
p.flanking$kappa = 2 #kappa is the transition/transversion rate
summary(p.flanking)

##set up hotspot
#6 codons for serine
#serine.codons <- c("TCT", "TCC", "TCA", "TCG", "AGT", "AGC")

# from Kumar&Jena: The single amino acid mutation at codon 450 (i.e., Ser to Leu [TCG to TTG]) of the rpoB gene is reported to be the most widespread mutation 
# setting up the code frequencies this way means that transitions from TCG (or any other codon) to TTG is high. Since the ancestral codon is TCG, this sets the rate of loss of this codon.
codon.freqs.S450 <- array(1,dim=c(1,61))#why no stop codon
codon.freqs.S450[4] <- 20 #TTG, twenty times higher
codon.freqs.S450 <- codon.freqs.S450/sum(codon.freqs.S450)
p.S450 <- GY94(codon.freqs = codon.freqs.S450, rate.multiplier = 10)
p.S450$kappa = 2

#Plot the transition matrix and equilibrium distribution of the two models
quartz(1)
plot(p.flanking, scale = 0.5)
quartz(2)
plot(p.S450, scale = 0.5)

#construct the root sequence
string="TTGGCAGATTCCCGCCAGAGCAAAACAGCCGCTAGTCCTAGTCCGAGTCGCCCGCAAAGTTCCTCGAATAACTCCGTACCCGGAGCGCCAAACCGGGTCTCCTTCGCTAAGCTGCGCGAACCACTTGAGGTTCCGGGACTCCTTGACGTCCAGACCGATTCGTTCGAGTGGCTGATCGGTTCGCCGCGCTGGCGCGAATCCGCCGCCGAGCGGGGTGATGTCAACCCAGTGGGTGGCCTGGAAGAGGTGCTCTACGAGCTGTCTCCGATCGAGGACTTCTCCGGGTCGATGTCGTTGTCGTTCTCTGACCCTCGTTTCGACGATGTCAAGGCACCCGTCGACGAGTGCAAAGACAAGGACATGACGTACGCGGCTCCACTGTTCGTCACCGCCGAGTTCATCAACAACAACACCGGTGAGATCAAGAGTCAGACGGTGTTCATGGGTGACTTCCCGATGATGACCGAGAAGGGCACGTTCATCATCAACGGGACCGAGCGTGTGGTGGTCAGCCAGCTGGTGCGGTCGCCCGGGGTGTACTTCGACGAGACCATTGACAAGTCCACCGACAAGACGCTGCACAGCGTCAAGGTGATCCCGAGCCGCGGCGCGTGGCTCGAGTTTGACGTCGACAAGCGCGACACCGTCGGCGTGCGCATCGACCGCAAACGCCGGCAACCGGTCACCGTGCTGCTCAAGGCGCTGGGCTGGACCAGCGAGCAGATTGTCGAGCGGTTCGGGTTCTCCGAGATCATGCGATCGACGCTGGAGAAGGACAACACCGTCGGCACCGACGAGGCGCTGTTGGACATCTACCGCAAGCTGCGTCCGGGCGAGCCCCCGACCAAAGAGTCAGCGCAGACGCTGTTGGAAAACTTGTTCTTCAAGGAGAAGCGCTACGACCTGGCCCGCGTCGGTCGCTATAAGGTCAACAAGAAGCTCGGGCTGCATGTCGGCGAGCCCATCACGTCGTCGACGCTGACCGAAGAAGACGTCGTGGCCACCATCGAATATCTGGTCCGCTTGCACGAGGGTCAGACCACGATGACCGTTCCGGGCGGCGTCGAGGTGCCGGTGGAAACCGACGACATCGACCACTTCGGCAACCGCCGCCTGCGTACGGTCGGCGAGCTGATCCAAAACCAGATCCGGGTCGGCATGTCGCGGATGGAGCGGGTGGTCCGGGAGCGGATGACCACCCAGGACGTGGAGGCGATCACACCGCAGACGTTGATCAACATCCGGCCGGTGGTCGCCGCGATCAAGGAGTTCTTCGGCACCAGCCAGCTGAGCCAATTCATGGACCAGAACAACCCGCTGTCGGGGTTGACCCACAAGCGCCGACTGTCGGCGCTGGGGCCCGGCGGTCTGTCACGTGAGCGTGCCGGGCTGGAGGTCCGCGACGTGCACCCGTCGCACTACGGCCGGATGTGCCCGATCGAAACCCCTGAGGGGCCCAACATCGGTCTGATCGGCTCGCTGTCGGTGTACGCGCGGGTCAACCCGTTCGGGTTCATCGAAACGCCGTACCGCAAGGTGGTCGACGGCGTGGTTAGCGACGAGATCGTGTACCTGACCGCCGACGAGGAGGACCGCCACGTGGTGGCACAGGCCAATTCGCCGATCGATGCGGACGGTCGCTTCGTCGAGCCGCGCGTGCTGGTCCGCCGCAAGGCGGGCGAGGTGGAGTACGTGCCCTCGTCTGAGGTGGACTACATGGACGTCTCGCCCCGCCAGATGGTGTCGGTGGCCACCGCGATGATTCCCTTCCTGGAGCACGACGACGCCAACCGTGCCCTCATGGGGGCAAACATGCAGCGCCAGGCGGTGCCGCTGGTCCGTAGCGAGGCCCCGCTGGTGGGCACCGGGATGGAGCTGCGCGCGGCGATCGACGCCGGCGACGTCGTCGTCGCCGAAGAAAGCGGCGTCATCGAGGAGGTGTCGGCCGACTACATCACTGTGATGCACGACAACGGCACCCGGCGTACCTACCGGATGCGCAAGTTTGCCCGGTCCAACCACGGCACTTGCGCCAACCAGTGCCCCATCGTGGACGCGGGCGACCGAGTCGAGGCCGGTCAGGTGATCGCCGACGGTCCCTGTACTGACGACGGCGAGATGGCGCTGGGCAAGAACCTGCTGGTGGCCATCATGCCGTGGGAGGGCCACAACTACGAGGACGCGATCATCCTGTCCAACCGCCTGGTCGAAGAGGACGTGCTCACCTCGATCCACATCGAGGAGCATGAGATCGATGCTCGCGACACCAAGCTGGGTGCGGAGGAGATCACCCGCGACATCCCGAACATCTCCGACGAGGTGCTCGCCGACCTGGATGAGCGGGGCATCGTGCGCATCGGTGCCGAGGTTCGCGACGGGGACATCCTGGTCGGCAAGGTCACCCCGAAGGGTGAGACCGAGCTGACGCCGGAGGAGCGGCTGCTGCGTGCCATCTTCGGTGAGAAGGCCCGCGAGGTGCGCGACACTTCGCTGAAGGTGCCGCACGGCGAATCCGGCAAGGTGATCGGCATTCGGGTGTTTTCCCGCGAGGACGAGGACGAGTTGCCGGCCGGTGTCAACGAGCTGGTGCGTGTGTATGTGGCTCAGAAACGCAAGATCTCCGACGGTGACAAGCTGGCCGGCCGGCACGGCAACAAGGGCGTGATCGGCAAGATCCTGCCGGTTGAGGACATGCCGTTCCTTGCCGACGGCACCCCGGTGGACATTATTTTGAACACCCACGGCGTGCCGCGACGGATGAACATCGGCCAGATTTTGGAGACCCACCTGGGTTGGTGTGCCCACAGCGGCTGGAAGGTCGACGCCGCCAAGGGGGTTCCGGACTGGGCCGCCAGGCTGCCCGACGAACTGCTCGAGGCGCAGCCGAACGCCATTGTGTCGACGCCGGTGTTCGACGGCGCCCAGGAGGCCGAGCTGCAGGGCCTGTTGTCGTGCACGCTGCCCAACCGCGACGGTGACGTGCTGGTCGACGCCGACGGCAAGGCCATGCTCTTCGACGGGCGCAGCGGCGAGCCGTTCCCGTACCCGGTCACGGTTGGCTACATGTACATCATGAAGCTGCACCACCTGGTGGACGACAAGATCCACGCCCGCTCCACCGGGCCGTACTCGATGATCACCCAGCAGCCGCTGGGCGGTAAGGCGCAGTTCGGTGGCCAGCGGTTCGGGGAGATGGAGTGCTGGGCCATGCAGGCCTACGGTGCTGCCTACACCCTGCAGGAGCTGTTGACCATCAAGTCCGATGACACCGTCGGCCGCGTCAAGGTGTACGAGGCGATCGTCAAGGGTGAGAACATCCCGGAGCCGGGCATCCCCGAGTCGTTCAAGGTGCTGCTCAAAGAACTGCAGTCGCTGTGCCTCAACGTCGAGGTGCTATCGAGTGACGGTGCGGCGATCGAACTGCGCGAAGGTGAGGACGAGGACCTGGAGCGGGCCGCGGCCAACCTGGGAATCAATCTGTCCCGCAACGAATCCGCAAGTGTCGAGGATCTTGCG"
rpoB <- CodonSequence(string=string)
substr(rpoB,1348,1350)

attachProcess(rpoB, p.flanking, 1:449) #left hand side
attachProcess(rpoB, p.S450, 450) #susceptive spot
attachProcess(rpoB, p.flanking, 451:1172) #right hand side

#Construct a deletion process proposing deletions with rate 0.00083333 according to a discrete length distribution
d <- DiscreteDeletor(rate = 0.00083333, sizes = c(1, 2, 3, 4, 5, 6, 7), probs = c(0.2, 0.2, 0.2, 
                                                                                  0.1, 0.1, 0.1, 0.1))

#Construct an insertion process proposing insertions with rate 0.25 according to a discrete length distribution
i <- DiscreteInsertor(rate = 0.00083333, sizes = c(1, 2, 3, 4, 5, 6, 7), probs = c(0.2, 0.2, 0.2, 
                                                                                   0.1, 0.1, 0.1, 0.1))

#Set the templete sequence for the insertion process (what to insert)
i$templateSeq <- NucleotideSequence(length = 7, processes = list(list(p.flanking)))

#Attaching the indel processes to the flanking regions.
attachProcess(rpoB,d,1:449)
attachProcess(rpoB,d,451:1172)
attachProcess(rpoB,i,1:449)
attachProcess(rpoB,i,451:1172)

# Sample omegas from a discrete model. Omegas are dN/dS. 1 is neutral. >1 if favored, <1 if deleterious
# Omegas are only useful to measure a general selection process on codon, not specific selection on specific codon. I have just set the omegas to 1, although this could be changed.
omegaVarM0(rpoB, p.flanking, omega = 1, index = c(1:449, 
                                                  451:1172))
omegaVarM0(rpoB, p.S450, omega = 1, index = 450)

setRateMultipliers(rpoB, p.flanking, value = .2, index = c(1:449, 
                                                           451:1172))
setRateMultipliers(rpoB, p.S450, value = .2, index = 450)

# Input tree
serine.codons <- c("TCT", "TCC", "TCA", "TCG", "AGT", "AGC")
phy.base <- read.tree(file = "TBSimulation.nwk")
phy <- phy.base
p <- Ntip(phy) #number of tips/species 

# This can be used to rescale the branch lengths of the tree
# phy$edge.length <- phy$edge.length

# check with a single example
system.time(sim <- Simulate(PhyloSim(root.seq = rpoB, phylo = phy), quiet = T))
alignment.names <- names(sim$alignment[1, ])

# This identifies the location (index) of 450
index <- (1:1172)[alignment.names == 450 & !is.na(alignment.names)]
#plot(sim, aln.xlim=index + c(-13.5, 13.5), num.pages=1)

# This makes a data.frame for 450 containing codons and whether they code for serine 
w <- data.frame(tip = phy$tip.label, codon = NA, serine = T)
selected.codons <- sim$alignment[,index]
for (kk in phy$tip.label) {
    w$codon[w$tip == kk] <- selected.codons[names(selected.codons) == kk]
    w$serine[w$tip == kk] <- is.element(selected.codons[names(selected.codons) == kk], serine.codons)
}
i=102
write.csv(w, file = paste("rpoB_GY84_trait_", i, ".csv", sep = ""))

# Function for simulating and saving alignments. It also saves as a separate file 
#the phenotype (serine or not at 450) and the codons at 450. Only simulations with
#at least 3 serines and 3 non-serines are saved.
k<-9
#generate kmers including S450
kmer<-sim$alignment[,(index-k/3):(index+k/3)]
kmer_list<-NULL #This does not consider possible deletions ('NA' in some codon)
for (x in 1:p) {
    kmers<-paste(kmer[x,],collapse='')
    for (j in 1:(nchar(kmers)-k+1)){
        kmer_list<-c(kmer_list, substr(kmers, j, j+k-1))
    } 
}
names(kmer_list)<-rep(c(1:(nchar(kmers)-k+1)),p)

if((sum(w$serine) >= 3) & (sum(w$serine) <= length(w$serine)-3)){
    saveAlignment(sim, file = paste("rpoB_GY84_", i, ".fas", sep = ""), skip.internal = T) 
        
        #        row.names(w) <- w$tip
        #        z <- binaryPGLMM(serine ~ 1, data=w, phy)
        #        s2 <- z$s2
        #        P.H0.s2 <- z$P.H0.s2
        #        show(c(i, s2, P.H0.s2))
        
        #        include <- TRUE
        #    } else {
        #        show("too little variation")
        #        include <- FALSE
    }
    #    return(include)
}
'''
#Run replicates singly
i <- 1
while(i <= 100) {
    include <- sim.replicate(i)
    if(include == TRUE) i <- i+1
}
'''
#Run aaf_phylosim.py and kmer_pattern.py
#TBSimulation Huan$ aaf_phylosim.py -k 9 -o phylokmer.dat -i rpoB_GY84_102.fas -W
#TBSimulation Huan$ python kmer_pattern.py -i rpoB_GY84_102/phylokmer.dat -o rpoB_GY84_102_
#Load in the shared kmer table
phylokmer <- read.delim("~/Documents/Project/TBSimulation/rpoB_GY84_102/phylokmer.dat", header=FALSE)
colnames(phylokmer)<-c("kmer",sort(phy$tip.label))
#Grep the patterns for kmers invloving S450 (kmer_list)
rc<-NULL
for (kmer in unique(kmer_list)) {
    rc<-c(rc,as.character(reverseComplement(DNAString(kmer))))
}
kmer_list_rc<-c(unique(kmer_list), rc)
S450_kmers<-phylokmer[phylokmer$kmer %in% kmer_list_rc,]

#score ONCE. We need information from simulations, not only the fas output.
C <- as.matrix(vcv(phy))
C <- C/det(C)^(1/p) #some transformation of C to make the determinant = 1, which should make calculations easier
#n <- nr.replicates
n<-1
iC <- solve(C) #inverse of C
ones <- array(1, c(p, 1)) # array of ones for the intercept

#output <- array(0, c(n, 1)) # collects the results for the n patterns
#threshold <- 3 # minimum number of zeros or ones for inclusion of pattern #already taken care of in kmer_pattern.py
#y should be kmer pattern
#X should be the trait
#read in the kmer pattern as Y, and calculate score for each y.
Y <- read.fwf(file='rpoB_GY84_102_kmerPattern.stats', widths=array(1,c(1,p)),header=F)
colnames(Y)<-sort(phy$tip.label)
#read in the trait values
rpoB_GY84_trait_102 <- read.csv("~/Documents/Project/TBSimulation/rpoB_GY84_trait_102.csv")
#sort the dataframe by tip name, get the serine column with Trues and falses and convert it into 0/1(by *1 or +0)
trait<-rpoB_GY84_trait_100[order(rpoB_GY84_trait_100$tip),]$serine
X<-t(t(trait*1))
threshold<-3
#set up dataframe for 
score<-array(0, c(nrow(Y), 1))
pattern<-array(NA,c(nrow(Y),1))
output<-data.frame(pattern,score)
for (i in 1:nrow(Y)) {
    y<-Y[i,]
    output$pattern[i]<-paste(y,collapse='')
    sumy <- sum(y)#sum of the pattern
    if (sumy < threshold | sumy > (p - threshold)) {
        output$score[i] <- 0 #all patterns with only 1 one or zero are assigned score 0.
    } else {
        xx <- cbind(ones, X)
        
        XiCX <- t(xx) %*% iC %*% xx
        XiCY <- t(xx) %*% iC %*% t(y)
        
        b <- solve(XiCX, XiCY)
        
        h <- t(y) - (xx %*% b)
        
        MSE <- t(h) %*% iC %*% h/(p - 2)
        
        iXiCX <- solve(XiCX)
        bSE <- (MSE * iXiCX[2, 2])^0.5
        output$score[i] <- b[2]/bSE
    }
}
output<-output[order(output$score),]
write.csv(output,"~/Documents/Project/TBSimulation/rpoB_GY84_19_scores.csv",row.names = FALSE, )

#Get scores for S450 containing kmers.
kft<-1 #kmer frequency threshold
pattern450<-array(0,nrow(S450_kmers))
for (i in 1:nrow(S450_kmers)){
    pattern450_j<-array(1,ncol(S450_kmers)-1)
    for (j in 2:ncol(S450_kmers)){
        if (S450_kmers[i,][j]<kft){
            pattern450_j[j-1]<-0
        }
    }
    pattern450[i]<-paste(pattern450_j,collapse='' )
}
output_450<-output[output$pattern %in% unique(pattern450),]
write.csv(output_450,"~/Documents/Project/TBSimulation/rpoB_GY84_19_scores_450.csv",row.names = FALSE, )
