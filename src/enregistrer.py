import mlflow
from mlflow import MlflowClient

mlflow.set_tracking_uri('http://127.0.0.1:5000')
c = MlflowClient()
exp = mlflow.get_experiment_by_name('tp2-registre')
runs = mlflow.search_runs([exp.experiment_id], order_by=['metrics.f1 DESC'])
existing = {v.run_id for v in c.search_model_versions("name='fraude'")}
for _, r in runs.head(3).iterrows():
    if r['run_id'] in existing:
        print('Deja enregistre :', r['run_id'])
        continue
    mv = mlflow.register_model(r['tags.model_uri'], 'fraude')
    print('version', mv.version, '- F1', round(r['metrics.f1'], 4))
