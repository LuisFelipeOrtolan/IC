# Prever preços usando Random Forest Regressor.

# Imports.
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Reading csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Prepairing data.
scouts.drop(scouts[(scouts.pontos_num == None)].index, inplace = True)
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)

# Getting only one position.
# scouts.drop(scouts[(scouts.posicao_id != 1)].index, inplace = True)

scouts = (scouts-scouts.min()) / (scouts.max()-scouts.min())

scouts.drop(columns = ['posicao_id','clube_id','participou','jogos_num','variacao_num','media_num',
	'partida_id','mando','titular','substituido','tempo_jogado','nota', 'rodada'], inplace = True)


# Getting the data for the Random Forest Regressor.
x = np.column_stack((scouts.FS, scouts.PE, scouts.FF, scouts.PP, scouts.RB, scouts.FC, scouts.CA, scouts.CV,
	scouts.DD, scouts.DP, scouts.GS, scouts.GC, scouts.FT, scouts.I, scouts.FD, scouts.A,scouts.G, scouts.SG))
y = scouts.pontos_num

np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

# The Random Forest Regressor.
modelo = RandomForestRegressor(n_estimators = 300, random_state = 42) #ramdom_state = 42 for replicable results.
modelo.fit(x_train,y_train)

predictions = modelo.predict(x_test)

# The Score.
print("Mean Squared Error = ", mean_squared_error(y_test, predictions))
print("Score = ", r2_score(y_test, predictions))

# Getting the dataset's features.
features = scouts.drop(columns = ['atleta_id','preco_num', 'pontos_num'])
feature_list = list(features.columns)

# Getting the feature's importances.
importancias = list(modelo.feature_importances_)
feature_importancias = [(feature, round(importancias, 2)) for feature, importancias in zip(feature_list, importancias)]
feature_importancias = sorted(feature_importancias, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importancias];

# Plotting the feature's importances.
feat_importances = pd.Series(modelo.feature_importances_, index = features.columns)
feat_importances.nlargest(14).plot(kind='barh')
plt.show()

# Plotting the prediction's of the Random Forest Regressor for the original Dataset.
aux = scouts.drop(columns = ['atleta_id','preco_num', 'pontos_num'])
predicoes = modelo.predict(aux)
plot = {'predicoes':predicoes, 'atleta_id':scouts.atleta_id}
df = pd.DataFrame(plot, columns = ['predicoes','atleta_id'])
sns.violinplot( y=df["predicoes"] )
plt.title("Predictions using the original dataset")
plt.ylabel("Predictions")
plt.show()

# Testing the 2014's model in the 2015's data.
scouts2015 = pd.read_csv("Csv's/2015_scouts.csv")
treinadores = pd.read_csv("Csv's/2015_atletas.csv")

scouts2015 = scouts2015.dropna()
scouts2015 = scouts2015.dropna(axis = 1, how = 'all')
#scouts2015 = (scouts2015-scouts2015.min()) / (scouts2015.max()-scouts2015.min())

treinadores = treinadores.query("posicao_id == 6")
treinadores = list(treinadores['id'])

scouts2015 = scouts2015.loc[~scouts2015.atleta_id.isin(treinadores)]

scouts2015 = scouts2015.drop(columns = ['atleta_id', 'rodada','clube_id','jogos_num','variacao_num','media_num','preco_num'])

x = np.column_stack((scouts2015.FS, scouts2015.PE, scouts2015.FF, scouts2015.PP, scouts2015.RB, scouts2015.FC, scouts2015.CA, scouts2015.CV,
	scouts2015.DD, scouts2015.DP, scouts2015.GS, scouts2015.GC, scouts2015.FT, scouts2015.I, scouts2015.FD, scouts2015.A,scouts2015.G, scouts2015.SG))
y = scouts2015.pontos_num

predictions2015 = modelo.predict(x)

data = {'predict': predictions2015, 'real':y}
df = pd.DataFrame(data)

df['dif'] = df['real'] - df['predict']

print(df.sort_values(by = 'dif'))
print("Mean Squared Error for 2015: ", mean_squared_error(predictions2015,y))

print(modelo.score(x,y))