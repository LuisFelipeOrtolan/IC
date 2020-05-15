import pandas as pd
import numpy as np

# Opening Csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")
vencedores = pd.read_csv("Csv's/2014_partidas.csv")

# Dropping Unneeded data.
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)
scouts.drop(columns = ['atleta_id','rodada','participou','jogos_num','media_num',
	'tempo_jogado','substituido', 'titular'], inplace = True)

def separaJogadores(partida_df):

	time1 = partida_df['clube_id'].unique()[0]
	time2 = partida_df['clube_id'].unique()[1]

	time1_df = partida_df.query("clube_id == @time1")
	time2_df = partida_df.query("clube_id == @time2")

	time1_df = time1_df.groupby('posicao_id').sum()
	time2_df = time2_df.groupby('posicao_id').sum()

	time1_df.loc[time1_df['mando'] > 0, 'mando'] = 1
	time2_df.loc[time2_df['mando'] > 0, 'mando'] = 1

	time1_df['partida_id'] = partida_df.partida_id.unique()[0]
	time2_df['partida_id'] = partida_df.partida_id.unique()[0]

	time1_df['clube_id'] = time1
	time2_df['clube_id'] = time2

	dados = []
	for posicao in time1_df.index:
		manipulacao = time1_df.query("posicao_id == @posicao")
		colunas = list(manipulacao.columns)
		for item in ['clube_id', 'partida_id','mando']:
			colunas.remove(item)
		
		for item in colunas:
			manipulacao = manipulacao.rename(columns={item:item+'_'+str(int(posicao))})
			manipulacao.reset_index(drop = True, inplace = True)
		dados.append(manipulacao)
	
	final_time1 = pd.concat([dados[0], dados[1], dados[2], dados[3], dados[4]], axis = 1)

	dados = []
	for posicao in time2_df.index:
		manipulacao = time2_df.query("posicao_id == @posicao")
		colunas = list(manipulacao.columns)
		for item in ['clube_id', 'partida_id','mando']:
			colunas.remove(item)
		
		for item in colunas:
			manipulacao = manipulacao.rename(columns={item:item+'_'+str(int(posicao))})
			manipulacao.reset_index(drop = True, inplace = True)
		dados.append(manipulacao)

	final_time2 = pd.concat([dados[0], dados[1], dados[2], dados[3], dados[4]], axis = 1)
	final = pd.concat([final_time1, final_time2])
	return final


primeira_partida = scouts['partida_id'].iloc[0]

scouts_detalhado = separaJogadores(scouts.query("partida_id == @primeira_partida"))
scouts.drop(scouts[scouts.partida_id == primeira_partida].index, inplace = True)

for partida in scouts.partida_id.unique():
	aux = separaJogadores(scouts.query("partida_id == @partida"))
	scouts_detalhado = pd.concat([scouts_detalhado,aux])

scouts_detalhado = scouts_detalhado.loc[:,~scouts_detalhado.columns.duplicated()]
scouts_detalhado.sort_values(by = 'partida_id', inplace = True)
scouts_detalhado.reset_index(drop = True, inplace = True)
print(scouts_detalhado)