import pandas as pd
import numpy as np

scouts2014 = pd.read_csv("2014_scouts.csv")
scouts2014 = scouts2014.drop(columns=['participou','jogos_num','pontos_num','media_num','preco_num', 'variacao_num','partida_id', 'mando','titular','substituido','tempo_jogado','nota'])

scouts2015 = pd.read_csv("2015_scouts.csv")
scouts2015 = scouts2015.drop(columns=['jogos_num'])
aux = pd.read_csv("2015_atletas.csv")
aux.rename(columns={'id':'atleta_id'}, inplace = True)
scouts2015 = pd.merge(scouts2015, aux, on = 'atleta_id')
scouts2015.rename(columns={'clube_id_x':'clube_id'},inplace = True)
scouts2015 = scouts2015.drop(columns=['pontos_num','media_num','preco_num','variacao_num','apelido','clube_id_y'])
scouts2015 = scouts2015[['atleta_id','rodada','clube_id','posicao_id','FS','PE','A','FT','FD','FF','G','I','PP','RB','FC','GC','CA','CV','SG','DD','DP','GS']]

scouts2016 = pd.read_csv("2016_scouts.csv")
scouts2016 = scouts2016.drop(columns=['participou'])
aux = pd.read_csv("2016_atletas.csv")
aux.rename(columns={'id':'atleta_id'}, inplace = True)
scouts2016 = pd.merge(scouts2016, aux, on = 'atleta_id')
scouts2016.rename(columns={'clube_id_x':'clube_id'},inplace = True)
scouts2016 = scouts2016.drop(columns=['pontos_num','media_num','preco_num','variacao_num','apelido','clube_id_y'])
scouts2016 = scouts2016[['atleta_id','rodada','clube_id','posicao_id','FS','PE','A','FT','FD','FF','G','I','PP','RB','FC','GC','CA','CV','SG','DD','DP','GS']]


scouts2017 = pd.read_csv("2017_scouts.csv")
scouts2017 = scouts2017.drop(columns=['status_id','pontos_num','preco_num','variacao_num','media_num','jogos_num'])
scouts2017.rename(columns={'rodada_id':'rodada'},inplace = True)

scouts = pd.concat([scouts2014,scouts2015,scouts2016,scouts2017])
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.FS == 0) & (scouts.PE == 0) & (scouts.A == 0) & (scouts.FT == 0) & (scouts.FD == 0) & (scouts.FF == 0) 
	& (scouts.G == 0) & (scouts.I == 0) & (scouts.PP == 0) & (scouts.RB == 0) & (scouts.FC == 0) & (scouts.GC == 0)
	& (scouts.CA == 0) & (scouts.CV == 0) & (scouts.SG == 0) & (scouts.DD == 0) & (scouts.DP == 0) & (scouts.GS == 0)].index, inplace = True)
scouts.sort_values(by=['clube_id','posicao_id','atleta_id','rodada'], inplace = True)

scouts=(scouts-scouts.min())/(scouts.max()-scouts.min())

print(scouts)