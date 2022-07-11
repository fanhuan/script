BiocManager::install("clusterProfiler")
library("clusterProfiler")

metagenome_enrichment = function(targetGenes,
                                 pathwayName,
                                 genePathway,
                                 pAdjustMethod='BH',
                                 pvalueCutoff=0.05,
                                 qvalueCutoff=0.05){
  
  gene_pathway = data.frame()
  count = 1
  for (i in 1:nrow(gene2pathway)) {
    str = strsplit(gene2pathway[i,],'\t')[[1]]
    for (j in 2:length(str)) {
      gene_pathway[count,1] = str[1]
      gene_pathway[count,2] = str[j]
      count = count + 1
    }
  }
  
  colnames(gene_pathway) = c('pathway_id','gene_id')
  colnames(gene_pathway) = c('pathway_id','pathway_term')
  
  clustergene = targetGenes
  backgene = gene_pathway[,2]
  
  enrich_result = clusterProfiler::enricher(gene=clustergene,universe=backgene,
                                 TERM2GENE=gene_pathway,TERM2NAME=pathway,
                                 pAdjustMethod=pAdjustMethod,
                                 pvalueCutoff=pvalueCutoff,qvalueCutoff=qvalueCutoff)
  
  return(enrich_result)
}

# example
pathway = read.table('~/build/picrust2-2.5.0/picrust2/default_files/description_mapfiles/KEGG_pathways_info.tsv',sep = '\t')
pathway <- read_delim("~/build/picrust2-2.5.0/picrust2/default_files/description_mapfiles/KEGG_pathways_info.tsv", 
                                      delim = "\t", escape_double = FALSE, 
                                      trim_ws = TRUE, col_names = c('V1','V2'))
gene2pathway = read.table('~/build/picrust2-2.5.0/picrust2/default_files/pathway_mapfiles/KEGG_pathways_to_KO.tsv',sep = ',')
# one column only
targetGenes = c('K07370','K07210','K10989')

test = metagenome_enrichment(targetGenes=targetGenes,
                             pathwayName = pathway,
                             genePathway = gene2pathway)

barplot(test)
