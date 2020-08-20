# Descoberta de Conhecimento em Dados de Scout do Campeonato Brasileiro de Futebol // Knowledge Discovery in Brazilian Football Championship Scout Data

Esse repositório contém os códigos usados durante a pesquisa de Iniciação Científica PIBIC 2019/2020 do dono deste repositório.

Na pasta Csv's estão os arquivos da base de dados usada durante a pesquisa, além de novas base de dados criadas para melhorar o desempenho dos códigos (essas distinções estão explicadas no Readme dentro da pasta).

Na pasta Results estão os resultados obtidos durante os experimentos, divididos pela categoria do experimento.

Os arquivos AssociationRules são os códigos usados para gerar regras de associação para, respectivamente, todos os jogadores, atacantes, zagueiros, laterais, goleiros e meias.

O arquivo Classifier mostra o código usado para tentar usar dados de scout para classificar se um time venceu, empatou ou perdeu a partida.

Os arquivos GradeLinearRegressor e GradeRegressor são os códigos usados para aplicar respectivamente Regressor Linear e Random Forest Regressor nas notas dos jogadores. Os arquivos PointsLinearRegressor e PointsRegressor são os códigos usados para aplicar respectivamente Regressor Linear e Random Forest Regressor nas pontuações do CartolaFC dos jogadores. Além desses arquivos, ainda há mais um código usado para aplicar regressor que é o WinnerRegressor, que aplica Random Forest Regressor para descobrir se um jogador ganhou uma partida.

O arquivo Grouping é o código usado para agrupar partidas usando o algoritmo K-means. Além disso, no código são testados diversos números de grupos para observar se é possível agrupar esses dados.

Os arquivos TransformDataset e TransformDatasetPositions são códigos usados para transformar o Dataset original em que cada linha correspondia aos scouts de um atleta em uma determinada partida em linhas que correspondessem a times em uma partida específica. O primeiro arquivo ignora que existam posições diferentes, enquanto o segundo divide cada scout por posição, transformando o atributo gol em gol de goleiro, gol de lateral, etc.

//

This repository contains the codes used in the PIBIC 2019/2020 Scientific Initiation of the owner of this repository.

In the folder Csv's are the datasets used in this research and new datasets built from the original one to improve codes performances (To see which is whic, check the Readme inside the folder).

In the folder Results there are the results obtained throughout the experiments, they are separated by type of experiment.

The files AssociationRules are the codes used to obtain the Association Rules for the following positions: All positions, Attackers, Centrebacks, Fullbacks, Goalkeepers and Midfielders.

The file Classifier is the code used to classify if a team won, tied or lost a game based in it's scouts.

The files GradeLinearRegressor and GradeRegressor are the codes used to apply Linear Regressor and Random Forest Regressor in player's grades. The files PointsLinearRegressor and PointsRegressor are the codes used to apply Linear Regressor and Random Forest Regressor in player's points in the CartolaFC game. Finally, the WinnerRegressor file is a code to apply Random Forest Regressor to try to figure if the player won, tied or lost the game.

The file Grouping is the code used to group the matches using the K-means algorithm. Besides, in the code, several numbers of clusters are tried to see if it is possible to group the matches.

The files TransformDataset and TransformDatasetPositions are codes to transform the original dataset. In the original dataset, every row represents a player in a single match. In the new datasets, every row represents a team in a single match. The first file ignores that there are multiple positions, while the second one acknowledges that by transforming an attribute like goal in five attributes (goal scored by goalkeeper, goal scored by centrebacks...).
