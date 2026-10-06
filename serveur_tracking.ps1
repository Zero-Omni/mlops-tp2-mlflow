Set-Location $PSScriptRoot
$env:PYTHONIOENCODING = 'utf-8'
& .venv/Scripts/mlflow.exe server --host 127.0.0.1 --port 5000 --workers 1 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts
