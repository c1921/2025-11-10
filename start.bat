@echo off
echo Starting Backend Server...
cd backend
start cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak

echo Starting Frontend Server...
cd ..\frontend
start cmd /k "npm run dev"

echo.
echo ========================================
echo Game servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo ========================================
