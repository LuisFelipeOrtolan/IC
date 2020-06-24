import pandas as pd

df = pd.read_csv("Csv's/2014_scouts.csv")

df.drop(df[(df.posicao_id != 1)].index, inplace = True)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
	print(df[df['SG'].isin(["1"])])
