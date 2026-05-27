# GUÍA ESTRUCTURADA — EES N°2 School Database Pipeline

> Documentación técnica completa del proyecto.  
> Audiencia: el propio desarrollador, revisores técnicos, y cualquier persona que clone el repositorio.

---

## Índice

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Estado actual](#2-estado-actual)
3. [Arquitectura del pipeline](#3-arquitectura-del-pipeline)
4. [Estructura de módulos](#4-estructura-de-módulos)
5. [Estructura de carpetas](#5-estructura-de-carpetas)
6. [Decisiones clave de diseño](#6-decisiones-clave-de-diseño)
7. [Convenciones del proyecto](#7-convenciones-del-proyecto)
8. [Cómo ejecutar el pipeline](#8-cómo-ejecutar-el-pipeline)
9. [Cómo extender el proyecto](#9-cómo-extender-el-proyecto)
10. [Documentación de referencia](#10-documentación-de-referencia)

---

## 1. Descripción del proyecto

### Qué es

Pipeline de datos que construye una base de datos relacional escalable para una escuela secundaria (EES N°2), a partir de archivos Word semi-estructurados que contienen información de alumnos, legajos y registros de inicio de ciclo lectivo.

### Problema que resuelve

La información escolar existe en archivos Word dispersos, sin estructura estandarizada, con metadatos incrustados en campos de texto, con fuentes inconsistentes entre sí, y sin ningún identificador único de persona. Este proyecto la convierte en una base de datos relacional consultable, con trazabilidad completa desde el archivo fuente hasta el registro final.

### Stack tecnológico

| Herramienta | Rol |
|---|---|
| Python | Lenguaje principal del pipeline |
| pandas | Manipulación y transformación de DataFrames |
| python-docx | Extracción de tablas desde archivos Word |
| SQLite | Storage intermedio y persistencia local |
| python-dotenv | Gestión de rutas y variables de entorno |
| Git / GitHub | Control de versiones y portfolio |

### Alcance actual

El pipeline cubre la entidad **Alumnos** con sus **Contactos** (teléfonos). Está diseñado para escalar a docentes, preceptores, materias, cursos, horarios y otras entidades escolares.

---

## 2. Estado actual

| Fase | Estado |
|---|---|
| Inventario de archivos | ✅ Completo |
| Notebook exploratorio piloto (1°1° 2025) | ✅ Completo |
| Contratos de fuentes (Datos, Legajos, Marzo) | ✅ Aprobados |
| Contrato de entidad Contactos | ✅ Aprobado |
| Contrato de arquitectura modular | ✅ Aprobado |
| Contrato de arquitectura de carpetas | ✅ Aprobado |
| pipeline_v1 — Etapas 1 a 5 | ✅ Completo para 1°1° 2025 |
| Implementación modular (src/) | 🔄 En diseño |
| Escalamiento a todos los cursos | ⏳ Pendiente |
| Exportación SQL final | ⏳ Pendiente |
| Modelo relacional completo | ⏳ Pendiente |

---

## 3. Arquitectura del pipeline

El pipeline tiene **10 etapas canónicas**. La numeración es fija y no varía entre fuentes ni versiones.

```
Etapa 0 — Inventario
Etapa 1 — Extracción RAW por fuente
Etapa 2 — Normalización técnica (STAGING)
Etapa 3 — Validación por fuente
Etapa 4 — Reconciliación de identidad
Etapa 5 — Master de alumnos + Contactos
Etapa 6 — Eventos / Movimientos (Marzo)
Etapa 7 — Otras entidades
Etapa 8 — Persistencia / Exportación
Etapa 9 — Modelo relacional
```

### Fuentes de datos

El pipeline maneja tres fuentes por curso/división:

| Fuente | Rol | Tipo |
|---|---|---|
| **Datos** | Fuente primaria de identidad y atributos | Registro administrativo completo |
| **Legajos** | Fuente de contraste para reconciliación | Identificadores institucionales |
| **Marzo** | Fuente de eventos de inicio de ciclo | Log de movimientos, no de identidad |

### Flujo de datos por etapa

```
[Archivos Word]
      │
      ▼
  Etapa 1: Extracción RAW
  df_datos_raw / df_legajos_raw / df_marzo_raw
      │
      ▼
  Etapa 2: Normalización STG
  df_datos_stg / df_legajos_stg / df_marzo_stg
      │
      ▼
  Etapa 3: Validación
  df_[fuente]_validos / df_[fuente]_revision / reporte_[fuente]
      │
      ▼
  Etapa 4: Reconciliación de identidad
  df_identidad / df_identidad_limpia / df_identidad_pendiente
      │
      ▼
  Etapa 5: Master + Contactos
  df_alumnos_master / df_contactos_validos / df_contactos_revision
      │
      ▼
  Etapa 6: Eventos (Marzo)
  df_movimientos
      │
      ▼
  Etapa 8: SQLite → SQL
      │
      ▼
  Etapa 9: Modelo relacional
```

---

## 4. Estructura de módulos

El código del pipeline está organizado en módulos con **responsabilidad única**. Cada módulo responde una sola pregunta.

```
src/
├── pipeline_alumnos.py   — Orquestador: ejecuta Etapas 1–5 para un curso/año
├── config.py             — Constantes, rutas y parámetros globales
├── utils_texto.py        — Herramientas genéricas de limpieza textual
├── extractores.py        — Extracción RAW desde archivos Word
├── normalizacion.py      — Transformación RAW → STG
├── validacion.py         — Evaluación de calidad y separación válidos/revisión
├── reconciliacion.py     — Resolución de identidad entre fuentes
├── master.py             — Construcción de entidades finales consolidadas
├── contactos.py          — Extracción y normalización de contactos telefónicos
└── persistencia.py       — Escritura y lectura desde SQLite
```

### Responsabilidades por módulo

| Módulo | Pregunta que responde |
|---|---|
| `pipeline_alumnos.py` | ¿Cómo ejecuto el pipeline completo para un curso? |
| `config.py` | ¿Dónde están definidas las rutas y nombres de tabla? |
| `utils_texto.py` | ¿Cómo evito repetir la misma limpieza de strings en todos lados? |
| `extractores.py` | ¿Qué contiene el archivo original, sin ninguna transformación? |
| `normalizacion.py` | ¿Cómo dejo el dato estructuralmente consistente sin decidir si es correcto? |
| `validacion.py` | ¿Este registro puede avanzar en el pipeline o necesita revisión manual? |
| `reconciliacion.py` | ¿Este alumno de Datos y este alumno de Legajos son la misma persona? |
| `master.py` | ¿Cómo queda representada finalmente la entidad? |
| `contactos.py` | ¿Qué teléfonos están asociados a cada persona? |
| `persistencia.py` | ¿Cómo persisto los resultados sin mezclar lógica de negocio? |

### Flujo entre módulos

```
extractores → normalizacion → validacion → reconciliacion → master
                                                          ↘ contactos
persistencia  (disponible desde cualquier etapa)
utils_texto   (disponible desde cualquier módulo)
config        (disponible desde cualquier módulo)
```

### Reglas de módulos

- Cada módulo tiene **una sola razón para cambiar**.
- Los helpers con reglas de negocio de una fuente específica viven en `normalizacion.py`, no en `utils_texto.py`.
- `utils_texto.py` contiene herramientas genéricas, no reglas de dominio.
- `persistencia.py` puede usarse antes de la Etapa 8 del pipeline maestro — es un módulo técnico, no una etapa.
- Cada etapa persiste en **un único punto al final**, no en el medio del procesamiento.

---

## 5. Estructura de carpetas

```
ees2-school-database-pipeline/
│
├── data/
│   ├── raw/                    ← Archivos fuente originales (en .gitignore)
│   │   ├── datos/
│   │   ├── legajos/
│   │   └── marzo/
│   ├── sqlite/                 ← Base de datos SQLite (en .gitignore)
│   └── outputs/                ← Resultados procesados (en .gitignore)
│       ├── reportes/
│       └── exports/
│
├── docs/
│   ├── contratos/              ← Contratos de fuentes y entidades
│   │   ├── vigentes/
│   │   └── historicos/
│   ├── pipeline/               ← Pipeline maestro
│   │   ├── vigentes/
│   │   └── historicos/
│   ├── auditorias/             ← Registros de auditorías técnicas
│   ├── arquitectura/           ← Contratos de arquitectura modular y carpetas
│   └── decisiones/             ← Registro de decisiones de diseño relevantes
│
├── notebooks/
│   ├── laboratorio/            ← Exploración y análisis ad hoc
│   └── operativo/              ← Notebooks del pipeline formal
│
├── src/                        ← Módulos Python del pipeline
├── tests/                      ← Validaciones automáticas
│
├── GUIA_ESTRUCTURADA.md        ← Este documento
├── README.md                   ← Descripción pública del proyecto
├── requirements.txt
├── .env.example
└── .gitignore
```

### Qué no está en el repositorio

Por diseño y por seguridad, no se suben a GitHub:

- `data/raw/` — archivos fuente con datos personales de alumnos
- `data/sqlite/` — base de datos generada por el pipeline
- `data/outputs/` — resultados generados, se regeneran con el pipeline
- `.env` — rutas y variables locales del entorno

---

## 6. Decisiones clave de diseño

### Raw vs Normalizado

Todo campo extraído del Word se preserva con sufijo `_raw` antes de cualquier transformación. El dato original nunca se destruye.

```
nombre_original  →  nombre_completo
telefono_raw     →  telefono_num + tipo_contacto
libro_matriz_raw →  libro_matriz
```

**Por qué:** trazabilidad y control de errores. Si algo sale mal en la normalización, se puede volver al dato original y determinar si el problema venía del Word o lo generó la transformación.

### id_persona — surrogate key

Cada alumno recibe un `id_persona` generado internamente en la Etapa 4, después de la reconciliación. Todos los sistemas del pipeline referencian `id_persona`, no el legajo ni el DNI directamente.

**Por qué:** el legajo puede repetirse entre años o cursos. El DNI puede estar ausente o tener errores. Un identificador propio, estable y garantizado elimina esa fragilidad.

**Regla crítica:** si falla la generación de `id_persona`, el pipeline se frena. No se corrige automáticamente, no se reemplaza con un índice local, no se reinicia desde 1.

### Marzo como fuente de eventos

Marzo nunca se mezcla directamente con la identidad de alumnos. Es una fuente de **eventos** (presencias, altas tardías, traslados), no de **identidad**. Nunca modifica `df_alumnos_master`.

**Por qué:** Marzo es estructuralmente un log de estado en un momento del tiempo. Un alumno puede aparecer en Marzo de formas distintas según el momento del año, con anotaciones contextuales mezcladas en el nombre. Usarla como fuente de identidad hubiera sido un error de modelado.

### Contactos como entidad separada

Los teléfonos se modelan en una tabla `Contactos` independiente con relación `Alumno 1→N Contactos`. No forman parte de `df_alumnos_master`.

**Por qué:** un alumno puede tener múltiples teléfonos. Incluirlos como columnas del master viola la Primera Forma Normal y no escala.

### Reconciliación jerárquica de identidad

La resolución de quién es quién entre fuentes sigue una jerarquía de cinco niveles:

| Nivel | Condición | Acción |
|---|---|---|
| 1 | DNI coincide | Match definitivo |
| 2 | Nombre + legajo coinciden | Match probable |
| 3 | Nombre + LM + folio coinciden | Match posible |
| 4 | Solo nombre coincide | Match débil → `requiere_revision = True` |
| 5 | Sin match | Nueva entidad → `df_identidad_pendiente` |

Un match de Nivel 4 no entra automáticamente al master. Va a `df_identidad_pendiente` para resolución manual.

**Por qué:** los homónimos son un caso real en una institución escolar. Un merge por nombre sin jerarquía de evidencia puede fusionar silenciosamente a dos personas distintas, lo cual es peor que un no-match.

### SQLite como storage intermedio

SQLite no es solo el destino final — es el storage del pipeline desde Etapa 1. Cada etapa escribe su output a una tabla en SQLite.

**Por qué:** hace el pipeline reiniciable. Si falla en Etapa 4 después de procesar 30 cursos, no se pierde el trabajo de las etapas anteriores. También permite inspeccionar el estado del pipeline en cualquier punto con SQL.

### Separación de etapas de validación

`validacion.py` es el primer módulo que toma decisiones. Antes de él, los módulos solo transforman. Después de él, los registros tienen un destino explícito: válidos, revisión, o descarte.

Niveles de problema:
- **Leve:** avanza con flag de calidad
- **Medio:** va a `df_[fuente]_revision` con `nivel_problema = 'medio'`
- **Grave:** va a `df_[fuente]_revision` con `nivel_problema = 'grave'`

---

## 7. Convenciones del proyecto

### Nombres de DataFrames

```
df_[fuente]_raw      — dato crudo extraído del Word
df_[fuente]_stg      — dato normalizado técnicamente
df_[fuente]_validos  — registros que pasan validación
df_[fuente]_revision — registros que requieren revisión manual
reporte_[fuente]     — métricas de calidad
df_identidad         — identidad cruzada entre fuentes
df_identidad_limpia  — identidad consolidada con id_persona
df_identidad_pendiente — casos sin resolución automática
df_alumnos_master    — una fila por alumno
df_contactos_validos — una fila por teléfono validado
```

### Nombres de archivos de output

```
[tipo]_[fuente_o_entidad]_[curso]_[division]_[anio].[ext]

Ejemplos:
reporte_datos_1ro_1ra_2025.csv
alumnos_master_1ro_1ra_2025.csv
contactos_validos_1ro_1ra_2025.csv
```

### Normalización de texto

Regla estándar aplicada en las tres fuentes:

```python
import re, unicodedata

def limpiar_texto(valor):
    valor = str(valor).strip()
    valor = re.sub(r"\s+", " ", valor)
    valor = unicodedata.normalize("NFC", valor)
    return valor
```

### Nuevas carpetas de fuentes

```
data/raw/[nombre_fuente]/   ← se crea cuando aparece la fuente real
```

No se crean carpetas por anticipación.

### Commits de Git

```
init:      estructura base y configuración inicial
feat:      nueva funcionalidad o módulo implementado
fix:       corrección de un error
refactor:  reorganización de código sin cambio de comportamiento
docs:      cambios en documentación
test:      agregado o modificación de tests
```

Ejemplos:
```
feat: implementar extractores.py — Etapa 1
feat: implementar normalizacion.py — Etapa 2
fix: corregir re.sub en campos con espacios internos
docs: actualizar GUIA_ESTRUCTURADA con estado actual
```

---

## 8. Cómo ejecutar el pipeline

### Requisitos

```bash
pip install -r requirements.txt
```

### Configuración de entorno

```bash
# Copiar el template y completar las rutas
cp .env.example .env
# Editar .env con las rutas reales del entorno local
```

### Ejecución

```python
# Desde un notebook operativo o directamente en Python
from src.pipeline_alumnos import ejecutar_pipeline_alumnos

ejecutar_pipeline_alumnos(
    curso="1ro",
    division="1ra",
    anio=2025
)
```

> **Nota:** el pipeline modular está en implementación. Esta sección se actualiza a medida que los módulos quedan disponibles.

---

## 9. Cómo extender el proyecto

### Agregar una nueva fuente de datos

1. Crear `data/raw/[nombre_fuente]/` y colocar los archivos.
2. Agregar función `extraer_[fuente]_raw()` en `extractores.py`.
3. Agregar función `normalizar_[fuente]()` en `normalizacion.py`.
4. Agregar función `validar_[fuente]()` en `validacion.py`.
5. Si es una fuente de identidad, incorporar a la reconciliación en `reconciliacion.py`.
6. Si es una fuente de eventos, crear su propio flujo análogo a Marzo.
7. Documentar el contrato de la fuente antes de implementar.

### Agregar una nueva entidad (docentes, preceptores, etc.)

1. Crear contrato de entidad en `docs/contratos/vigentes/`.
2. Seguir la misma estructura: staging → validación → identidad → master.
3. Agregar módulo específico si la entidad tiene lógica compleja.
4. Agregar a `pipeline_alumnos.py` o crear un `pipeline_[entidad].py` equivalente.

### Regla general

> "No crear carpetas ni módulos por ansiedad futura.  
> Crear cuando aparece una fuente, entidad o módulo real."

---

## 10. Documentación de referencia

Toda la documentación técnica del proyecto vive en `docs/`:

| Documento | Ubicación | Descripción |
|---|---|---|
| Pipeline Maestro | `docs/pipeline/vigentes/` | Arquitectura completa de las 10 etapas |
| Contrato 01 — Datos | `docs/contratos/vigentes/` | Contrato de la fuente Datos |
| Contrato 02 — Legajos | `docs/contratos/vigentes/` | Contrato de la fuente Legajos |
| Contrato 03 — Marzo | `docs/contratos/vigentes/` | Contrato de la fuente Marzo |
| Contrato 04 — Contactos | `docs/contratos/vigentes/` | Contrato de la entidad Contactos |
| Contrato 05 — Arquitectura Modular | `docs/arquitectura/` | Responsabilidades de cada módulo |
| Contrato 06 — Arquitectura de Carpetas | `docs/arquitectura/` | Estructura física del proyecto |
| Backlog (00) | `docs/decisiones/` | Deudas técnicas y mejoras pendientes |

---

*EES N°2 School Database Pipeline — 2025*
