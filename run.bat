@echo off
REM ============================================================================
REM  Batch script to start both the Frontend and Backend servers simultaneously.
REM  This version assumes Python packages are installed globally (no venv).
REM  Run this file from the root directory of your project (e.g., SGP-II).
REM ============================================================================

ECHO Starting servers...
ECHO.

REM --- Start Backend Server ---
REM This command opens a new window, navigates to the backend folder,
REM and then starts the Flask app using the system's Python.
ECHO Launching Python backend server in a new window...
start "Backend Server" cmd /k "cd backend && echo Starting Flask server (app.py)... && python app.py"

REM --- Start Frontend Server ---
REM This command opens another new window, navigates to the frontend folder,
REM and starts the Vite development server.
ECHO Launching Node.js frontend server in a new window...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

ECHO.
ECHO Both server windows have been launched.
ECHO Please keep both terminal windows open while you are working.

