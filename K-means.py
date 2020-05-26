import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import mean_squared_error

# For scouts that every line has the scouts from every position in a match:

# Opening csv.
scouts_por_time_detalhado = pd.read_csv("Csv's/scouts_por_time_detalhado.csv")

# Dropping unneeded data.
scouts_por_time_detalhado.drop(columns = ['clube_id','partida_id'], inplace = True)
for posicao in range(1,6):
	colunas = ['pontos_num_','preco_num_','variacao_num_']
	new_colunas = []
	for item in colunas:
		new_colunas.append(item+str(posicao))
	scouts_por_time_detalhado.drop(columns = new_colunas, inplace = True)

# Transforming the dataframe in an array.
x = scouts_por_time_detalhado.reset_index(drop = True).values

# Creating an auxiliar array.
values = []

# Using the "knee" method to try to discover the best number of cluster for the K-means algorithm.	
for n in range(2,60):
	kmeans = KMeans(n_clusters = n).fit(x)	
	dif = 0
	# Calculating the mean squared error for every point in x compared to the cluster that was predicted for this point..
	for k in range(0,kmeans.labels_.size):
		dif += mean_squared_error(x[k], kmeans.cluster_centers_[kmeans.labels_[k]])
	values.append(dif)

# Plot the mean squared error for every number of clusters.
plt.plot(list(range(2,60)),values)
plt.show()

# Using the silhouette model to try to discover the best number of clusters for the K-means algorithm.
sil = []
for k in range(2,11):
	kmeans = KMeans(n_clusters = k).fit(x)
	labels = kmeans.labels_
	sil.append(silhouette_score(x,labels, metric = 'euclidean'))

print(sil)

# For scouts that every line has the scouts from a team added in the match:

# Opening csv.
scouts_detalhado = pd.read_csv("Csv's/scouts_detalhado.csv")

# Dropping unneeded data.
scouts_detalhado.drop(columns = ['clube_id','partida_id', 'pontos_num','preco_num','variacao_num'], inplace = True)

# Transforming the dataframe in an array.
x = scouts_detalhado.reset_index(drop = True).values

# Creating an auxiliar array.
values = []

# Using the "knee" method to try to discover the best number of cluster for the K-means algorithm.	
for n in range(2,60):
	kmeans = KMeans(n_clusters = n).fit(x)	
	dif = 0
	# Calculating the mean squared error for every point in x compared to the cluster that was predicted for this point..
	for k in range(0,kmeans.labels_.size):
		dif += mean_squared_error(x[k], kmeans.cluster_centers_[kmeans.labels_[k]])
	values.append(dif)

# Plot the mean squared error for every number of clusters.
plt.plot(list(range(2,60)),values)
plt.show()

# Using the silhouette model to try to discover the best number of clusters for the K-means algorithm.
sil = []
for k in range(2,11):
	kmeans = KMeans(n_clusters = k).fit(x)
	labels = kmeans.labels_
	sil.append(silhouette_score(x,labels, metric = 'euclidean'))

print(sil)