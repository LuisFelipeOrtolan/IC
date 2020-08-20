# Agrupamento // Grouping

Aqui estão os resultados dos códigos relacionados a agrupamento. Knee Method for matches with positions detailed é um gráfico do "método do joelho" para tentar obter o número ideal de grupos para o algoritmo K-means, e o documento Knee Method for matches without positions detailed possui exatamente a mesma função, entretanto este segundo usa dados sem a descrição de posições nos dados de scout. Não é claro um ponto de inflexão para determinar o melhor grupo.

Existe o documento silhouette que contém a silhueta na tentativa de obter o melhor número de grupos. O primeiro vetor é o resultado aplicado em grupos de 2 a 10 sobre os dados originais. O segundo vetor é usado sobre o dataset aplicando Principal Component Analysis(PCA), no mesmo intervalo. 

Os outros dois gráficos (MDS for matches with position detailed e MDS for matches without position detailed) são gráficos Multi-dimensional scaling(MDS), que transformam os pontos no espaço em pontos no plano, mantendo suas distâncias relativas, para observar se é possível identificar grupos. Em ambos os casos, não existe uma distinção clara de grupos.

//

Here are the results for the grouping codes.  Knee Method for matches with positions detailed is a graphic of the "knee method", which is to discover the best number of clusters for the K-means algorithm, and Knee Method for matches without positions detailed is the same exact graphic, but this one use the database without the description of scout's positions. Isnt clear which is the best number of clusters in both graphics.

There is also a document called silhouette which has the results from using the silhouette method in the dataset. The first vector is the result in the original dataset for 2 to 10 clusters. The second vector is in the same interval, but applying the Principal Component Analysis(PCA) first. 

The other two graphics (MDS for matches with position detailed e MDS for matches without position detailed) are Multi-dimensional scaling graphics(MDS). It transforms points in space to points in plane, mantaining the relative distance between them, to help observe if there are clusters in that dataset. In both cases, there is no clusters easy to be seen.

