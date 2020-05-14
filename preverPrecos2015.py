import pandas as pd 
import numpy as np
import scipy as sp
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# Opening csv's.
scouts = pd.read_csv("Csv's/2015_scouts.csv")
atletas = pd.read_csv("Csv's/2015_atletas.csv")

# Merging csv's to get the athletes positions.
atletas.rename(columns = {'id':'atleta_id'}, inplace = True) 
scouts = pd.merge(scouts,atletas, on = 'atleta_id')

# Removing the managers.
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)

# Removing information that is no longer needed.
scouts.drop(columns = ['apelido','clube_id_y','preco_num','media_num','pontos_num','jogos_num','rodada','posicao_id','clube_id_x','atleta_id'], inplace = True)

# Preparing the data
scouts = scouts.dropna()
scouts = (scouts-scouts.min()) / (scouts.max()-scouts.min())
scouts = scouts.dropna(axis = 1, how = 'all')

# Getting the dataframe's features
features = scouts.drop(columns = ['variacao_num'])
feature_list = list(features.columns)

# Getting the information for the Random Forest Regressor
x = np.column_stack((scouts.FS, scouts.PE, scouts.FF, scouts.PP, scouts.RB, scouts.FC, scouts.CA, scouts.CV,
	scouts.DD, scouts.DP, scouts.GS, scouts.GC,scouts.FT, scouts.I, scouts.FD, scouts.A,scouts.G, scouts.SG))
y = scouts.variacao_num

# The Random Forest Regressor
modelo = RandomForestRegressor(n_estimators = 18, random_state = 42)
modelo.fit(x,y)

# The Score
print(modelo.score(x,y))
importancias = list(modelo.feature_importances_)
feature_importancias = [(feature, round(importancias, 2)) for feature, importancias in zip(feature_list, importancias)]
feature_importancias = sorted(feature_importancias, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importancias];