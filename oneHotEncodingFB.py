# One Hot Encoding.

# Imports.
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

pd.set_option('display.max_rows', None)

# Function to qualify the data in the dataframe
def qualify(dataframe, name, quantity, strategy):
	est = KBinsDiscretizer(n_bins=[quantity], encode = 'ordinal', strategy = strategy)
	dataframe[name] = est.fit_transform(dataframe[[name]])
	return dataframe

def oneHotEncoding(dataframe, name):
	dataframe[name] = pd.Categorical(dataframe[name])
	dataframe = pd.get_dummies(dataframe, prefix = [name])
	return dataframe
	
# Opening Csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Dropping Unneeded data.
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.participou != 1)].index , inplace = True)
scouts.drop(scouts[(scouts.posicao_id != 3)].index, inplace = True)
scouts.drop(columns = ['rodada','clube_id','atleta_id','participou','preco_num',
	'pontos_num','media_num','partida_id', 'posicao_id'], inplace = True)

# Qualifying data in the dataframe.
for data in ['variacao_num','jogos_num']:
	scouts = qualify(scouts,data, 5, 'quantile')
for data in ['tempo_jogado','nota']:
	scouts = qualify(scouts,data, 3, 'uniform')
for data in ['FS','PE','A','FT','FD','FF','G','I','PP','RB','FC','GC','DD','DP','GS']:
	scouts = qualify(scouts,data, 7, 'uniform')

for data in ['variacao_num','jogos_num','tempo_jogado','nota','FS','PE','A','FT','FD','FF','G','I','PP','RB','FC','GC','DD','DP','GS']:
	scouts = oneHotEncoding(scouts,data)

# Dropping columns wih support over 90%.
scouts.drop(columns = ['titular','tempo_jogado_2.0','A_0.0','FT_0.0','FD_0.0','G_0.0','I_0.0','PP_0.0','GC_0.0','DD_0.0','DP_0.0','GS_0.0'], inplace = True)

frequent_itens = apriori(scouts, min_support = 0.2, use_colnames = True, max_len = None, verbose = 0, low_memory = True)
rules = association_rules(frequent_itens, metric = "confidence", min_threshold = 0.8)

rules.to_excel("Laterais.xlsx")
