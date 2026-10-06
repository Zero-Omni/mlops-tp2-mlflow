from pathlib import Path
import json
import joblib
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, precision_score, recall_score, ConfusionMatrixDisplay

test = pd.read_csv('data/prepare/test.csv')
modele = joblib.load('models/model.pkl')
y = test['fraude']
pred = modele.predict(test.drop(columns='fraude'))
mets = {k: round(f(y, pred), 4) for k, f in
        [('f1', f1_score), ('precision', precision_score), ('recall', recall_score)]}
Path('reports').mkdir(exist_ok=True)
Path('reports/metrics.json').write_text(json.dumps(mets, indent=2), encoding='utf-8')
ConfusionMatrixDisplay.from_predictions(y, pred)
plt.savefig('reports/confusion.png', dpi=160, bbox_inches='tight')
plt.close()
print('evaluation :', mets)
