import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, mean_squared_error
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA
from sklearn import manifold

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

# Removing any columns with negative attributes.
for cols in scouts_por_time_detalhado.columns.tolist()[1:]:
	if not (scouts_por_time_detalhado[scouts_por_time_detalhado[cols] < 0].empty):
		aux = scouts_por_time_detalhado[scouts_por_time_detalhado[cols] < 0]

index = aux.index.values.tolist()
scouts_por_time_detalhado.drop(scouts_por_time_detalhado.index[index], inplace = True)

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
plt.title("Elbow method for detailed data")
plt.tight_layout()
plt.grid()
plt.show()

# Using the silhouette model to try to discover the best number of clusters for the K-means algorithm.
sil = []
for k in range(2,11):
	kmeans = KMeans(n_clusters = k).fit(x)
	labels = kmeans.labels_
	sil.append(silhouette_score(x,labels, metric = 'euclidean'))

print("Original silhouette scoure: ",sil)

# Trying using the PCA to group better.

pca = PCA(n_components = int(x.shape[1]/10))

x_reduced = pca.fit_transform(x)

sil = []
for k in range(2,11):
	kmeans = KMeans(n_clusters = k).fit(x_reduced)
	labels = kmeans.labels_
	sil.append(silhouette_score(x,labels, metric = 'euclidean'))

print("PCA silhouette score: ", sil)

# Plotting the MDS graphic
mds = manifold.MDS(2, max_iter = 1000, n_init = 1)
Y = mds.fit_transform(x)
plt.scatter(Y[:,0], Y[:,1])
plt.title("MDS for detailed data")
plt.tight_layout()
plt.show()

# For scouts that every line has the scouts from a team added in the match:

# Opening csv.
scouts_detalhado = pd.read_csv("Csv's/scouts_detalhado.csv")


# Dropping unneeded data.
scouts_detalhado.drop(columns = ['clube_id','partida_id', 'pontos_num','preco_num','variacao_num', 'vencedor'], inplace = True)

# Removing any columns with negative attributes.
for cols in scouts_detalhado.columns.tolist()[1:]:
	if not (scouts_detalhado[scouts_detalhado[cols] < 0].empty):
		aux = scouts_detalhado[scouts_detalhado[cols] < 0]

index = aux.index.values.tolist()
scouts_detalhado.drop(scouts_detalhado.index[index], inplace = True)

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
plt.title("Elbow method for undetailed data")
plt.tight_layout()
plt.grid()
plt.show()

# Using the silhouette model to try to discover the best number of clusters for the K-means algorithm.
sil = []

for k in range(2,11):
	kmeans = KMeans(n_clusters = k).fit(x)
	labels = kmeans.labels_
	sil.append(silhouette_score(x,labels, metric = 'euclidean'))

print("Original silhouette scoure: ", sil)

# Trying using the PCA to group better.
pca = PCA(n_components = int(x.shape[1]/10))

x_reduced = pca.fit_transform(x)

sil = []
for k in range(2,11):
	kmeans = KMeans(n_clusters = k).fit(x_reduced)
	labels = kmeans.labels_
	sil.append(silhouette_score(x,labels, metric = 'euclidean'))

print("PCA silhouette score: ", sil)

# Plotting the MDS graphic
mds = manifold.MDS(2, max_iter = 1000, n_init = 1)
Y = mds.fit_transform(x)
plt.scatter(Y[:,0], Y[:,1])
plt.title("MDS for undetailed data")
plt.tight_layout()
plt.show()