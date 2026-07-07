# leesure! - Startup Script
# Launches the FastAPI backend and Vite frontend simultaneously

Write-Host "=================================" -ForegroundColor Magenta
Write-Host "   leesure! - AI Entertainment" -ForegroundColor Magenta
Write-Host "=================================" -ForegroundColor Magenta
Write-Host ""

# Start backend
Write-Host "[1/2] Starting Tyler's Backend (FastAPI)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8000" -WindowStyle Normal

Start-Sleep -Seconds 2

# Start frontend
Write-Host "[2/2] Starting leesure! Frontend (Vite)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev" -WindowStyle Normal

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host " leesure! is now running!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host " Frontend:  http://localhost:5173" -ForegroundColor Yellow
Write-Host " Backend:   http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host " API Docs:  http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host " Demo login: demo / tyler" -ForegroundColor Cyan
Write-Host ""
