import pandas as pd

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

	print(time1_df)
	print(time2_df)
	
def separaPartida(partida):
	global scouts
	partida2 = scouts.query("partida_id == @partida")
	separaJogadores()
	parti = partida2.groupby('clube_id').sum()
	parti = parti.reset_index()
	parti['partida_id'] = partida
	parti.loc[parti['mando'] > 0, 'mando'] = 1
	scouts.drop(scouts[scouts.partida_id == partida].index, inplace = True)
	scouts = pd.concat([parti,scouts])

separaJogadores(scouts.query("partida_id == 179872"))