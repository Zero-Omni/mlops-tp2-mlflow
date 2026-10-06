from pathlib import Path
import sys
import json
import hashlib
import subprocess
import yaml
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, ConfusionMatrixDisplay

n_estimators, max_depth = map(int, sys.argv[1:3])
P = yaml.safe_load(Path('params.yaml').read_text(encoding='utf-8'))
mlflow.set_tracking_uri('http://127.0.0.1:5000')
mlflow.set_experiment('tp2-registre')
Path('reports').mkdir(exist_ok=True)
df = pd.read_csv('data/transactions.csv')
X, y = df.drop(columns='fraude'), df['fraude']
Xtr, Xte, ytr, yte = train_test_split(X, y, **P['preparation'])
with mlflow.start_run(run_name=f'rf-{n_estimators}-{max_depth}') as run:
    m = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
        random_state=P['entrainement']['random_state']).fit(Xtr, ytr)
    pred, proba = m.predict(Xte), m.predict_proba(Xte)[:, 1]
    metrics = dict(f1=f1_score(yte, pred), precision=precision_score(yte, pred),
                   recall=recall_score(yte, pred), roc_auc=roc_auc_score(yte, proba))
    mlflow.log_params(dict(n_estimators=n_estimators, max_depth=max_depth, **P['preparation']))
    mlflow.log_metrics(metrics)
    commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], text=True).strip()
    mlflow.set_tags(dict(auteur='ELATTAR Abderrahman et EL MRHARI Marouane',
        commit=commit, jeu_de_donnees='transactions v1',
        donnees_sha256=hashlib.sha256(Path('data/transactions.csv').read_bytes()).hexdigest()))
    ConfusionMatrixDisplay.from_predictions(yte, pred)
    plt.savefig('reports/confusion.png', dpi=160, bbox_inches='tight')
    plt.close()
    mlflow.log_artifact('reports/confusion.png')
    imp = {c: round(float(v), 4) for c, v in zip(X.columns, m.feature_importances_)}
    Path('reports/importances.json').write_text(json.dumps(imp, indent=2))
    mlflow.log_artifact('reports/importances.json')
    info = mlflow.sklearn.log_model(m, name='model', input_example=Xte.head(3),
                                  skops_trusted_types=['sklearn.tree._tree.Tree'])
    mlflow.set_tag('model_uri', info.model_uri)
    print('RUN', run.info.run_id, 'F1 =', round(metrics['f1'], 4))
