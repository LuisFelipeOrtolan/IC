import pandas as pd 

# Opening Csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")
vencedores = pd.read_csv("Csv's/2014_partidas.csv")

# Dropping Unneeded data.
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)
scouts.drop(columns = ['atleta_id','rodada','participou','posicao_id','jogos_num','media_num',
	'tempo_jogado','substituido', 'titular'], inplace = True)

# time = axis 1
def separaPartida(partida):
	global scouts
	partida2 = scouts.query("partida_id == @partida")
	parti = partida2.groupby('clube_id').sum()
	parti = parti.reset_index()
	parti['partida_id'] = partida
	scouts.drop(scouts[scouts.partida_id == partida].index, inplace = True)
	scouts = pd.concat([parti,scouts])

for partida in scouts.partida_id.unique():
	separaPartida(partida)

scouts.sort_values(by = 'partida_id', inplace = True)
scouts.reset_index(drop = True, inplace = True)
print(scouts)