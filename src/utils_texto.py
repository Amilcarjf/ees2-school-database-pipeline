import re
import unicodedata


# ========================================
# LIMPIEZA DE TEXTO
# ========================================

def convertir_a_texto(valor):
    """
    Convierte cualquier valor a string.
    """
    return str(valor)


def colapsar_espacios(valor):
    """
    Elimina espacios externos y reduce espacios internos múltiples a uno.
    """
    valor = str(valor).strip()

    valor = re.sub(r"\s+", " ", valor)

    return valor


def normalizar_unicode(valor):
    """
    Normaliza texto a Unicode NFC.
    """
    return unicodedata.normalize("NFC", valor)


def limpiar_texto(valor):
    """
    Convierte cualquier valor a texto,
    elimina espacios redundantes y
    normaliza Unicode a NFC.
    """
    valor = convertir_a_texto(valor)

    valor = colapsar_espacios(valor)

    valor = normalizar_unicode(valor)

    return valor

# ========================================
# FUNCIONES DE COLUMNA
# ========================================

def limpiar_columna_texto(serie):
    """
    Aplica limpiar_texto() a cada valor de una Serie de pandas.
    """
    return serie.apply(limpiar_texto)

