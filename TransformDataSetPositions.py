# Code to transform the dataset from player's scouts to team's scouts by summing them and separating each position.

import pandas as pd

# Opening Csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")
vencedores = pd.read_csv("Csv's/2014_partidas.csv")

# Dropping Unneeded data.
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)
scouts.drop(columns = ['atleta_id','rodada','participou','jogos_num','media_num',
	'tempo_jogado','substituido', 'titular'], inplace = True)

# Creating a function that splits the scouts for each of the players positions in a match.
# Input: a dataframe from a match.
# Output: a dataframe from a match with scouts per players position.
def separaJogadores(partida_df):
	# Get the two teams ids.
	time1 = partida_df['clube_id'].unique()[0]
	time2 = partida_df['clube_id'].unique()[1]
	# Get the dataframe for each team.
	time1_df = partida_df.query("clube_id == @time1")
	time2_df = partida_df.query("clube_id == @time2")
	# Adding the scouts for every position.
	time1_df = time1_df.groupby('posicao_id').sum()
	time2_df = time2_df.groupby('posicao_id').sum()
	# Adjusting data.
	time1_df.loc[time1_df['mando'] > 0, 'mando'] = 1
	time2_df.loc[time2_df['mando'] > 0, 'mando'] = 1
	time1_df['partida_id'] = partida_df.partida_id.unique()[0]
	time2_df['partida_id'] = partida_df.partida_id.unique()[0]
	time1_df['clube_id'] = time1
	time2_df['clube_id'] = time2

	# Initiating the split for each position for team 1.
	dados = []
	# Getting the data for each position.
	for posicao in range(1,6):
		manipulacao = time1_df.query("posicao_id == @posicao")
		# Getting the name of each column for creating the columns for each position.
		colunas = list(manipulacao.columns)
		# Removing columns that wont be for each position.
		for item in ['clube_id', 'partida_id','mando']:
			colunas.remove(item)
		# For the each of the columns remaining:
		for item in colunas:
			# Rename the column with the original name of the column plus the number of the position
			manipulacao = manipulacao.rename(columns={item:item+'_'+str(int(posicao))})
			manipulacao.reset_index(drop = True, inplace = True)
		# This condition is here if a team has not a certain position in that match.
		# It creates all the columns but fills it with 0's.
		if(manipulacao.empty):
			manipulacao.loc[len(manipulacao)] = 0
			manipulacao.loc[len(manipulacao)-1,'clube_id'] = time1
			manipulacao.loc[len(manipulacao)-1,'partida_id'] = partida_df.partida_id.unique()[0]
			manipulacao.loc[len(manipulacao)-1,'mando'] = time1_df['mando'].unique()[0]
		# Finally, it puts in an array for future concat.
		dados.append(manipulacao)

	# Concat all the data, so a line will have all the scouts for each position in a single line.
	final_time1 = pd.concat([dados[0], dados[1], dados[2], dados[3], dados[4]], axis = 1)

	# Initiating the split for each position for team 2.
	dados = []
	# Getting the data for each position.
	for posicao in range(1,6):
		manipulacao = time2_df.query("posicao_id == @posicao")
		# Getting the name of each column for creating the columns for each position.
		colunas = list(manipulacao.columns)
		# Removing columns that wont be for each position.
		for item in ['clube_id', 'partida_id','mando']:
			colunas.remove(item)
		# For the each of the columns remaining:
		for item in colunas:
			# Rename the column with the original name of the column plus the number of the position
			manipulacao = manipulacao.rename(columns={item:item+'_'+str(int(posicao))})
			manipulacao.reset_index(drop = True, inplace = True)
		# This condition is here if a team has not a certain position in that match.
		# It creates all the columns but fills it with 0's.
		if(manipulacao.empty):
			manipulacao.loc[len(manipulacao)] = 0
			manipulacao.loc[len(manipulacao)-1,'clube_id'] = time2
			manipulacao.loc[len(manipulacao)-1,'partida_id'] = partida_df.partida_id.unique()[0]
			manipulacao.loc[len(manipulacao)-1,'mando'] = time2_df['mando'].unique()[0]
		# Finally, it puts in an array for future concat.
		dados.append(manipulacao)
	# Concat all the data, so a line will have all the scouts for each position in a single line.
	final_time2 = pd.concat([dados[0], dados[1], dados[2], dados[3], dados[4]], axis = 1)

	# Concat all the data from the two teams.
	final = pd.concat([final_time1, final_time2])
	# And return the dataframe.
	return final

# Gets the first match id.
primeira_partida = scouts['partida_id'].iloc[0]

# Initianilize the new dataframe with the positions for the first match.
scouts_detalhado = separaJogadores(scouts.query("partida_id == @primeira_partida"))
scouts.drop(scouts[scouts.partida_id == primeira_partida].index, inplace = True)

# Apply the function for the rest of the matches.
for partida in scouts.partida_id.unique():
	aux = separaJogadores(scouts.query("partida_id == @partida"))
	scouts_detalhado = pd.concat([scouts_detalhado,aux])

# Drop the dupplicate columns.
scouts_detalhado = scouts_detalhado.loc[:,~scouts_detalhado.columns.duplicated()]

# Sorting index.
scouts_detalhado.sort_values(by = 'partida_id', inplace = True)
scouts_detalhado.reset_index(drop = True, inplace = True)

print(scouts_detalhado)

# Exporting the dataframe to a csv.
scouts_detalhado.to_csv("Csv's/scouts_por_time_detalhado.csv", index = False)