import pandas as pd

data = {
    'player': ['De Jong', 'Busquets', 'De Jong', 'Pedri', 'De Jong'],
    'action': ['Pass', 'Pass', 'Carry', 'Pass', 'Ball Recovery'],
    'x': [45, 30, 60, 55, 20],
    'y': [40, 35, 45, 50, 30]
}

df = pd.DataFrame(data)
print(df)
print(df[df['player'] == 'De Jong'])
print(df[df['action'] == 'Pass'])
print(df['player'].value_counts())
passes = df[df['action'] == 'Pass']
print(passes['player'].value_counts())
print(df['x'].mean())
print(df['x'].max())
print(df['x'].min())