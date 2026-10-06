from pathlib import Path
import sys
import json
import subprocess
import yaml
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn

P = yaml.safe_load(Path('params.yaml').read_text(encoding='utf-8'))
mlflow.set_tracking_uri('http://127.0.0.1:5000')
mlflow.set_experiment('tp2-pipeline')

def lancer(etape):
    subprocess.run([sys.executable, f'src/{etape}.py'], check=True)

refuse = False
with mlflow.start_run(run_name='pipeline'):
    for etape, cle in [('preparer', 'preparation'), ('entrainer', 'entrainement'), ('evaluer', None)]:
        with mlflow.start_run(run_name=etape, nested=True):
            lancer(etape)
            if cle:
                mlflow.log_params(P[cle])
            else:
                mets = json.loads(Path('reports/metrics.json').read_text())
                mlflow.log_metrics(mets)
                mlflow.log_artifact('reports/confusion.png')
    seuil = P['validation']['seuil_f1']
    mlflow.log_param('seuil_f1', seuil)
    mlflow.log_metrics(mets)
    mlflow.log_dict(P, 'params.yaml')
    if mets['f1'] >= seuil:
        exemple = pd.read_csv('data/prepare/test.csv').drop(columns='fraude').head(3)
        mlflow.sklearn.log_model(joblib.load('models/model.pkl'), name='model',
            input_example=exemple, registered_model_name='fraude-tp2',
            skops_trusted_types=['sklearn.tree._tree.Tree'])
        mlflow.set_tag('statut', 'accepte')
        print(f"modele accepte (F1 {mets['f1']} >= {seuil}) et enregistre")
    else:
        mlflow.set_tag('statut', 'refuse')
        refuse = True
if refuse:
    raise SystemExit(f"modele refuse : F1 {mets['f1']} < seuil {seuil}")
