import mlflow
from mlflow import MlflowClient

mlflow.set_tracking_uri('http://127.0.0.1:5000')
c = MlflowClient()
c.set_registered_model_alias('fraude', 'staging', 2)
c.set_registered_model_alias('fraude', 'production', 1)
c.update_model_version('fraude', 1, description='Meilleur F1 parmi les trois configurations comparees')
for a in ['staging', 'production']:
    print(a, '-> version', c.get_model_version_by_alias('fraude', a).version)
