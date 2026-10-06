from pathlib import Path
import yaml
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

p = yaml.safe_load(Path('params.yaml').read_text(encoding='utf-8'))['entrainement']
train = pd.read_csv('data/prepare/train.csv')
modele = RandomForestClassifier(**p).fit(train.drop(columns='fraude'), train['fraude'])
Path('models').mkdir(exist_ok=True)
joblib.dump(modele, 'models/model.pkl')
print('entrainement : modele ecrit dans models/model.pkl')
