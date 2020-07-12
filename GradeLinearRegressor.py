# Prever notas usando Regressão Linear.

# Imports.
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.model_selection import train_test_split

# Opening the csv.
scouts = pd.read_csv("Csv's/2014_scouts.csv")

# Prepairing data.
scouts = scouts.dropna()
scouts.drop(scouts[(scouts.nota == None)].index, inplace = True)
scouts.drop(scouts[(scouts.posicao_id == 6)].index, inplace = True)
scouts.drop(scouts[(scouts.posicao_id != 5)].index, inplace = True)


# Stacking the data for the regression.
x = np.column_stack((scouts.FS,scouts.PE,scouts.A,scouts.FT,scouts.FD,scouts.FF,scouts.G,scouts.I,scouts.PP,scouts.RB,scouts.FC,
	scouts.GC,scouts.CA,scouts.CV,scouts.SG,scouts.DD,scouts.DP,scouts.GS))
y = scouts.nota


# Splitting the data for the regressor
np.random.seed(30284)
x_train, x_test, y_train, y_test = train_test_split(x,y)

# Training model.
model = LinearRegression()
model.fit(x_train, y_train)

# Printing each scout and what its importance
scouts_names = ['FS','PE','A','FT','FD','FF','G','I','PP','RB','FC','GC','CA','CV','SG','DD','DP','GS']
for i in range(0, len(scouts_names)):
	print(scouts_names[i], ": ", round(model.coef_[i],2))

feat_importances = pd.Series(model.coef_, index = scouts_names)
feat_importances.nlargest(20).plot(kind='barh')
plt.title("Feature Importance Linear Regressor")
plt.grid()
plt.tight_layout()	
plt.show()

# The Score
predictions = model.predict(x_test)
print("Score for the Linear Regressor = ", r2_score(y_test, predictions))
print("Mean Squared Error for the Linear Regressor = ", mean_squared_error(y_test, predictions))

