import pandas as pd

from src.utils_texto import limpiar_texto

# ========================================
# HELPERS DE DOMINIO
# ========================================

def normalizar_nombre_alumno(valor):
    """
    Normaliza un nombre de alumno aplicando la limpieza textual estándar del proyecto.
    """
    return limpiar_texto(valor)

def normalizar_identificador(valor):
    """
    Normaliza un identificador administrativo escolar
    conservándolo como texto.
    """
    return limpiar_texto(valor)

def separar_telefono(valor):
    """
    Separa un teléfono crudo en número telefónico y tipo de contacto.

    Si el último carácter es una letra, se interpreta como tipo_contacto.
    El resto se conserva como telefono_num.
    """
    valor = limpiar_texto(valor)

    if valor[-1:].isalpha():
        tipo_contacto = valor[-1]
        telefono_num = valor[:-1]
    else:
        tipo_contacto = None
        telefono_num = valor

    return telefono_num, tipo_contacto

def normalizar_encabezado(valor):
    """
    Normaliza encabezados RAW antes del mapeo a nombres canónicos internos.
    """
    valor = limpiar_texto(valor)

    valor = valor.replace("\n", "")

    valor = valor.replace(" ", "")

    return valor

# ========================================
# ESTANDARIZACIÓN DE COLUMNAS RAW
# ========================================

COLUMNAS_DATOS = {
    "Nº": "numero_raw",
    "": "numero_raw",

    "APELLIDOYNOMBRESDELALUMNO": "nombre_original",
    "APELLIDOYNOMBREDELALUMNO": "nombre_original",
    "APELLIDOYNOMBRE": "nombre_original",

    "LM": "libro_matriz_raw",
    "F": "folio_raw",

    "Leg": "legajo_raw",
    "Leg.": "legajo_raw",
    "L": "legajo_raw",

    "ESC": "escuela_procedencia_raw",

    "D.N.I.": "dni_raw",
    "D.N.I": "dni_raw",

    "F.N.": "fecha_nacimiento_raw",
    "F.N": "fecha_nacimiento_raw",

    "Lugar": "lugar_nacimiento_raw",

    "E": "edad_raw",
    "Edad": "edad_raw",

    "Dirección": "direccion_raw",
    "Teléfono": "telefono_raw",
}

COLUMNAS_LEGAJOS = {
    "Nº": "numero_raw",
    "": "numero_raw",

    "APELLIDOYNOMBRESDELALUMNO": "nombre_original",
    "APELLIDOYNOMBREDELALUMNO": "nombre_original",
    "APELLIDOYNOMBRE": "nombre_original",

    "LM": "libro_matriz_raw",
    "F": "folio_raw",

    "Leg": "legajo_raw",
    "Leg.": "legajo_raw",
    "L": "legajo_raw",
}

COLUMNAS_MARZO = {
    "Nº": "numero_raw",
    "": "numero_raw",

    "APELLIDOYNOMBRESDELALUMNO": "nombre_original",
    "APELLIDOYNOMBREDELALUMNO": "nombre_original",
    "APELLIDOYNOMBRE": "nombre_original",
}

COLUMNAS_CONTEXTUALES = {
    "curso",
    "division",
    "anio",
    "fuente",
    "archivo_origen"
}

def estandarizar_columnas_datos(df):
    """
    Estandariza los encabezados RAW de Datos
    a nombres canónicos internos del pipeline.

    Si encuentra una columna no reconocida, frena el proceso.
    """
    df = df.copy()

    columnas_normalizadas = {}

    for columna in df.columns:

        if columna in COLUMNAS_CONTEXTUALES:
            columnas_normalizadas[columna] = columna
            continue

        encabezado_normalizado = normalizar_encabezado(columna)

        if encabezado_normalizado not in COLUMNAS_DATOS:
            raise ValueError(
                f"Columna no reconocida en fuente Datos: {columna}"
            )

        columnas_normalizadas[columna] = COLUMNAS_DATOS[encabezado_normalizado]

    df = df.rename(columns=columnas_normalizadas)

    return df

def estandarizar_columnas_legajos(df):
    """
    Estandariza los encabezados RAW de Legajos
    a nombres canónicos internos del pipeline.

    Si encuentra una columna no reconocida, frena el proceso.
    """
    df = df.copy()

    columnas_normalizadas = {}

    for columna in df.columns:

        if columna in COLUMNAS_CONTEXTUALES:
            columnas_normalizadas[columna] = columna
            continue

        encabezado_normalizado = normalizar_encabezado(columna)

        if encabezado_normalizado not in COLUMNAS_LEGAJOS:
            raise ValueError(
                f"Columna no reconocida en fuente Legajos: {columna}"
            )

        columnas_normalizadas[columna] = COLUMNAS_LEGAJOS[encabezado_normalizado]

    df = df.rename(columns=columnas_normalizadas)

    return df

def estandarizar_columnas_marzo(df):
    """
    Estandariza los encabezados RAW de Marzo
    a nombres canónicos internos del pipeline.

    Si encuentra una columna no reconocida, frena el proceso.
    """
    df = df.copy()

    columnas_normalizadas = {}

    for columna in df.columns:

        if columna in COLUMNAS_CONTEXTUALES:
            columnas_normalizadas[columna] = columna
            continue

        encabezado_normalizado = normalizar_encabezado(columna)

        if encabezado_normalizado not in COLUMNAS_MARZO:
            raise ValueError(
                f"Columna no reconocida en fuente Marzo: {columna}"
            )

        columnas_normalizadas[columna] = COLUMNAS_MARZO[encabezado_normalizado]

    df = df.rename(columns=columnas_normalizadas)

    return df

# ========================================
# NORMALIZACIÓN FUENTE DATOS
# ========================================

def normalizar_datos(df_datos_raw):
    """
    Normaliza la fuente Datos desde RAW hacia STG.
    """
    df = df_datos_raw.copy()

    df = estandarizar_columnas_datos(df)

    df["nombre_completo"] = df["nombre_original"].apply(normalizar_nombre_alumno)

    df["libro_matriz"] = df["libro_matriz_raw"].apply(normalizar_identificador)

    df["folio"] = df["folio_raw"].apply(normalizar_identificador)

    df["legajo"] = df["legajo_raw"].apply(normalizar_identificador)

    if "escuela_procedencia_raw" in df.columns:
        df["escuela_procedencia"] = df["escuela_procedencia_raw"].apply(limpiar_texto)
    else:
        df["escuela_procedencia"] = None

    df["dni"] = df["dni_raw"].apply(limpiar_texto)

    df["fecha_nacimiento"] = df["fecha_nacimiento_raw"].apply(limpiar_texto)

    df["lugar_nacimiento"] = df["lugar_nacimiento_raw"].apply(limpiar_texto)

    df["edad"] = df["edad_raw"].apply(limpiar_texto)

    df["direccion"] = df["direccion_raw"].apply(limpiar_texto)

    telefonos = df["telefono_raw"].apply(separar_telefono)

    df["telefono_num"] = telefonos.apply(lambda x: x[0])

    df["tipo_contacto"] = telefonos.apply(lambda x: x[1])

    return df

# ========================================
# NORMALIZACIÓN FUENTE LEGAJOS
# ========================================

def normalizar_legajos(df_legajos_raw):
    """
    Normaliza la fuente Legajos desde RAW hacia STG.
    """
    df = df_legajos_raw.copy()

    df = estandarizar_columnas_legajos(df)

    df["nombre_completo"] = df["nombre_original"].apply(normalizar_nombre_alumno)

    df["libro_matriz"] = df["libro_matriz_raw"].apply(normalizar_identificador)

    df["folio"] = df["folio_raw"].apply(normalizar_identificador)

    df["legajo"] = df["legajo_raw"].apply(normalizar_identificador)

    return df

# ========================================
# NORMALIZACIÓN FUENTE MARZO
# ========================================

def normalizar_marzo(df_marzo_raw):
    """
    Normaliza la fuente Marzo desde RAW hacia STG.

    Versión inicial: asigna presencia_simple por defecto.
    La inferencia completa de eventos queda pendiente para Etapa 6.
    """
    df = df_marzo_raw.copy()

    df = estandarizar_columnas_marzo(df)

    df["nombre_completo"] = df["nombre_original"].apply(normalizar_nombre_alumno)

    df["observacion_marzo"] = None

    df["tipo_evento_inferido"] = "presencia_simple"
  
    df["requiere_revision"] = False

    return df