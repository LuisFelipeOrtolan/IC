import pandas as pd 

# Opening Csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")
vencedores = pd.read_csv("Csv's/2014_partidas.csv")

# Dropping Unneeded data.
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)
scouts.drop(columns = ['atleta_id','rodada','participou','posicao_id','jogos_num','media_num',
	'tempo_jogado','substituido', 'titular'], inplace = True)

def separaPartida(partida):
	global scouts
	partida2 = scouts.query("partida_id == @partida")
	parti = partida2.groupby('clube_id').sum()
	parti = parti.reset_index()
	parti['partida_id'] = partida
	parti.loc[parti['mando'] > 0, 'mando'] = 1
	scouts.drop(scouts[scouts.partida_id == partida].index, inplace = True)
	scouts = pd.concat([parti,scouts])

for partida in scouts.partida_id.unique():
	separaPartida(partida)

scouts.sort_values(by = 'partida_id', inplace = True)
scouts.reset_index(drop = True, inplace = True)

vencedores['vencedor'] = vencedores['placar_oficial_mandante'] - vencedores['placar_oficial_visitante']
vencedores.drop(columns = ['placar_oficial_mandante','placar_oficial_visitante','rodada'], inplace = True)
vencedores.loc[vencedores['vencedor'] > 0, 'vencedor'] = vencedores['clube_casa_id']
vencedores.loc[vencedores['vencedor'] < 0, 'vencedor'] = vencedores['clube_visitante_id']
vencedores.drop(columns = ['clube_casa_id','clube_visitante_id'], inplace = True)
vencedores.rename(columns = {'id':'partida_id'}, inplace = True)

scouts = scouts.merge(vencedores, on = 'partida_id')
scouts.loc[(scouts['vencedor'] != 0) & (scouts['vencedor'] != scouts['clube_id']), 'vencedor'] = -1
scouts.loc[scouts['vencedor'] > 0, 'vencedor'] = 1
print(scouts)