library(optparse)

option_list <- list(
  make_option(c("-s", "--single"), type = "character", default = FALSE,
              action = "store", help = "single sequencing data! format .csv"
  ),
  make_option(c("-m", "--mix"), type = "character", default = FALSE,
              action = "store", help = "mix sequencing data! format .csv"
  ),
  make_option(c("-x", "--input_single_matrix"), type = "character", default = FALSE,
              action = "store", help = "any input single matrix, format .csv"
  ),
  make_option(c("-y", "--input_mix_matrix"), type = "character", default = FALSE,
              action = "store", help = "any input mix matrix, format .csv"
  ),
  make_option(c("-p", "--perm"), type = "numeric", default = 0,
              action = "store", help = "number of permutations"
  ),
  make_option(c("-c", "--calculate_deconvolution"),type = "logical", default = TRUE,
              action = "store", help = "whether calculate deconvolution or not"
  )
)

opt = parse_args(OptionParser(option_list = option_list, 
                              usage = "Deconvolution!"))




###########################Deconvolution function

CoreAlg <- function(X, y){
  
  #try different values of nu
  svn_itor <- 3
  
  res <- function(i){
    if(i==1){nus <- 0.25}
    if(i==2){nus <- 0.5}
    if(i==3){nus <- 0.75}
    model<-e1071::svm(X,y,type="nu-regression",kernel="linear",nu=nus,scale=F)
    model
  }
  
  if(Sys.info()['sysname'] == 'Windows') {
    out <- parallel::mclapply(1:svn_itor, res, mc.cores=1) 
  }else{
    out <- parallel::mclapply(1:svn_itor, res, mc.cores=svn_itor)
    }
    
  
  nusvm <- rep(0,svn_itor)
  corrv <- rep(0,svn_itor)
  
  #do cibersort
  t <- 1
  while(t <= svn_itor) {
    weights = t(out[[t]]$coefs) %*% out[[t]]$SV
    weights[which(weights<0)]<-0
    w<-weights/sum(weights)
    u <- sweep(X,MARGIN=2,w,'*')
    k <- apply(u, 1, sum)
    nusvm[t] <- sqrt((mean((k - y)^2)))
    corrv[t] <- cor(k, y)
    t <- t + 1
  }
  
  #pick best model
  rmses <- nusvm
  mn <- which.min(rmses)
  model <- out[[mn]]
  
  #get and normalize coefficients
  q <- t(model$coefs) %*% model$SV
  q[which(q<0)]<-0
  w <- (q/sum(q))
  
  mix_rmse <- rmses[mn]
  mix_r <- corrv[mn]
  
  newList <- list("w" = w, "mix_rmse" = mix_rmse, "mix_r" = mix_r)
  
}


doPerm <- function(perm, X, Y){
  itor <- 1
  Ylist <- as.list(data.matrix(Y))
  dist <- matrix()
  
  while(itor <= perm){
    #print(itor)
    
    #random mixture
    yr <- as.numeric(Ylist[sample(length(Ylist),dim(X)[1])])
    
    #standardize mixture
    yr <- (yr - mean(yr)) / sd(yr)
    
    #run CIBERSORT core algorithm
    result <- CoreAlg(X, yr)
    
    mix_r <- result$mix_r
    
    #store correlation
    if(itor == 1) {dist <- mix_r}
    else {dist <- rbind(dist, mix_r)}
    
    itor <- itor + 1
  }
  newList <- list("dist" = dist)
}


CIBERSORT <- function(sig_matrix, mixture_file, perm=0, QN=TRUE,outfile){
  
  #read in data
  X <- data.matrix(sig_matrix)
  Y <- data.matrix(mixture_file)
  
  #order
  X <- X[order(rownames(X)),]
  Y <- Y[order(rownames(Y)),]
  
  P <- perm #number of permutations
  
  #anti-log if max < 50 in mixture file
  if(max(Y) < 50) {Y <- 2^Y}
  
  #quantile normalization of mixture file
  if(QN == TRUE){
    tmpc <- colnames(Y)
    tmpr <- rownames(Y)
    Y <- preprocessCore::normalize.quantiles(Y)
    colnames(Y) <- tmpc
    rownames(Y) <- tmpr
  }
  
  #intersect genes
  Xgns <- row.names(X)
  Ygns <- row.names(Y)
  YintX <- Ygns %in% Xgns
  Y <- Y[YintX,]
  XintY <- Xgns %in% row.names(Y)
  X <- X[XintY,]
  
  #standardize sig matrix
  X <- (X - mean(X)) / sd(as.vector(X))
  
  #empirical null distribution of correlation coefficients
  if(P > 0) {nulldist <- sort(doPerm(P, X, Y)$dist)}
  
  #print(nulldist)
  
  header <- c('Mixture',colnames(X),"P-value","Correlation","RMSE")
  #print(header)
  
  output <- matrix()
  itor <- 1
  mixtures <- dim(Y)[2]
  pval <- 9999
  
  #iterate through mixtures
  while(itor <= mixtures){
    
    y <- Y[,itor]
    
    #standardize mixture
    y <- (y - mean(y)) / sd(y)
    
    #run SVR core algorithm
    result <- CoreAlg(X, y)
    
    #get results
    w <- result$w
    mix_r <- result$mix_r
    mix_rmse <- result$mix_rmse
    
    #calculate p-value
    if(P > 0) {pval <- 1 - (which.min(abs(nulldist - mix_r)) / length(nulldist))}
    
    #print output
    out <- c(colnames(Y)[itor],w,pval,mix_r,mix_rmse)
    if(itor == 1) {output <- out}
    else {output <- rbind(output, out)}
    
    itor <- itor + 1
    
  }
  
  #save results
  write.table(rbind(header,output), file='percentage.txt', sep="\t", row.names=F, col.names=F, quote=F)
  
  #return matrix object containing all results
  obj <- rbind(header,output)
  obj <- obj[,-1]
  obj <- obj[-1,]
  obj <- matrix(as.numeric(unlist(obj)),nrow=nrow(obj))
  rownames(obj) <- colnames(Y)
  colnames(obj) <- c(colnames(X),"P-value","Correlation","RMSE")
  obj
}

###########################Read files
read_all_files = function(mix_path,
                          single_path){
  
  
  # get single data
  single_a <- list.files(single_path)
  dir_a <- paste(single_path, single_a,sep="")  
  
  
  # get files
  assign(paste("single_data", 1,sep = '_'), 
         na.omit(read.csv(file = dir_a[1], header=F, sep=",")))
  
  assign(paste("single_data", 2,sep = '_'), 
         na.omit(read.csv(file = dir_a[2], header=F, sep=",")))
  
  # make intersect
  single_intersect_a = intersect(single_data_1[[1]],c(single_data_2[[1]]))
  for(i in 3:length(dir_a)){
    single_intersect_a = intersect(single_intersect_a,assign(paste("single_data", i,sep = '_'), 
                                                             na.omit(read.csv(file = dir_a[i], header=F, sep=",")))[[1]])
  }
  
  # combine all single data
  all_single = cbind(single_data_1[single_data_1[,1] %in% single_intersect_a,],
                     single_data_2[single_data_2[,1] %in% single_intersect_a,])
  
  
  for (i in 3:length(dir_a)) {
    all_single = cbind(all_single,
                       eval(parse(text = paste0(paste("single_data", i,sep = '_'),'[',
                                                paste("single_data", i,sep = '_'), 
                                                '[,1]',' %in% single_intersect_a,]'))))
  }
  
  row.names(all_single) = all_single[,1]
  all_single = all_single[,-c(seq(1,ncol(all_single),2))]
  colnames(all_single) = c(single_a)
  
  # avoid depth
  all_single = all_single / colSums(all_single)
  
  # get mix data
  mix_b <- list.files(mix_path)
  dir_b <- paste(mix_path, mix_b,sep="")  
  
  
  # get files
  assign(paste("mix_data", 1,sep = '_'), 
         na.omit(read.csv(file = dir_b[1], header=F, sep=",")))
  
  assign(paste("mix_data", 2,sep = '_'), 
         na.omit(read.csv(file = dir_b[2], header=F, sep=",")))
  
  # make intersect
  mix_intersect_b = intersect(mix_data_1[[1]],c(mix_data_2[[1]]))
  for(i in 3:length(dir_b)){
    mix_intersect_b = intersect(mix_intersect_b,assign(paste("mix_data", i,sep = '_'), 
                                                       na.omit(read.csv(file = dir_b[i], header=F, sep=",")))[[1]])
  }
  
  
  # combine all mix data
  all_mix = cbind(mix_data_1[mix_data_1[,1] %in% mix_intersect_b,],
                  mix_data_2[mix_data_2[,1] %in% mix_intersect_b,])
  
  
  for (i in 3:length(dir_b)) {
    all_mix = cbind(all_mix,
                    eval(parse(text = paste0(paste("mix_data", i,sep = '_'),'[',
                                             paste("mix_data", i,sep = '_'), 
                                             '[,1]',' %in% mix_intersect_b,]'))))
  }
  
  row.names(all_mix) = all_mix[,1]
  all_mix = all_mix[,-c(seq(1,ncol(all_mix),2))]
  colnames(all_mix) = c(mix_b)
  
  # avoid depth
  all_mix = all_mix / colSums(all_mix)
  
  result = list(mix_data = all_mix,single_data = all_single)
  
  return(result)
}

#####################################pipeline
if (is.null(opt$mix) != TRUE & is.null(opt$single) != TRUE & is.null(opt$single) & opt$calculate_deconvolution) {
  result = read_all_files(mix_path = opt$mix,single_path = opt$single)
  
  CIBERSORT(sig_matrix = result$single_data,mixture_file = result$mix_data,
            perm = opt$perm,QN = F)
  
}else if(is.null(opt$input_single_matrix) != TRUE & is.null(opt$input_mix_matrix) != TRUE & opt$calculate_deconvolution){
  x = read.csv(opt$input_single_matrix,header = T,row.names = 1)
  y = read.csv(opt$input_mix_matrix,header = T,row.names = 1)
  CIBERSORT(sig_matrix = x,mixture_file = y,
            perm = opt$perm,QN = F)
  
}else if(is.null(opt$mix) != TRUE & is.null(opt$single) != TRUE 
         & is.null(opt$input_mix_matrix) == TRUE 
         & is.null(opt$input_single_matrix) == TRUE
         & !opt$calculate_deconvolution){
  
  result = read_all_files(mix_path = opt$mix,single_path = opt$single)
  
  write.table(result$single_data, file='singleMatrix.txt', sep="\t", 
              row.names=F, col.names=F, quote=F)
  write.table(result$mix_data, file='mixMatrix.txt', sep="\t", 
              row.names=F, col.names=F, quote=F)
}else{
  stop("Please add right parameters")
}


