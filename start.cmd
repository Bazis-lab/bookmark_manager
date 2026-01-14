@echo off
setlocal enabledelayedexpansion
cd /d %~dp0

echo.
echo =====================================
echo bookmark manager launcher
echo =====================================
echo.
echo urls:
echo   http://127.0.0.1:5000/
echo   http://127.0.0.1:5000/categories/
echo   http://127.0.0.1:5000/tags/
echo   http://127.0.0.1:5000/export/json
echo   http://127.0.0.1:5000/export/csv
echo.

echo choose:
echo   1 - run (fast, keep venv)
echo   2 - run (rebuild venv)
echo   3 - rebuild venv only
echo   4 - reset database (empty or with examples)
echo   5 - exit
echo.

set choice=
set /p choice=enter 1/2/3/4/5 and press enter: 

if "%choice%"=="" (
  echo empty choice
  pause
  goto :end
)

if "%choice%"=="5" (
  echo bye
  pause
  goto :end
)

python --version >nul 2>&1
if errorlevel 1 (
  echo python not found in PATH
  pause
  goto :end
)

echo.
echo cleaning caches...
if exist "__pycache__" rmdir /s /q "__pycache__"
for /d /r %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
for /r %%f in (*.pyc) do @del /q "%%f" >nul 2>&1
for /r %%f in (*.pyo) do @del /q "%%f" >nul 2>&1
if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
if exist ".mypy_cache" rmdir /s /q ".mypy_cache"
if exist ".ruff_cache" rmdir /s /q ".ruff_cache"
if exist "htmlcov" rmdir /s /q "htmlcov"
if exist ".coverage" del /q ".coverage" >nul 2>&1

if "%choice%"=="1" goto :fast
if "%choice%"=="2" goto :rebuild
if "%choice%"=="3" goto :rebuild
if "%choice%"=="4" goto :dbreset

echo invalid choice: %choice%
pause
goto :end

:fast
echo.
if not exist ".venv\Scripts\activate.bat" (
  echo venv not ready, switching to rebuild
  goto :rebuild
)

echo activating venv...
call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo failed to activate venv
  pause
  goto :end
)

echo checking dependencies...
python -c "import flask, flask_sqlalchemy" >nul 2>&1
if errorlevel 1 (
  echo dependencies missing, installing...
  pip install -r requirements.txt
  if errorlevel 1 (
    echo pip install failed
    pause
    goto :end
  )
)

echo.
echo starting server...
echo open: http://127.0.0.1:5000/
echo stop: ctrl+c
echo.

python run.py
echo.
echo server stopped (or crashed)
pause
goto :end

:rebuild
echo.
echo recreating venv...
if exist ".venv" rmdir /s /q ".venv"

python -m venv .venv
if errorlevel 1 (
  echo failed to create venv
  pause
  goto :end
)

echo activating venv...
call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo failed to activate venv
  pause
  goto :end
)

echo installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
  echo pip install failed
  pause
  goto :end
)

if "%choice%"=="3" (
  echo venv ready, project not started
  pause
  goto :end
)

echo.
echo starting server...
echo open: http://127.0.0.1:5000/
echo stop: ctrl+c
echo.

python run.py
echo.
echo server stopped (or crashed)
pause
goto :end

:dbreset
echo.
if not exist ".venv\Scripts\activate.bat" (
  echo venv not found. please run option 2 first.
  pause
  goto :end
)

echo activating venv...
call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo failed to activate venv
  pause
  goto :end
)

echo.
echo reset database:
echo   1 - empty database
echo   2 - database with examples
echo   3 - back
echo.

set dbchoice=
set /p dbchoice=enter 1/2/3 and press enter: 

if "%dbchoice%"=="3" goto :end
if "%dbchoice%"=="1" goto :dbempty
if "%dbchoice%"=="2" goto :dbseed

echo invalid choice
pause
goto :end

:dbempty
echo.
echo creating empty database...
python manage_db.py empty
echo.
pause
goto :end

:dbseed
echo.
echo creating database with examples...
python manage_db.py seed
echo.
pause
goto :end

:end
endlocal