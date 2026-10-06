Set-Location $PSScriptRoot
$env:PATH = (Join-Path $PSScriptRoot '.venv/Scripts') + ';' + $env:PATH
$env:PYTHONIOENCODING = 'utf-8'
$env:MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
& .venv/Scripts/mlflow.exe models serve -m 'models:/fraude@production' -p 8000 --env-manager local
