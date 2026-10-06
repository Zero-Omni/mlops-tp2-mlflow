# TP2 MLflow — détection de fraude bancaire

ELATTAR Abderrahman et EL MRHARI Marouane — 5IASD G7.

## Installation sous PowerShell

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python donnees.py
```

Dans un premier terminal, lancer `./serveur_tracking.ps1` et ouvrir http://127.0.0.1:5000.
Dans un deuxième terminal activé :

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python pipeline.py
```

Modifier `max_depth` de 12 à 2 dans params.yaml, relancer le pipeline et vérifier
`$LASTEXITCODE` (1). Restaurer 12 et relancer. Le tag `statut=refuse` indique
un refus métier, même si le run MLflow est marqué Finished : la sortie non nulle
est émise après la fermeture du run, conformément au sujet.

```powershell
python src/train_complet.py 200 8
python src/train_complet.py 300 12
python src/train_complet.py 500 16
python src/enregistrer.py
python src/alias.py
python src/rollback.py
```

Le script d'enregistrement utilise les URI `models:/m-...` des Logged Models de
MLflow 3 et ne réenregistre pas les runs déjà présents. Sur un registre neuf,
les versions 1, 2 et 3 sont attribuées par F1 décroissant.

Dans un troisième terminal, lancer `./serveur_inference.ps1`, puis exécuter
`./test_http.ps1` dans le deuxième. La requête valide renvoie 1 et la requête
incomplète est rejetée avec HTTP 400. Le montant doit être un flottant, 8500.0,
pour respecter la signature double.

Le serveur d'inférence charge l'alias au démarrage. Une modification d'alias
ne recharge pas automatiquement un serveur déjà lancé. Le test rollback.py
recharge le modèle à chaque étape ; redémarrer le serveur HTTP pour lui faire
prendre en compte une autre version.

## Résultats réellement obtenus

5000 transactions, 568 fraudes ; 3750 lignes train et 1250 lignes test.

| Arbres | Profondeur | F1 | Précision | Rappel | ROC AUC |
| --- | --- | --- | --- | --- | --- |
| 200 | 8 | 0.8549 | 0.9008 | 0.8134 | 0.9885 |
| 300 | 12 | 0.8636 | 0.8769 | 0.8507 | 0.9884 |
| 500 | 16 | 0.8669 | 0.8837 | 0.8507 | 0.9872 |

Le modèle dégradé (profondeur 2) obtient F1=0.2013, inférieur au seuil 0.82.
Production pointe vers la version 1 ; staging vers la version 2.

Les dossiers data, models, reports, .venv et les stockages MLflow sont ignorés
par Git et sont recréés par les scripts. requirements-lock.txt contient les
versions exactes de l'environnement utilisé pour ce compte rendu.
