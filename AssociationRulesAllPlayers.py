# Code to obtain association rules from all players through Apriori.

# Imports.
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.preprocessing import KBinsDiscretizer

# Function to qualify the data in the dataframe
# Inputs: a dataframe do be qualified, the column name that is going to be classified, how many bins to qualify and which strategy.
# Output: the orinigal dataframe now qualified.
def qualify(dataframe, name, quantity, strategy):
	est = KBinsDiscretizer(n_bins=[quantity], encode = 'ordinal', strategy = strategy)
	dataframe[name] = est.fit_transform(dataframe[[name]])
	return dataframe

# Function to transform a dataframe in a onehot encoded dataframe for a column.
# Inputs: a dataframe to be onehot encoded and a column name.
# Output: the original dataframe now onehot encoded.
def oneHotEncoding(dataframe, name):
	dataframe[name] = pd.Categorical(dataframe[name])
	dataframe = pd.get_dummies(dataframe, prefix = [name])
	return dataframe
	
# Opening Csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Dropping Unneeded data.
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.participou != 1)].index , inplace = True)
scouts.drop(columns = ['rodada','clube_id','atleta_id','participou','preco_num','pontos_num','media_num','partida_id', 'posicao_id'], inplace = True)

# Turning floats into ints.
scouts['titular'] = scouts['titular'].apply(np.int64)

# Qualifying data in the dataframe.
for data in ['variacao_num','jogos_num']:
	scouts = qualify(scouts,data, 5, 'quantile')
for data in ['tempo_jogado','nota']:
	scouts = qualify(scouts,data, 3, 'uniform')
for data in ['FS','PE','A','FT','FD','FF','G','I','PP','RB','FC','GC','CA','CV','SG','DD','DP','GS']:
	scouts = qualify(scouts,data, 7, 'uniform')

for data in ['variacao_num','jogos_num','tempo_jogado','nota','FS','PE','A','FT','FD','FF','G','I','PP','RB','FC','GC','CA','CV','SG','DD','DP','GS']:
	scouts = oneHotEncoding(scouts,data)

#print(scouts.sum()/len(scouts.index) > 0.9)

frequent_itens = apriori(scouts, min_support = 0.2, use_colnames = True, max_len = None, verbose = 0, low_memory = True)
rules = association_rules(frequent_itens, metric = "confidence", min_threshold = 0.8)
rules.sort_values(by=['support'], inplace = True, ascending = False)
print(rules)