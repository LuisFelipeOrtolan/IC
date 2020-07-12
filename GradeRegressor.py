# Predict the grade of a player using his scouts.

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
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)

# Getting only one position.
# scouts.drop(scouts[(scouts.posicao_id != 5)].index, inplace = True)

# Dropping unneeded data.
scouts.drop(columns = ['atleta_id','preco_num','posicao_id','clube_id','participou','jogos_num','pontos_num','media_num',
	'partida_id','mando','titular','substituido','tempo_jogado','variacao_num', 'rodada'], inplace = True)

# Getting the data for the Random Forest Regressor.
x = np.column_stack((scouts.FS, scouts.PE, scouts.FF, scouts.PP, scouts.RB, scouts.FC, scouts.CA, scouts.CV, 
	scouts.FD, scouts.A,scouts.G, scouts.SG, scouts.GS, scouts.DD, scouts.DP, scouts.GC, scouts.FT, scouts.I, scouts.DD,scouts.DP,scouts.GS))
y = scouts.nota

# Splitting the data for regressor.
np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

# Training model.
modelo = RandomForestRegressor(n_estimators = 500, random_state = 42) #ramdom_state = 42 for replicable results.
modelo.fit(x_train, y_train)

# The Score.
predict = modelo.predict(x_test)
print("Score = ", r2_score(predict,y_test))
print("Mean Squared Error = ", mean_squared_error(predict, y_test))

# Getting the dataset's features.
features = scouts.drop(columns = ['nota'])
feature_list = list(features.columns)

# Getting the feature's importances.
importancias = list(modelo.feature_importances_)
feature_importancias = [(feature, round(importancias, 2)) for feature, importancias in zip(feature_list, importancias)]
feature_importancias = sorted(feature_importancias, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importancias];

# Plotting the feature importances
feat_importances = pd.Series(modelo.feature_importances_, index = features.columns)
feat_importances.nlargest(20).plot(kind='barh')
plt.title("Feature Importance Random Forest Regressor")
plt.tight_layout()
plt.grid()
plt.show()