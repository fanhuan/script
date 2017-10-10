# pandas
import pandas as pd
S450 = pd.read_table('S450_'+count+'.kmer',header=None,names=['kmer'])
S450_kmers = list(extra.loc[:,'kmer'])
GLS = S450_df.loc[:,'rankGLS']
S450_dic = dict(zip(S450_kmers,GLS))
Npatterns = str(len(set(S450_df.loc[:,'pattern'])))
model_list = model_iter('model.fasta')

#matplotlib
import matplotlib.pyplot as plt
n, bins, patches = plt.hist(dataframe['variable'], 50, normed=1, facecolor='g', alpha=0.75)
