library(phylosim)

setwd("/Users/arives/Box Sync/Traveller Box/Huan GWAS")
#Enable the "fast and careless mode"
PSIM_FAST<-TRUE
#Set up the codon evol model = GY94 for codon evolution of protein-coding genes
p.flanking<-GY94()
p.S450<-GY94() #variable region, starting as sensitive, at codon position 450

#codon freqs for flanking regions are calculated based on 11 rpoB genes in Mycobacterium genus, stored in rpoB_alignment.fa 
#calculates transitions from the frequency: 61 possible codons, excluding the 3 stop codons
codon.freqs.flanking<-c(0.001783083959996899, 0.027676564074734476, 7.752538956508256e-05, 0.010000775253895651, 0.002170710907822312, 0.01783083959996899, 0.0018606093495619816, 0.023335142259089853, 0.0013954570121714862, 0.018683618885184897, 0.0013954570121714862, 0.005659353438251027, 0.0076750135669431735, 0.0031010155826033028, 0.012869214667803705, 0.0009303046747809908, 0.0560508566555547, 0.002480812466082642, 0.013101790836498954, 0.0024032870765175597, 0.036824560043414216, 0.0013179316226064035, 0.01744321265214358, 0.0024032870765175597, 0.026978835568648732, 0.010620978370416312, 0.03829754244515079, 0.002480812466082642, 0.017908364989534072, 0.004496472594774789, 0.05124428250251958, 0.00038762694782541285, 0.02597100550430266, 0.0031010155826033028, 0.03697961082254438, 0.0015505077913016514, 0.0133343670051942, 0.0018606093495619816, 0.03232808744863943, 0.003178540972168385, 0.03969299945732227, 0.003566167919993798, 0.009225521358244825, 0, 0.0006977285060857431, 0.006279556554771687, 0.042173811923404914, 0.0009303046747809908, 0.043414218156446235, 0.004651523373904954, 0.03721218699123963, 0.0034886425304287154, 0.025505853166912163, 0.00814016590433367, 0.06202031165206605, 0.014652298627800604, 0.07473447554073959, 0.024032870765175594, 0.046437708349484456, 0.003566167919993798, 0.010388402201721063)

p.flanking<-GY94(equDist=codon.freqs.flanking,force=TRUE)
p.flanking$kappa=2 #kappa is the transition/transversion rate

##set up hotspot
#6 codons for serine
#codon freqs for S450 are Ser(5), 3rd codon sub(4), 2nd(3), 2nd and 3rd(2), others(1)
codon.freqs.S450<-c(3,3,3,3,5,5,5,5,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,2,2,3,3,2,2,3,3,2,2,5,5,4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)/127
p.S450<-GY94(equDist=codon.freqs.S450,force=TRUE)
p.S450$kappa=2
#Plot the transition matrix and equilibrium distribution of the two models

plot(p.flanking, scale=0.5)
plot(p.S450, scale=0.5)
#construct the root sequence
rpoB<-CodonSequence(string="TTGGCAGATTCCCGCCAGAGCAAAACAGCCGCTAGTCCTAGTCCGAGTCGCCCGCAAAGTTCCTCGAATAACTCCGTACCCGGAGCGCCAAACCGGGTCTCCTTCGCTAAGCTGCGCGAACCACTTGAGGTTCCGGGACTCCTTGACGTCCAGACCGATTCGTTCGAGTGGCTGATCGGTTCGCCGCGCTGGCGCGAATCCGCCGCCGAGCGGGGTGATGTCAACCCAGTGGGTGGCCTGGAAGAGGTGCTCTACGAGCTGTCTCCGATCGAGGACTTCTCCGGGTCGATGTCGTTGTCGTTCTCTGACCCTCGTTTCGACGATGTCAAGGCACCCGTCGACGAGTGCAAAGACAAGGACATGACGTACGCGGCTCCACTGTTCGTCACCGCCGAGTTCATCAACAACAACACCGGTGAGATCAAGAGTCAGACGGTGTTCATGGGTGACTTCCCGATGATGACCGAGAAGGGCACGTTCATCATCAACGGGACCGAGCGTGTGGTGGTCAGCCAGCTGGTGCGGTCGCCCGGGGTGTACTTCGACGAGACCATTGACAAGTCCACCGACAAGACGCTGCACAGCGTCAAGGTGATCCCGAGCCGCGGCGCGTGGCTCGAGTTTGACGTCGACAAGCGCGACACCGTCGGCGTGCGCATCGACCGCAAACGCCGGCAACCGGTCACCGTGCTGCTCAAGGCGCTGGGCTGGACCAGCGAGCAGATTGTCGAGCGGTTCGGGTTCTCCGAGATCATGCGATCGACGCTGGAGAAGGACAACACCGTCGGCACCGACGAGGCGCTGTTGGACATCTACCGCAAGCTGCGTCCGGGCGAGCCCCCGACCAAAGAGTCAGCGCAGACGCTGTTGGAAAACTTGTTCTTCAAGGAGAAGCGCTACGACCTGGCCCGCGTCGGTCGCTATAAGGTCAACAAGAAGCTCGGGCTGCATGTCGGCGAGCCCATCACGTCGTCGACGCTGACCGAAGAAGACGTCGTGGCCACCATCGAATATCTGGTCCGCTTGCACGAGGGTCAGACCACGATGACCGTTCCGGGCGGCGTCGAGGTGCCGGTGGAAACCGACGACATCGACCACTTCGGCAACCGCCGCCTGCGTACGGTCGGCGAGCTGATCCAAAACCAGATCCGGGTCGGCATGTCGCGGATGGAGCGGGTGGTCCGGGAGCGGATGACCACCCAGGACGTGGAGGCGATCACACCGCAGACGTTGATCAACATCCGGCCGGTGGTCGCCGCGATCAAGGAGTTCTTCGGCACCAGCCAGCTGAGCCAATTCATGGACCAGAACAACCCGCTGTCGGGGTTGACCCACAAGCGCCGACTGTCGGCGCTGGGGCCCGGCGGTCTGTCACGTGAGCGTGCCGGGCTGGAGGTCCGCGACGTGCACCCGTCGCACTACGGCCGGATGTGCCCGATCGAAACCCCTGAGGGGCCCAACATCGGTCTGATCGGCTCGCTGTCGGTGTACGCGCGGGTCAACCCGTTCGGGTTCATCGAAACGCCGTACCGCAAGGTGGTCGACGGCGTGGTTAGCGACGAGATCGTGTACCTGACCGCCGACGAGGAGGACCGCCACGTGGTGGCACAGGCCAATTCGCCGATCGATGCGGACGGTCGCTTCGTCGAGCCGCGCGTGCTGGTCCGCCGCAAGGCGGGCGAGGTGGAGTACGTGCCCTCGTCTGAGGTGGACTACATGGACGTCTCGCCCCGCCAGATGGTGTCGGTGGCCACCGCGATGATTCCCTTCCTGGAGCACGACGACGCCAACCGTGCCCTCATGGGGGCAAACATGCAGCGCCAGGCGGTGCCGCTGGTCCGTAGCGAGGCCCCGCTGGTGGGCACCGGGATGGAGCTGCGCGCGGCGATCGACGCCGGCGACGTCGTCGTCGCCGAAGAAAGCGGCGTCATCGAGGAGGTGTCGGCCGACTACATCACTGTGATGCACGACAACGGCACCCGGCGTACCTACCGGATGCGCAAGTTTGCCCGGTCCAACCACGGCACTTGCGCCAACCAGTGCCCCATCGTGGACGCGGGCGACCGAGTCGAGGCCGGTCAGGTGATCGCCGACGGTCCCTGTACTGACGACGGCGAGATGGCGCTGGGCAAGAACCTGCTGGTGGCCATCATGCCGTGGGAGGGCCACAACTACGAGGACGCGATCATCCTGTCCAACCGCCTGGTCGAAGAGGACGTGCTCACCTCGATCCACATCGAGGAGCATGAGATCGATGCTCGCGACACCAAGCTGGGTGCGGAGGAGATCACCCGCGACATCCCGAACATCTCCGACGAGGTGCTCGCCGACCTGGATGAGCGGGGCATCGTGCGCATCGGTGCCGAGGTTCGCGACGGGGACATCCTGGTCGGCAAGGTCACCCCGAAGGGTGAGACCGAGCTGACGCCGGAGGAGCGGCTGCTGCGTGCCATCTTCGGTGAGAAGGCCCGCGAGGTGCGCGACACTTCGCTGAAGGTGCCGCACGGCGAATCCGGCAAGGTGATCGGCATTCGGGTGTTTTCCCGCGAGGACGAGGACGAGTTGCCGGCCGGTGTCAACGAGCTGGTGCGTGTGTATGTGGCTCAGAAACGCAAGATCTCCGACGGTGACAAGCTGGCCGGCCGGCACGGCAACAAGGGCGTGATCGGCAAGATCCTGCCGGTTGAGGACATGCCGTTCCTTGCCGACGGCACCCCGGTGGACATTATTTTGAACACCCACGGCGTGCCGCGACGGATGAACATCGGCCAGATTTTGGAGACCCACCTGGGTTGGTGTGCCCACAGCGGCTGGAAGGTCGACGCCGCCAAGGGGGTTCCGGACTGGGCCGCCAGGCTGCCCGACGAACTGCTCGAGGCGCAGCCGAACGCCATTGTGTCGACGCCGGTGTTCGACGGCGCCCAGGAGGCCGAGCTGCAGGGCCTGTTGTCGTGCACGCTGCCCAACCGCGACGGTGACGTGCTGGTCGACGCCGACGGCAAGGCCATGCTCTTCGACGGGCGCAGCGGCGAGCCGTTCCCGTACCCGGTCACGGTTGGCTACATGTACATCATGAAGCTGCACCACCTGGTGGACGACAAGATCCACGCCCGCTCCACCGGGCCGTACTCGATGATCACCCAGCAGCCGCTGGGCGGTAAGGCGCAGTTCGGTGGCCAGCGGTTCGGGGAGATGGAGTGCTGGGCCATGCAGGCCTACGGTGCTGCCTACACCCTGCAGGAGCTGTTGACCATCAAGTCCGATGACACCGTCGGCCGCGTCAAGGTGTACGAGGCGATCGTCAAGGGTGAGAACATCCCGGAGCCGGGCATCCCCGAGTCGTTCAAGGTGCTGCTCAAAGAACTGCAGTCGCTGTGCCTCAACGTCGAGGTGCTATCGAGTGACGGTGCGGCGATCGAACTGCGCGAAGGTGAGGACGAGGACCTGGAGCGGGCCGCGGCCAACCTGGGAATCAATCTGTCCCGCAACGAATCCGCAAGTGTCGAGGATCTTGCG")

attachProcess(rpoB,p.flanking,1:449) #left hand side
attachProcess(rpoB,p.S450,450) #susceptive spot
attachProcess(rpoB,p.flanking,451:1172) #right hand side

#Construct a deletion process proposing deletions with rate 0.00083333 according to a discrete length distribution
d<-DiscreteDeletor(rate=0.00083333, sizes=c(1,2,3,4,5,6,7), probs=c(0.2,0.2,.2,.1,.1,.1,.1))
#Construct an insertion process proposing insertions with rate 0.25 according to a discrete length distribution
i<-DiscreteInsertor(rate=0.00083333, sizes=c(1,2,3,4,5,6,7), probs=c(0.2,0.2,.2,.1,.1,.1,.1))
#Set the templete sequence for the insertion process (what to insert)
i$templateSeq<-NucleotideSequence(length=7,processes=list(list(p.flanking)))
#Attaching the indel processes to the flanking regions.
attachProcess(rpoB,d,1:449)
attachProcess(rpoB,d,451:1172)
attachProcess(rpoB,i,1:449)
attachProcess(rpoB,i,451:1172)

#Sample omegas from a discrete model. Omegas are dN/dS. 1 is neutral. <1 if favored, >1 if deleterious
#You want the S450 to be deleterious
omegaVarM3(rpoB,p.flanking,omegas=c(0,0.5,1),probs=c(2/4,1/4,1/4),index=c(1:449,451:1172))
omegaVarM3(rpoB,p.S450,omegas=c(0,0.5,1),probs=c(2/4,1/4,1/4),index=c(450))

#Set the phylogenetic tree
cat("(((((MAF_11821_03:0.412,(MAF_GM_0981:0.582,MTB_95_0545:0.550):0.184):0.212,((MTB_K21:0.242,(MTB_K67:0.280,MTB_K93:0.234):0.096):0.108,(MTB_T17:0.624,MTB_T92:0.584):0.150):0.114):0.096,(((((MTB_00_1695:0.510,MTB_T67:0.518):0.182,MTB_T85:0.278):0.154,(MTB_98_1833:0.392,MTB_M4100A:0.072):0.142):0.134,(MTB_4783_04:0.574,MTB_GM_1503:0.596):0.166):0.118,MTB_91_0079:0.576):0.094):0.074,(MTB_K37:0.518,MTB_K49:0.288):0.070):0.138,MTB_H37Rv:0.256);",file="TBSimulation.nwk")

#NEW SIM.REPLICATE
#Function to simulate a single replication
serine.codons <- c('TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC')
phy <- read.tree(file="TBSimulation.nwk")
nr.replicates<-3

p <- Ntip(phy)

sim.replicate<-function(i){
  name<-paste("replication_",i,sep="")
  
  sim<-Simulate(PhyloSim(name=name,root.seq=rpoB,phylo=read.tree("TBSimulation.nwk")),quiet=TRUE) 
  saveAlignment(sim,file=paste("GWAS simulations/rpoB_GY84_",i,".fas",sep=""),skip.internal=TRUE) #do not save the internal node states
  
  root<-sim$alignment[1,]
  
  w <- data.frame(tip=phy$tip.label, serine = TRUE)
  for (ii in 1:length(root)) {
    if (!is.na(names(root[ii]))) {
      if (names(root[ii])=="450") {
        selected.codons <- sim$alignment[,ii]
        for(kk in phy$tip.label)
        	w$serine[w$tip == kk] <- is.element(selected.codons[names(selected.codons) == kk],serine.codons)
      }
    } 
  }
  write.csv(w,file=paste("GWAS simulations/rpoB_GY84_trait_",i,".csv",sep=""))
  return(sim)
  return(TRUE) #save memory by throwing away objects generated
}

#Run replication in parallel
library(parallel)
res.objects<-mclapply(1:nr.replicates,sim.replicate,mc.cores=3)




####################################################################################
####################################################################################
####################################################################################
# Huan's code for AAF

#Parameters for AAF
#memory per thread
total_Gmem<-10
if (total_Gmem/nr.replicates > 1) {
	memPerSim<-1
} else {
	memPerSim<-total_Gmem/nr.replicates
}

#k-mer length
k<-5

#Function to process a single fas file
aaf.replicate<-function(i){
	simFile=paste("rpoB_GY84_",i,".fas",sep=“")
	outfile<-paste(phylokmer_",as.character(i),".dat",sep=“")
	aaf_phylosim.call<-paste("python aaf_phylosim.py -k ",
	as.character(k)," -i ", simFile," -G ", memPerSim, " -o ",
	outfile,sep="")
	print(aaf_phylosim.call)
	system(aaf_phylosim.call, ignore.stdout = T)
	kmer_pattern.call<-paste("python kmer_pattern.py -i ", outfile,
	"-t 10 -G ",memPerSim," -o kmerPattern_",as.character(i), ".stats",sep="")
	print(kmer_pattern.call)
	system(kmer_pattern.call, ignore.stdout = T)
}

#Run replication in parallel
mclapply(1:nr.replicates, aaf.replicate, mc.cores=3)
####################################################################################
####################################################################################
####################################################################################

# or use sim.1 <- Simulate(PhyloSim(root.seq=rpoB,phylo=read.tree("TBSimulation.nwk")),quiet=TRUE)

#Check the status of S450 in each simulation.
#Note that states of S450 at internal nodes are also included
#Codons for Serine are: TCT, TCC, TCA, TCG, AGT, AGC
serine.codons <- c('TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC')
phy <- read.tree(file="TBSimulation.nwk")

p <- Ntip(phy)
tip.names <- phy$tip.label
rep.names <- matrix(matrix(1, ncol=1, nrow=Ntip(phy)) %*% matrix(1:nr.replicates, ncol=nr.replicates, nrow=1), ncol=1)
w <- data.frame(rep=rep.names, tip=phy$tip.label, serine = TRUE)

for (j in 1:nr.replicates) {
  print(noquote(c("S450 in Simulation",j)))
  root<-res.objects[[j]]$alignment[1,]
  for (i in 1:length(root)) {
    if (!is.na(names(root[i]))) {
      if (names(root[i])=="450") {
        print(i)
        selected.codons <- res.objects[[j]]$alignment[,i]
        print(selected.codons)
        print(is.element(res.objects[[j]]$alignment[,i],serine.codons))
        for(k in tip.names)
        	w$serine[w$rep == j & w$tip == k] <- is.element(selected.codons[names(selected.codons) == k],serine.codons)
        break
      }
    } 
  }
} 

write.csv(w, file='GWAS simulations/rpoB_GY84_traits.csv', row.names=F)

# compute phylogenetic signal
n <- nr.replicates

sum.phy <- data.frame(rep=1:n, s2=0, Pr=1)
for(i in 1:n){
	x <- w[w$rep==i,]
	row.names(x) <- x$tip
	z <- binaryPGLMM(serine ~ 1, data = x, phy)
	sum.phy$s2[i] <- z$s2
	sum.phy$Pr[i] <- z$P.H0.s2
}

write.csv(sum.phy, file='GWAS simulations/rpoB_GY84_signal.csv', row.names=F)


###############

# compute scores
n <- nr.replicates

C <- as.matrix(vcv(phy))
C <- C/det(C)^(1/p) #some transformation of C to make the determinant = 1, which should make calculations easier

iC <- solve(C) #inverse of C
ones <- array(1,c(p,1)) # array of ones for the intercept
output <- array(0,c(n,1)) # collects the results for the n patterns
threshold <- 3 # minimum number of zeros or ones for inclusion of pattern
for(i in 1:n){
  y <- as.matrix(w$serine[w$rep==i]) 
  sumy <- sum(y) #sum of the pattern
  
  if (sumy < threshold | sumy > (p-threshold)) {
  	output[i] <- 0 #all patterns with only 1 one or zero are assigned score 0.
  	}  else{
    xx <- cbind(ones,X)
    
    XiCX <- t(xx) %*% iC %*% xx
    XiCY <- t(xx) %*% iC %*% t(y)
    
    b <- solve(XiCX,XiCY)
    
    h <- t(y) - (xx %*% b)
    
    MSE <- t(h) %*% iC %*% h/(p-2)
    
    iXiCX <- solve(XiCX)
    bSE <- (MSE * iXiCX[2,2])^.5
    output[i] <- b[2]/bSE
  }
}






#OLD Function to simulate a single replication
sim.replicate<-function(i){
  name<-paste("replication_",i,sep="")
  
  sim<-Simulate(PhyloSim(name=name,root.seq=rpoB,
                         phylo=read.tree("TBSimulation.nwk")),
                quiet=TRUE) 
  saveAlignment(sim,file=paste("GWAS simulations/rpoB_GY84_",i,".fas",sep=""),skip.internal=TRUE) #do not save the internal node states
  return(sim)
  return(TRUE) #save memory by throwing away objects generated
}

