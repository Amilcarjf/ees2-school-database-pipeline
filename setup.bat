@echo off
echo.
echo ================================================
echo   EES N2 - School Database Pipeline
echo   Setup de estructura de carpetas + Git
echo ================================================
echo.

set ROOT=C:\ees2-school-database-pipeline

echo [1/4] Creando estructura de carpetas...

mkdir "%ROOT%"
mkdir "%ROOT%\data\raw\datos"
mkdir "%ROOT%\data\raw\legajos"
mkdir "%ROOT%\data\raw\marzo"
mkdir "%ROOT%\data\sqlite"
mkdir "%ROOT%\data\outputs\reportes"
mkdir "%ROOT%\data\outputs\exports"
mkdir "%ROOT%\docs\contratos\vigentes"
mkdir "%ROOT%\docs\contratos\historicos"
mkdir "%ROOT%\docs\pipeline\vigentes"
mkdir "%ROOT%\docs\pipeline\historicos"
mkdir "%ROOT%\docs\auditorias"
mkdir "%ROOT%\docs\arquitectura"
mkdir "%ROOT%\docs\decisiones"
mkdir "%ROOT%\notebooks\laboratorio"
mkdir "%ROOT%\notebooks\operativo"
mkdir "%ROOT%\src"
mkdir "%ROOT%\tests"

echo     OK - Carpetas creadas.
echo.

echo [2/4] Creando archivos base...

echo # .env.example - EES N2 School Database Pipeline > "%ROOT%\.env.example"
echo # Copia este archivo como .env y completa tus rutas >> "%ROOT%\.env.example"
echo # El archivo .env real NO se sube a GitHub >> "%ROOT%\.env.example"
echo. >> "%ROOT%\.env.example"
echo RUTA_SQLITE=C:/ees2-school-database-pipeline/data/sqlite/escuela_pipeline.db >> "%ROOT%\.env.example"
echo RUTA_RAW_DATOS=C:/ees2-school-database-pipeline/data/raw/datos >> "%ROOT%\.env.example"
echo RUTA_RAW_LEGAJOS=C:/ees2-school-database-pipeline/data/raw/legajos >> "%ROOT%\.env.example"
echo RUTA_RAW_MARZO=C:/ees2-school-database-pipeline/data/raw/marzo >> "%ROOT%\.env.example"
echo RUTA_OUTPUTS=C:/ees2-school-database-pipeline/data/outputs >> "%ROOT%\.env.example"

echo # .gitignore - EES N2 School Database Pipeline > "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Variables de entorno >> "%ROOT%\.gitignore"
echo .env >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Base de datos SQLite >> "%ROOT%\.gitignore"
echo *.db >> "%ROOT%\.gitignore"
echo data/sqlite/ >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Archivos fuente Word - datos sensibles de alumnos >> "%ROOT%\.gitignore"
echo data/raw/ >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Outputs generados >> "%ROOT%\.gitignore"
echo data/outputs/ >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Python >> "%ROOT%\.gitignore"
echo __pycache__/ >> "%ROOT%\.gitignore"
echo *.pyc >> "%ROOT%\.gitignore"
echo *.pyo >> "%ROOT%\.gitignore"
echo *.egg-info/ >> "%ROOT%\.gitignore"
echo dist/ >> "%ROOT%\.gitignore"
echo build/ >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Entornos virtuales >> "%ROOT%\.gitignore"
echo venv/ >> "%ROOT%\.gitignore"
echo .venv/ >> "%ROOT%\.gitignore"
echo env/ >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Jupyter >> "%ROOT%\.gitignore"
echo .ipynb_checkpoints/ >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # IDEs >> "%ROOT%\.gitignore"
echo .vscode/ >> "%ROOT%\.gitignore"
echo .idea/ >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Windows >> "%ROOT%\.gitignore"
echo Thumbs.db >> "%ROOT%\.gitignore"
echo Desktop.ini >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Logs >> "%ROOT%\.gitignore"
echo *.log >> "%ROOT%\.gitignore"
echo. >> "%ROOT%\.gitignore"
echo # Temporales >> "%ROOT%\.gitignore"
echo *.tmp >> "%ROOT%\.gitignore"
echo *.bak >> "%ROOT%\.gitignore"

echo # requirements.txt - EES N2 School Database Pipeline > "%ROOT%\requirements.txt"
echo python-docx >> "%ROOT%\requirements.txt"
echo pandas >> "%ROOT%\requirements.txt"
echo python-dotenv >> "%ROOT%\requirements.txt"
echo openpyxl >> "%ROOT%\requirements.txt"

type nul > "%ROOT%\src\__init__.py"
type nul > "%ROOT%\tests\__init__.py"
type nul > "%ROOT%\README.md"

echo     OK - Archivos base creados.
echo.

echo [3/4] Inicializando repositorio Git...
cd /d "%ROOT%"
git init
git add .
git commit -m "init: estructura base del proyecto y archivos de configuracion"
echo     OK - Repositorio inicializado con primer commit.
echo.

echo [4/4] Listo.
echo.
echo ================================================
echo   Estructura creada en: %ROOT%
echo.
echo   Proximo paso - conectar con GitHub:
echo   git remote add origin https://github.com/TU_USUARIO/ees2-school-database-pipeline.git
echo   git branch -M main
echo   git push -u origin main
echo ================================================
echo.
pause
