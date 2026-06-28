@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ports = Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue; foreach ($port in $ports) { Stop-Process -Id $port.OwningProcess -Force -ErrorAction SilentlyContinue }"
.\.venv\Scripts\python.exe scripts\clean_runtime_cache.py
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '.\.venv\Scripts\python.exe' -ArgumentList @('-m', 'streamlit', 'run', 'app.py', '--server.port', '8501') -WorkingDirectory (Get-Location).Path -WindowStyle Hidden"
echo Streamlit started in background: http://localhost:8501
