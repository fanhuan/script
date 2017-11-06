# pandas
import pandas as pd
# read
S450 = pd.read_table('S450_'+count+'.kmer',header=None,names=['kmer'])
# rename
lily.rename(index=str, columns={"old name": "new name"})
# get value of a column
s = df['A']
# convert into present/absent
## convert whole df
df[df>1] = 0
## convert a columns
df.a[df.a>1] = 0
## row sum
df.sum(axis = 1)
## col sum
df.sum()
## convert numpy series to dataframe
df.sum().to_frame()
## filter rows
df_filtered = df.query('variable > 30000')
## manipulate the content of a column
### get rid of the suffix
df['A'] = df['A'].str[:-len('.faa')]
## put columns of values into a dictionary
df_dic = dict(zip(df['A'],df['B']))
## add a new column based on an existing column as keys in a dictionary
df['C'] = df['A'].map(d)

S450_kmers = list(df.loc[:,'kmer'])
GLS = S450_df.loc[:,'rankGLS']
S450_dic = dict(zip(S450_kmers,GLS))
Npatterns = str(len(set(S450_df.loc[:,'pattern'])))
model_list = model_iter('model.fasta')
#tally
dic_gene[file] = tsv.gene.value_counts().to_frame(name=file)
#outter join, or merge
result = pd.concat(dic_gene.values(), axis=1)
#write
result.to_csv()

#matplotlib
import matplotlib.pyplot as plt
n, bins, patches = plt.hist(dataframe['variable'], 50, normed=1, facecolor='g', alpha=0.75)
plt.show()

#iter through all the folders in the directory
for file in os.lidstdir(directory):
    if os.path.isdir(os.path.join(directory, file)):

# list
list1 = [x.split(',') for x in list2]
## join a list of list
combined = [item for sublist in lists for item in sublist]
