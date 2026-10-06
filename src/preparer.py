from pathlib import Path
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split

p = yaml.safe_load(Path('params.yaml').read_text(encoding='utf-8'))['preparation']
df = pd.read_csv('data/transactions.csv')
train, test = train_test_split(df, **p)
Path('data/prepare').mkdir(parents=True, exist_ok=True)
train.to_csv('data/prepare/train.csv', index=False)
test.to_csv('data/prepare/test.csv', index=False)
print('preparation :', len(train), 'lignes train /', len(test), 'lignes test')
