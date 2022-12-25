import pandas as pd

df = pd.read_json('./data.json')

df = df.groupby(by=['category']).mean()

print(df)