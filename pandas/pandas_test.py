import pandas as pd


df = pd.read_csv("FP2-GIT\pandas\BostonHousing.csv")


primeras_5_filas = df.head()

ejericicio_3 = df[(df['RM']>7) & (df['MEDV']>30)]

print(ejericicio_3)


ejercicio_4 = sum(df['CRIM'])

print(ejercicio_4)

df_chas0 = df[df['CHAS'] == 0]
df_chas1 = df[df['CHAS'] == 1]
CHAS0 = len(df_chas0)
CHAS1 = len(df_chas1)

print(CHAS0, CHAS1)


df['BIG_HOUSE'] = df['RM'] > 6.5





