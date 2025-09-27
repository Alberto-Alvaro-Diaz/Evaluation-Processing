from thefuzz import fuzz
import unicodedata
import re

# --- Función de normalización ---
def normalizar(texto):
    texto = texto.lower().strip()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto

# --- Función para validar nombres (solo letras y espacios) ---
def es_valido(nombre: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+", nombre))

# --- Función para agrupar nombres similares ---
def nombres_repetidos(listas, umbral = 85, min_repeticiones = 2):
    # Paso 1: aplanar lista
    todos = [nombre for sublista in listas for nombre in sublista]

    # Paso 2: normalizar
    normalizados = [(nombre, normalizar(nombre)) for nombre in todos]

    # Paso 3: agrupar por similitud
    grupos = []
    usados = set()

    for i, (original, norm) in enumerate(normalizados):
        if i in usados:
            continue
        grupo = [original]
        usados.add(i)

        for j, (other_orig, other_norm) in enumerate(normalizados[i+1:], start=i+1):
            if j in usados:
                continue
            sim = fuzz.partial_ratio(norm, other_norm)
            if sim >= umbral:
                grupo.append(other_orig)
                usados.add(j)

        grupos.append(grupo)

    # Paso 4: quedarnos solo con grupos que tengan al menos `min_repeticiones`
    unicos = []
    for grupo in grupos:
        if len(grupo) >= min_repeticiones:
            representante = max(grupo, key=len)  # el más largo como representativo
            if es_valido(representante):  # solo nombres con letras
                unicos.append(representante)

    return unicos