import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# Reading csv's.
resultados = pd.read_csv("Csv's/2014_partidas.csv") 
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Merging csv's.
resultados.rename(columns = {'id':'partida_id'}, inplace = True) 
scouts = pd.merge(resultados,scouts, on = 'partida_id') 

# Dropping unnedded data.
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)
scouts = scouts.dropna()

# Dropping columns that doesn't help anymore.
scouts.drop(columns = ['rodada_x','rodada_y','clube_casa_id','clube_visitante_id',], inplace = True)

# Determining who won the match.
scouts['mandante'] = np.where(scouts['placar_oficial_mandante'] > scouts['placar_oficial_visitante'], 1,0)
scouts['visitante'] = np.where(scouts['placar_oficial_mandante'] < scouts['placar_oficial_visitante'], 1,0)
scouts['vencedor'] = np.where(scouts['visitante'] == scouts['mandante'], 0, scouts['mandante'] - scouts['visitante'])

# Dropping columns that doesn't help anymore.
scouts.drop(columns = ['placar_oficial_visitante', 'placar_oficial_mandante', 'mandante','visitante', 'atleta_id','clube_id','participou','jogos_num','pontos_num','media_num','preco_num','variacao_num',
	'titular','substituido','tempo_jogado','nota','posicao_id'
	,'A','G','GC','SG','GS'
	], inplace = True)

# Creating a column indicating if the player lost(-1), tied(0) or won(1) the game. 
scouts['vitoria'] = np.where(1,0,0)
scouts['vitoria'] = np.where((scouts['vencedor'] == 1) & (scouts['mando'] == 1), 1, scouts['vitoria'])
scouts['vitoria'] = np.where((scouts['vencedor'] == 1) & (scouts['mando'] == 0), -1, scouts['vitoria'])
scouts['vitoria'] = np.where(scouts['vencedor'] == 0, 0, scouts['vitoria'])
scouts['vitoria'] = np.where((scouts['vencedor'] == -1) & (scouts['mando'] == 0), 1, scouts['vitoria'])
scouts['vitoria'] = np.where((scouts['vencedor'] == -1) & (scouts['mando'] == 1), -1,scouts['vitoria'])

# Dropping unneed data.
scouts.drop(columns = ['mando', 'partida_id','vencedor'] , inplace = True)

# Getting the data for the RandomForestRegressor. (Without assists, goal, own-goals and clean sheets for an actual problem.)
x = np.column_stack((scouts.FS, scouts.PE, scouts.FT, scouts.FD, scouts.FF, scouts.I, scouts.PP, scouts.RB, scouts.FC, scouts.CA, scouts.CV, scouts.DD, scouts.DP
	#,scouts.A,scouts.G, scouts.GC, scouts.SG, scouts.GS
	))
y = scouts.vitoria

# Splitting the data for the regressor.
np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

# Training the regressor.
modelo = RandomForestRegressor(n_estimators = 1000, random_state = 42) #ramdom_state = 42 for replicable results.
modelo.fit(x_train,y_train)

# Getting it's predictions.
predictions = modelo.predict(x_test)

# The score.
print("Score = ", r2_score(predictions, y_test))
print("Mean Squared Error = ", mean_squared_error(predictions, y_test))

# Plotting the feature's importances.
features = scouts.drop(columns = 'vitoria')
feature_list = list(features.columns)
importancias = list(modelo.feature_importances_)
feature_importancias = [(feature, round(importancias, 2)) for feature, importancias in zip(feature_list, importancias)]
feature_importancias = sorted(feature_importancias, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importancias];

feat_importances = pd.Series(modelo.feature_importances_, index = features.columns)
feat_importances.nlargest(20).plot(kind='barh')
plt.title("Feature Importance RandomForestRegressor")
plt.tight_layout()
plt.grid()
plt.show()