import pandas as pd 
import numpy as np
import scipy as sp
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# Reading csv's.
resultados = pd.read_csv("Csv's/2014_partidas.csv") 
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Merging csv's.
resultados.rename(columns = {'id':'partida_id'}, inplace = True) 
scouts = pd.merge(resultados,scouts, on = 'partida_id') 

# Dropping managers.
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)

# Dropping unnedded data.
scouts.drop(scouts[(scouts.FS == 0) & (scouts.PE == 0) & (scouts.FT == 0) & (scouts.FD == 0) & (scouts.FF == 0) 
	& (scouts.I == 0) & (scouts.PP == 0) & (scouts.RB == 0) & (scouts.FC == 0)
	& (scouts.A) & (scouts.G) & (scouts.GC) & (scouts.SG) & (scouts.GS)
	& (scouts.CA == 0) & (scouts.CV == 0) & (scouts.DD == 0) & (scouts.DP == 0)].index, inplace = True)
scouts=(scouts-scouts.min())/(scouts.max()-scouts.min())
scouts = scouts.dropna()

# Dropping columns that doesn't help anymore.
scouts.drop(columns = ['rodada_x','rodada_y','clube_casa_id','clube_visitante_id'], inplace = True)

# Determining who won the match.
scouts['mandante'] = np.where(scouts['placar_oficial_mandante'] > scouts['placar_oficial_visitante'], 1,0)
scouts['visitante'] = np.where(scouts['placar_oficial_mandante'] < scouts['placar_oficial_visitante'], 1,0)
scouts['vencedor'] = np.where(scouts['visitante'] == scouts['mandante'], 0, scouts['mandante'] - scouts['visitante'])

# Dropping columns that doesn't help anymore.
scouts.drop(columns = ['placar_oficial_visitante', 'placar_oficial_mandante', 'mandante','visitante', 'atleta_id','clube_id','participou','jogos_num','pontos_num','media_num','preco_num','variacao_num',
	'titular','substituido','tempo_jogado','nota','posicao_id'
	,'A','G','GC','SG','GS'
	], inplace = True)

scouts['vitoria'] = np.where(1,0,0)
scouts['vitoria'] = np.where((scouts['vencedor'] == 1) & (scouts['mando'] == 1), 1, scouts['vitoria'])
scouts['vitoria'] = np.where((scouts['vencedor'] == 1) & (scouts['mando'] == 0), -1, scouts['vitoria'])
scouts['vitoria'] = np.where(scouts['vencedor'] == 0, 0, scouts['vitoria'])
scouts['vitoria'] = np.where((scouts['vencedor'] == -1) & (scouts['mando'] == 0), 1, scouts['vitoria'])
scouts['vitoria'] = np.where((scouts['vencedor'] == -1) & (scouts['mando'] == 1), -1,scouts['vitoria'])

scouts.drop(columns = ['mando', 'partida_id','vencedor'] , inplace = True)


x = np.column_stack((scouts.FS, scouts.PE, scouts.FT, scouts.FD, scouts.FF, scouts.I, scouts.PP, scouts.RB, scouts.FC, scouts.CA, scouts.CV, scouts.DD, scouts.DP
	#,scouts.A,scouts.G, scouts.GC, scouts.SG, scouts.GS
	))
y = scouts.vitoria

modelo = RandomForestRegressor(n_estimators = 1000, random_state = 42) #ramdom_state = 42 for replicable results.
modelo.fit(x,y)
print("RF = ", modelo.score(x,y))

features = scouts.drop(columns = 'vitoria')
feature_list = list(features.columns)
importancias = list(modelo.feature_importances_)
feature_importancias = [(feature, round(importancias, 2)) for feature, importancias in zip(feature_list, importancias)]
feature_importancias = sorted(feature_importancias, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importancias];

