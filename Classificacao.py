import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

scouts = pd.read_csv("Csv's/scouts_detalhado.csv")
scouts_posicao = pd.read_csv("Csv's/scouts_por_time_detalhado.csv")

scouts_posicao['vencedor'] = scouts['vencedor']

scouts.drop(columns = ['clube_id', 'pontos_num', 'preco_num','variacao_num', 'partida_id', 'G', 'A', 'SG', 'GC','GS'], inplace = True)

x = scouts.drop(columns = ['vencedor']).reset_index(drop = True).values
y = scouts['vencedor']

np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

classifier = RandomForestClassifier()
classifier.fit(x_train, y_train)

predictions = classifier.predict(x_test)

print("R2 = ", accuracy_score(predictions, y_test))


scouts_posicao.drop(columns = ['clube_id','partida_id'], inplace = True)

for posicao in range(1,6):
	colunas = ['pontos_num_','preco_num_','variacao_num_', 'G_', 'A_', 'SG_', 'GC_', 'GS_']
	new_colunas = []
	for item in colunas:
		new_colunas.append(item+str(posicao))
	scouts_posicao.drop(columns = new_colunas, inplace = True)

x = scouts_posicao.drop(columns = ['vencedor']).reset_index(drop = True).values
y = scouts_posicao['vencedor']

np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

classifier = RandomForestClassifier()
classifier.fit(x_train, y_train)

predictions = classifier.predict(x_test)

print("R2 = ", accuracy_score(predictions, y_test))