Set-Location $PSScriptRoot
$corps = @{ dataframe_records = @(
    @{ montant = 8500.0; anciennete = 3; freq_24h = 9; nuit = 1 }
) } | ConvertTo-Json -Depth 5
Write-Output 'REQUETE VALIDE'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/invocations -ContentType 'application/json' -Body $corps | ConvertTo-Json
$mauvais = @{ dataframe_records = @(@{ montant = 8500.0 }) } | ConvertTo-Json -Depth 5
Write-Output 'REQUETE INVALIDE'
try {
    Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/invocations -ContentType 'application/json' -Body $mauvais
} catch {
    Write-Output ('HTTP ' + [int]$_.Exception.Response.StatusCode)
    Write-Output $_.ErrorDetails.Message
}
