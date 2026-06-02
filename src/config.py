import os
from dotenv import load_dotenv

# ========================================
# CARGA DE VARIABLES DE ENTORNO
# ========================================

# Leer variables definidas en .env
load_dotenv()

# ========================================
# RUTAS DEL PROYECTO
# ========================================

RUTA_SQLITE = os.getenv(
    "RUTA_SQLITE",
    "data/sqlite/escuela_pipeline.db"
)

RUTA_RAW_DATOS = os.getenv(
    "RUTA_RAW_DATOS",
    "data/raw/datos"
)

RUTA_RAW_LEGAJOS = os.getenv(
    "RUTA_RAW_LEGAJOS",
    "data/raw/legajos"
)

RUTA_RAW_MARZO = os.getenv(
    "RUTA_RAW_MARZO",
    "data/raw/marzo"
)

RUTA_OUTPUTS = os.getenv(
    "RUTA_OUTPUTS",
    "data/outputs"
)

# ========================================
# NOMBRES DE TABLAS
# ========================================

TABLA_ALUMNOS_MASTER = "alumnos_master"

TABLA_CONTACTOS_NORMALIZADOS = "contactos_normalizados"

TABLA_CONTACTOS_VALIDOS = "contactos_validos"

TABLA_CONTACTOS_REVISION = "contactos_revision"

TABLA_REPORTE_CONTACTOS = "reporte_contactos"

# Tablas de fuentes validadas

TABLA_DATOS_VALIDOS = "datos_validos"
TABLA_DATOS_REVISION = "datos_revision"

TABLA_LEGAJOS_VALIDOS = "legajos_validos"
TABLA_LEGAJOS_REVISION = "legajos_revision"

TABLA_MARZO_VALIDOS = "marzo_validos"
TABLA_MARZO_REVISION = "marzo_revision"

# Tablas de identidad

TABLA_IDENTIDAD = "identidad"
TABLA_IDENTIDAD_LIMPIA = "identidad_limpia"
TABLA_IDENTIDAD_PENDIENTE = "identidad_pendiente"