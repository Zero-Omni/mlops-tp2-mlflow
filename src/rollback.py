import mlflow
import pandas as pd
from mlflow import MlflowClient

mlflow.set_tracking_uri('http://127.0.0.1:5000')
c = MlflowClient()
X = pd.DataFrame([dict(montant=8500.0, anciennete=3, freq_24h=9, nuit=1)])
def servi():
    v = c.get_model_version_by_alias('fraude', 'production').version
    m = mlflow.pyfunc.load_model('models:/fraude@production')
    print('alias production -> version', v, '| run', str(m.metadata.run_id)[:8],
          '| prediction', m.predict(X))
for version, message in [(1, 'etat initial'), (2, 'promotion v2'), (1, 'retour arriere v1')]:
    c.set_registered_model_alias('fraude', 'production', version)
    print('---', message)
    servi()
