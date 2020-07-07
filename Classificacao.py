import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

scouts = pd.read_csv("Csv's/scouts_detalhado.csv")
scouts_posicao = pd.read_csv("Csv's/scouts_por_time_detalhado.csv")

scouts_posicao['vencedor'] = scouts['vencedor']

scouts.drop(columns = ['clube_id', 'pontos_num', 'preco_num','variacao_num', 'G', 'A', 'SG', 'GC','GS','nota'], inplace = True)

columns = []

for column in scouts.drop(columns = ['partida_id', 'mando', 'vencedor']).columns:
	columns.append(str(column)+'_home')

for column in scouts.drop(columns = ['partida_id', 'mando', 'vencedor']).columns:
	columns.append(str(column)+'_away')

columns.append('vencedor')
new_scouts = pd.DataFrame(columns = columns)

for partida in scouts['partida_id'].unique():
	home = scouts.query("partida_id == @partida").query("mando == 1")
	win_home = int(home['vencedor'])
	home.drop(columns = ['partida_id','mando','vencedor'], inplace = True)
	home.reset_index(drop = True, inplace = True)
	for column in home.columns:
		home.rename(columns = {column:column+'_home'}, inplace = True)
	away = scouts.query("partida_id == @partida").query("mando == 0")
	win_away = int(away['vencedor'])
	away.drop(columns = ['partida_id','mando','vencedor'], inplace = True)
	away.reset_index(drop = True, inplace = True)
	for column in away.columns:
		away.rename(columns = {column:column+'_away'}, inplace = True)
	result = pd.concat([home,away], axis = 1)
	if win_home == 1:
		result['vencedor'] = 1
	else:
		if win_away == 1:
			result['vencedor'] = -1
		else:
			result['vencedor'] = 0
	new_scouts = new_scouts.append(result)
	

x = new_scouts.drop(columns = ['vencedor']).reset_index(drop = True).values
y = new_scouts['vencedor']
y = y.astype('int')

np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

classifier = RandomForestClassifier()
classifier.fit(x_train, y_train)

predictions = classifier.predict(x_test)

print("Accuracy = ", accuracy_score(predictions, y_test))

# Getting the dataset's features.
features = new_scouts.drop(columns = ['vencedor'])
feature_list = list(features.columns)

# Getting the feature's importances.
importancias = list(classifier.feature_importances_)
feature_importancias = [(feature, round(importancias, 2)) for feature, importancias in zip(feature_list, importancias)]
feature_importancias = sorted(feature_importancias, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importancias];

# Plotting the feature's importances.
feat_importances = pd.Series(classifier.feature_importances_, index = features.columns)
feat_importances.nlargest(50).plot(kind='barh')
plt.title("Feature Importance of Random Forest Classifier")
plt.tight_layout()
plt.grid()
plt.show()

scouts_posicao.drop(columns = ['clube_id'], inplace = True)

for posicao in range(1,6):
	colunas = ['pontos_num_','preco_num_','variacao_num_', 'G_', 'A_', 'SG_', 'GC_', 'GS_','nota_']
	new_colunas = []
	for item in colunas:
		new_colunas.append(item+str(posicao))
	scouts_posicao.drop(columns = new_colunas, inplace = True)

columns = []

for column in scouts_posicao.drop(columns = ['partida_id', 'mando', 'vencedor']).columns:
	columns.append(str(column)+'_home')

for column in scouts_posicao.drop(columns = ['partida_id', 'mando', 'vencedor']).columns:
	columns.append(str(column)+'_away')

columns.append('vencedor')
new_scouts = pd.DataFrame(columns = columns)

for partida in scouts_posicao['partida_id'].unique():
	home = scouts_posicao.query("partida_id == @partida").query("mando == 1")
	win_home = int(home['vencedor'])
	home.drop(columns = ['partida_id','mando','vencedor'], inplace = True)
	home.reset_index(drop = True, inplace = True)
	for column in home.columns:
		home.rename(columns = {column:column+'_home'}, inplace = True)
	away = scouts_posicao.query("partida_id == @partida").query("mando == 0")
	win_away = int(away['vencedor'])
	away.drop(columns = ['partida_id','mando','vencedor'], inplace = True)
	away.reset_index(drop = True, inplace = True)
	for column in away.columns:
		away.rename(columns = {column:column+'_away'}, inplace = True)
	result = pd.concat([home,away], axis = 1)
	if win_home == 1:
		result['vencedor'] = 1
	else:
		if win_away == 1:
			result['vencedor'] = -1
		else:
			result['vencedor'] = 0
	new_scouts = new_scouts.append(result)
	

x = new_scouts.drop(columns = ['vencedor']).reset_index(drop = True).values
y = new_scouts['vencedor']
y = y.astype('int')

np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

classifier = RandomForestClassifier()
classifier.fit(x_train, y_train)

predictions = classifier.predict(x_test)

print("Accuracy = ", accuracy_score(predictions, y_test))

# Getting the dataset's features.
features = new_scouts.drop(columns = ['vencedor'])
feature_list = list(features.columns)

# Getting the feature's importances.
importancias = list(classifier.feature_importances_)
feature_importancias = [(feature, round(importancias, 2)) for feature, importancias in zip(feature_list, importancias)]
feature_importancias = sorted(feature_importancias, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importancias];

# Plotting the feature's importances.
feat_importances = pd.Series(classifier.feature_importances_, index = features.columns)
feat_importances.nlargest(50).plot(kind='barh')
plt.title("Feature Importance Random Forest Classifier")
plt.tight_layout()
plt.grid()
plt.show()