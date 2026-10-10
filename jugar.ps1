# Inicia el servidor local de Arena (sin caché)
Write-Host "Abre http://localhost:8000 en tu navegador"
Start-Process "http://localhost:8000"
python "$PSScriptRoot\serve.py"
