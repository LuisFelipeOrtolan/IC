# Prever nota usando Random Forest Regressor

# Imports.
import pandas as pd 
import numpy as np
import scipy as sp
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# Reading csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Prepairing data.
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)

# Getting only one position.
# scouts.drop(scouts[(scouts.posicao_id != 5)].index, inplace = True)

scouts = (scouts-scouts.min()) / (scouts.max()-scouts.min())
scouts.drop(columns = ['posicao_id','clube_id','participou','jogos_num','pontos_num','media_num',
	'partida_id','mando','titular','substituido','tempo_jogado','variacao_num', 'rodada'], inplace = True)
scouts = scouts.dropna(axis = 1, how = 'all')

# Getting the data for the Random Forest Regressor.
x = np.column_stack((scouts.FS, scouts.PE, scouts.FF, scouts.PP, scouts.RB, scouts.FC, scouts.CA, scouts.CV, 
	scouts.FD, scouts.A,scouts.G, scouts.SG,scouts.FT, scouts.I, scouts.GS, scouts.DD, scouts.DP, scouts.GC))
y = scouts.nota

modelo = RandomForestRegressor(n_estimators = 18, random_state = 42) #ramdom_state = 42 for replicable results.
modelo.fit(x,y)

# The Score.
print("RF = ", modelo.score(x,y))

# Getting the dataset's features.
features = scouts.drop(columns = ['atleta_id','preco_num', 'nota'])
feature_list = list(features.columns)

# Getting the feature's importances.
importancias = list(modelo.feature_importances_)
feature_importancias = [(feature, round(importancias, 2)) for feature, importancias in zip(feature_list, importancias)]
feature_importancias = sorted(feature_importancias, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importancias];

feat_importances = pd.Series(modelo.feature_importances_, index = features.columns)
feat_importances.nlargest(14).plot(kind='barh')
plt.show()