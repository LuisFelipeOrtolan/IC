# Code to use Classifier in the dataset.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Import datasets.
scouts = pd.read_csv("Csv's/scouts_matches.csv")
scouts_posicao = pd.read_csv("Csv's/scouts_matches_positions.csv")

# First, the classifier will be used in the dataset with no differentiation between positions.

# Copying the winner column from one dataframe to another.
scouts_posicao['vencedor'] = scouts['vencedor']

# Dropping unneeded data for the classifier.
scouts.drop(columns = ['clube_id', 'pontos_num', 'preco_num','variacao_num', 'G', 'A', 'SG', 'GC','GS','nota'], inplace = True)

# Groupping the two teams from a match in a single row.
columns = []
# Getting the home columns.
for column in scouts.drop(columns = ['partida_id', 'mando', 'vencedor']).columns:
	columns.append(str(column)+'_home')
# Getting the away columns.
for column in scouts.drop(columns = ['partida_id', 'mando', 'vencedor']).columns:
	columns.append(str(column)+'_away')
# And finally adding a winner column.
columns.append('vencedor')
# Creating the dataframe with the away and home columns.
new_scouts = pd.DataFrame(columns = columns)

# Getting the data from every match to the new scouts dataframe.
for partida in scouts['partida_id'].unique():
	# Getting the data from the home team.
	home = scouts.query("partida_id == @partida").query("mando == 1")
	win_home = int(home['vencedor'])
	home.drop(columns = ['partida_id','mando','vencedor'], inplace = True)
	home.reset_index(drop = True, inplace = True)
	for column in home.columns:
		home.rename(columns = {column:column+'_home'}, inplace = True)
	# Getting the data from the away team.
	away = scouts.query("partida_id == @partida").query("mando == 0")
	win_away = int(away['vencedor'])
	away.drop(columns = ['partida_id','mando','vencedor'], inplace = True)
	away.reset_index(drop = True, inplace = True)
	for column in away.columns:
		away.rename(columns = {column:column+'_away'}, inplace = True)
	# Merging the two teams in a single row.
	result = pd.concat([home,away], axis = 1)
	# Getting the data for the winner column.
	if win_home == 1:
		result['vencedor'] = 1
	else:
		if win_away == 1:
			result['vencedor'] = -1
		else:
			result['vencedor'] = 0
	new_scouts = new_scouts.append(result)
	
# The scouts are the input in the Classifier and the winner column is what's supposed to be classified.
x = new_scouts.drop(columns = ['vencedor']).reset_index(drop = True).values
y = new_scouts['vencedor']
y = y.astype('int')

np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

# Training the classifier.
classifier = RandomForestClassifier()
classifier.fit(x_train, y_train)

# Getting it's predictions.
predictions = classifier.predict(x_test)

# The score for the classifier.
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

# Now the classifier will be used in the dataset with differentiation between positions.

# Dropping unneeded data.
scouts_posicao.drop(columns = ['clube_id'], inplace = True)
for posicao in range(1,6):
	colunas = ['pontos_num_','preco_num_','variacao_num_', 'G_', 'A_', 'SG_', 'GC_', 'GS_','nota_']
	new_colunas = []
	for item in colunas:
		new_colunas.append(item+str(posicao))
	scouts_posicao.drop(columns = new_colunas, inplace = True)

# Groupping the two teams from a match in a single row.
columns = []
# Getting the home columns.
for column in scouts_posicao.drop(columns = ['partida_id', 'mando', 'vencedor']).columns:
	columns.append(str(column)+'_home')
# Getting the away columns.
for column in scouts_posicao.drop(columns = ['partida_id', 'mando', 'vencedor']).columns:
	columns.append(str(column)+'_away')
# And finally adding a winner column.
columns.append('vencedor')
# Creating the dataframe with the away and home columns.
new_scouts = pd.DataFrame(columns = columns)

# Getting the data from every match to the new scouts dataframe.
for partida in scouts_posicao['partida_id'].unique():
	# Getting the data from the home team.
	home = scouts_posicao.query("partida_id == @partida").query("mando == 1")
	win_home = int(home['vencedor'])
	home.drop(columns = ['partida_id','mando','vencedor'], inplace = True)
	home.reset_index(drop = True, inplace = True)
	for column in home.columns:
		home.rename(columns = {column:column+'_home'}, inplace = True)
	# Getting the data from the away team.
	away = scouts_posicao.query("partida_id == @partida").query("mando == 0")
	win_away = int(away['vencedor'])
	away.drop(columns = ['partida_id','mando','vencedor'], inplace = True)
	away.reset_index(drop = True, inplace = True)
	for column in away.columns:
		away.rename(columns = {column:column+'_away'}, inplace = True)
	# Merging the two teams in a single row.
	result = pd.concat([home,away], axis = 1)
	# Getting the data for the winner column.
	if win_home == 1:
		result['vencedor'] = 1
	else:
		if win_away == 1:
			result['vencedor'] = -1
		else:
			result['vencedor'] = 0
	new_scouts = new_scouts.append(result)
	
# The scouts are the input in the Classifier and the winner column is what's supposed to be classified.
x = new_scouts.drop(columns = ['vencedor']).reset_index(drop = True).values
y = new_scouts['vencedor']
y = y.astype('int')

np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

# Training the classifier.
classifier = RandomForestClassifier()
classifier.fit(x_train, y_train)

# Getting it's predictions.
predictions = classifier.predict(x_test)

# The score for the classifier.# Getting it's predictions.
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