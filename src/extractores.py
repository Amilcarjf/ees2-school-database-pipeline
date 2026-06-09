import pandas as pd

from docx import Document


# ========================================
# CONSTANTES ESTRUCTURALES
# ========================================

CANTIDAD_COLUMNAS_DATOS = 12

CANTIDAD_COLUMNAS_LEGAJOS = 5

CANTIDAD_COLUMNAS_MARZO = 2

# ========================================
# EXTRACCIÓN DE TABLAS DOCX
# ========================================

def extraer_tabla_docx(ruta_archivo):
    """
    Extrae la primera tabla de un archivo .docx
    y devuelve una lista de filas.
    """
    documento = Document(ruta_archivo)

    tabla = documento.tables[0]

    filas = []

    for fila in tabla.rows:

        celdas = []

        for celda in fila.cells:

            celdas.append(celda.text)

        filas.append(celdas)

    return filas


# ========================================
# CONSTRUCCIÓN DE DATAFRAMES RAW
# ========================================

def crear_dataframe_raw(filas):
    """
    Convierte una lista de filas en un DataFrame pandas.
    Usa la primera fila como encabezado.
    """
    columnas = filas[0]

    datos = filas[1:]

    df = pd.DataFrame(datos, columns=columnas)

    return df


# ========================================
# VALIDACIÓN ESTRUCTURAL DE EXTRACCIÓN
# ========================================

def validar_cantidad_columnas(df, cantidad_esperada):
    """
    Verifica que un DataFrame tenga la cantidad esperada de columnas.
    """
    cantidad_actual = len(df.columns)

    if cantidad_actual != cantidad_esperada:
        raise ValueError(
            f"Cantidad de columnas inesperada. "
            f"Esperadas: {cantidad_esperada}. "
            f"Encontradas: {cantidad_actual}."
        )


# ========================================
# EXTRACCIÓN FUENTE DATOS
# ========================================

def extraer_datos_raw(ruta_archivo, curso, division, anio):
    """
    Extrae la fuente Datos desde un archivo .docx
    y devuelve un DataFrame RAW con metadata contextual.
    """
    filas = extraer_tabla_docx(ruta_archivo)

    df = crear_dataframe_raw(filas)

    validar_cantidad_columnas(df, CANTIDAD_COLUMNAS_DATOS)

    df["curso"] = curso

    df["division"] = division

    df["anio"] = anio

    df["fuente"] = "datos"

    df["archivo_origen"] = ruta_archivo

    return df

# ========================================
# EXTRACCIÓN FUENTE LEGAJOS
# ========================================

def extraer_legajos_raw(ruta_archivo, curso, division, anio):
    """
    Extrae la fuente Legajos desde un archivo .docx
    y devuelve un DataFrame RAW con metadata contextual.
    """
    filas = extraer_tabla_docx(ruta_archivo)

    df = crear_dataframe_raw(filas)

    validar_cantidad_columnas(df, CANTIDAD_COLUMNAS_LEGAJOS)

    df["curso"] = curso

    df["division"] = division

    df["anio"] = anio

    df["fuente"] = "legajos"

    df["archivo_origen"] = ruta_archivo

    return df

# ========================================
# EXTRACCIÓN FUENTE MARZO
# ========================================

def extraer_marzo_raw(ruta_archivo, curso, division, anio):
    """
    Extrae la fuente Marzo desde un archivo .docx
    y devuelve un DataFrame RAW con metadata contextual.
    """
    filas = extraer_tabla_docx(ruta_archivo)

    df = crear_dataframe_raw(filas)

    validar_cantidad_columnas(df, CANTIDAD_COLUMNAS_MARZO)

    df["curso"] = curso

    df["division"] = division

    df["anio"] = anio

    df["fuente"] = "marzo"

    df["archivo_origen"] = ruta_archivo

    return df