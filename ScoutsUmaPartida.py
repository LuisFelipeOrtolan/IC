import pandas as pd 
import numpy as np
import scipy as sp
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# Read the csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Removing the managers
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)

# Removing information that is no longer needed.
scouts.drop(columns = ['clube_id','participou','jogos_num','pontos_num','media_num','mando','titular',
	'substituido','tempo_jogado','nota','posicao_id','rodada', 'preco_num'], inplace  = True)

# Preparing the data.
scouts = scouts.dropna()

# Getting the information for the Random Forest Regressor
x = np.column_stack((scouts.FS, scouts.PE, scouts.FF, scouts.PP, scouts.RB, scouts.FC, scouts.CA, scouts.CV,
	scouts.DD, scouts.DP, scouts.GS, scouts.GC,scouts.FT, scouts.I, scouts.FD, scouts.A,scouts.G, scouts.SG))
y = scouts.variacao_num

# The Random Forest Regressor
modelo = RandomForestRegressor(n_estimators = 18, random_state = 42)
modelo.fit(x,y)

# Selecting the data from only one match.
partida = 180094
scouts.drop(scouts[scouts.partida_id != partida].index, inplace = True)

# Predicting the values for a match.
y = np.column_stack((scouts.FS, scouts.PE, scouts.FF, scouts.PP, scouts.RB, scouts.FC, scouts.CA, scouts.CV,
	scouts.DD, scouts.DP, scouts.GS, scouts.GC,scouts.FT, scouts.I, scouts.FD, scouts.A,scouts.G, scouts.SG))
predicoes = modelo.predict(y)

# The Score.
print("Score = ", modelo.score(y,scouts.variacao_num))
data = {'Valor real':scouts.variacao_num,'Predicoes':predicoes,'Atleta_id':scouts.atleta_id}
df = pd.DataFrame(data)
df.sort_values(by=['Predicoes'], ascending = False, inplace = True)
print(df)