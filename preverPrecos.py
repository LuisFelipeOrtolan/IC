# Prever preços usando Regressão Polinomial.

# Imports.
import pandas as pd 
import numpy as np
import scipy as sp
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline

# Opening the csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Prepairing data.
scouts.drop(scouts[(scouts.variacao_num == None)].index, inplace = True)
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)

# Option to get only one position.
# scouts.drop(scouts[(scouts.posicao_id != 1)].index, inplace = True)

# Stacking the data for the regression.
x = np.column_stack((scouts.FS,scouts.PE,scouts.A,scouts.FT,scouts.FD,scouts.FF,scouts.G,scouts.I,scouts.PP,scouts.RB,scouts.FC,
	scouts.GC,scouts.CA,scouts.CV,scouts.SG,scouts.DD,scouts.DP,scouts.GS))

print(x)

# Using Polynomial Regression, degrees one to four.
for degree in range(1,5):
	modelo = make_pipeline(PolynomialFeatures(degree), LinearRegression())
	modelo.fit(x,scouts.variacao_num)
	print(degree, " = ", modelo.score(x,scouts.variacao_num))