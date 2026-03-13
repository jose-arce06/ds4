from __future__ import annotations
import csv
import unicodedata
from typing import Dict, List, Any, Optional, Iterable, Tuple
from Animal import Animal

def _norm(s: str) -> str:
    s = (s or "").strip().casefold()
    s = ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')
    return s


def cargar_csv_en_diccionario(ruta_csv: str, campo_clave: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    registros: Dict[str, Dict[str, Any]] = {}
    with open(ruta_csv, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        headers = [h.strip() for h in reader.fieldnames or []]
        if not headers:
            return {}
        key_index = headers.index(campo_clave) if campo_clave else 0

        for row in reader:
            row_norm = {
                k.strip(): (v.strip() if isinstance(v, str) else v)
                for k, v in row.items()
            }
            key = row_norm[headers[key_index]]
            registros[key] = row_norm
    return registros


def escribir_diccionario_a_csv(ruta_csv: str, data: Dict[str, Dict[str, Any]], orden_campos):
    with open(ruta_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=orden_campos)
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


def construir_indices_clases(clases: Dict[str, Dict[str, Any]]):
    by_id = {}
    by_tipo = {}
    for row in clases.values():
        _id = row["Clase_id"].strip()
        tipo = row["Clase_tipo"].strip()
        by_id[_id] = tipo
        by_tipo[_norm(tipo)] = _id
    return by_id, by_tipo


def listar_por_clase(animales, clases_by_id, clases_by_tipo, clase_input):
    val = clase_input.strip()

    if val in clases_by_id:
        clase_id = val
    else:
        clase_id = clases_by_tipo.get(_norm(val), None)

    if not clase_id:
        return []

    resultados = []
    for row in animales.values():
        if row["clase"] == clase_id:
            nombre = row["nombre_animal"]
            tipo = clases_by_id[clase_id]

            features = [
                col for col, v in row.items()
                if col not in ("nombre_animal", "clases") and v == "1"
            ]
            resultados.append(Animal(nombre, tipo, features))

    return resultados


def listar_por_caracteristica(animales, caracteristica):
    car_norm = _norm(caracteristica)

    sample = next(iter(animales.values()))
    columnas = sample.keys()

    columna_real = None
    for col in columnas:
        if col not in ("nombre_animal", "clase"):
            if _norm(col) == car_norm:
                columna_real = col
                break

    if not columna_real:
        return []

    resultados = []
    for row in animales.values():
        if row[columna_real] == "1":
            nombre = row["nombre_animal"]
            clase = row["clase"]
            resultados.append(Animal(nombre, f"Clase {clase}", [columna_real]))

    return resultados


def agregar_animal(animales, clases_by_id, clases_by_tipo, nombre, clase_input, features):
    if clase_input in clases_by_id:
        clase_id = clase_input
    else:
        clase_id = clases_by_tipo.get(_norm(clase_input), None)
        if not clase_id:
            raise ValueError("La clases no existe.")

    sample = next(iter(animales.values()))
    columnas = list(sample.keys())

    nueva_fila = {}
    for col in columnas:
        if col == "nombre_animal":
            nueva_fila[col] = nombre
        elif col == "clase":
            nueva_fila[col] = clase_id
        else:
            nueva_fila[col] = "0"

    features_norm = {_norm(f) for f in features}
    for col in columnas:
        if _norm(col) in features_norm:
            nueva_fila[col] = "1"

    animales[nombre] = nueva_fila

    car_names = [k for k, v in nueva_fila.items()
                 if k not in ("nombre_animal", "clase") and v == "1"]

    return Animal(nombre, clases_by_id[clase_id], car_names)


def menu_opcion():
    print("\nMENU ZOOLOGICO")
    print("1) Listar animales por CLASE")
    print("2) Listar animales por CARACTERISTICA")
    print("3) Agregar un ANIMAL")
    print("4) Agregar VARIOS animales")
    print("5) Guardar y SALIR")

    while True:
        o = input("Opción es del 1-5: ").strip()
        if o in {"1", "2", "3", "4", "5"}:
            return int(o)
        print("Invalido.")