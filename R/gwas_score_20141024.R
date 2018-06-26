library(ape)
Ytree <- read.tree(file = '/Users/iveslab/Documents/projects/GWAS/Yeast/yeast32_asb_k17.tre')
plot(Ytree)
Y_VCV <- vcv(Ytree)
h <- order(colnames(Y_VCV))
Y_VCV <- Y_VCV[h,h]

library(data.table)

sample_Y_VCV <- read.csv(file = '/Users/iveslab/Documents/YeastSNP_VCV.csv', header=F)

p <- length(sample_Y_VCV[,1])

X <- read.fwf(file='/Users/iveslab/Dropbox/RESEARCH/GWAS/zhezhen/yeastSNP_Pattern.stats', widths=array(1,c(1,p)),header=F)

n <- dim(X)[1]

y <- sample_Y_VCV[,2]
VCV <- sample_Y_VCV[,2:length(sample_Y_VCV[1,])]

# compute scores
C <- as.matrix(VCV)
C <- C/det(C)^(1/p)

iC <- solve(C)
#iC <- diag(1,nrow=p,ncol=p)
ones <- array(1,c(p,1))

output <- array(0,c(n,1))
for(i in 1:n){
  x <- as.matrix(X[i,])
  sumx <- sum(x)
  
  if(sumx < 2 | sumx > (p-1)) output[i] <- 0
  else{
    tx <- t(x)
    xx <- cbind(ones,tx)
    
    XiCX <- t(xx) %*% iC %*% xx
    XiCY <- t(xx) %*% iC %*% y
    
    b <- solve(XiCX,XiCY)
    
    h <- y - (xx %*% b)
    
    MSE <- t(h) %*% iC %*% h/p
    
    iXiCX <- solve(XiCX)
    bSE <- (MSE * iXiCX[2,2])^.5
    output[i] <- b[2]/bSE
  }
}

hist(abs(output),breaks=50, main=NULL, xlab='Abs(scores)', ylab='Count')

Xpattern <- X[abs(output)>1.96,]
dim(Xpattern)

par(mfrow=c(3,3),mai=c(0,0,0,0))
#for(i in 1:9) plot(y ~ as.numeric(Xpattern[i,]),xaxt="n",yaxt="n",xlim=c(-.2,1.2))

for(i in 1:9) plot(y ~ factor(as.numeric(Xpattern[i,])),xaxt="n",yaxt="n",xlim=c(.5,2.5))
Pattern <- read.table(file='/Users/iveslab/Dropbox/RESEARCH/GWAS/zhezhen/yeastSNP_Pattern.stats',header=F, colClasses=c(rep("factor",41))) 
Pattern <- Pattern[1]
Pattern$score <-output
names(Pattern) <-c("pattern", "score")
Pattern <- Pattern[order(Pattern$score),]
write.table(Pattern,file='/Users/iveslab/Dropbox/RESEARCH/GWAS/zhezhen/yeastSNP_GWAScore_24Oct14.txt', sep="\t",col.names=F, row.names=F, quote=F)
