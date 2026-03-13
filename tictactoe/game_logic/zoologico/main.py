from __future__ import annotations
import os
from pathlib import Path
from funciones import (
    cargar_csv_en_diccionario,
    escribir_diccionario_a_csv,
    construir_indices_clases,
    listar_por_clase,
    listar_por_caracteristica,
    agregar_animal,
    menu_opcion,
)

RUTA_CLASES = Path(r"C:\Users\Home\OneDrive\Documents\ds4\tictactoe\game_logic\zoologico\clases.csv")
RUTA_ZOO    = Path(r"C:\Users\Home\OneDrive\Documents\ds4\tictactoe\game_logic\zoologico\zoo.csv")

for p in (RUTA_CLASES, RUTA_ZOO):
    if not p.exists():
        raise FileNotFoundError(f"No se encontró: {p}")

HEADERS_CLASES = ["Clase_id", "Clase_tipo"]
HEADERS_ZOO = [
    "nombre_animal","pelo","plumas","huevos","leche","vuela","acuatico","depredador",
    "dientes","espinazo","respira","venenoso","aletas","patas","cola","domestico",
    "tamanio_gato","clase"
]

def cargar_datos():
    clases = cargar_csv_en_diccionario(str(RUTA_CLASES), campo_clave="Clase_id")
    animales = cargar_csv_en_diccionario(str(RUTA_ZOO), campo_clave="nombre_animal")
    return clases, animales

def guardar_datos(clases, animales):
    escribir_diccionario_a_csv(str(RUTA_CLASES), clases, HEADERS_CLASES)
    escribir_diccionario_a_csv(str(RUTA_ZOO), animales, HEADERS_ZOO)

if __name__ == "__main__":
    print("Iniciando sistema de Zoológico")
    clases, animales = cargar_datos()
    by_id, by_tipo = construir_indices_clases(clases)

    while True:
        op = menu_opcion()
        if op == 1:
            c = input("\nClase id o nombre: ").strip()
            res = listar_por_clase(animales, by_id, by_tipo, c)
            if res:
                print("\nResultados:")
                for a in res: print(" -", a)
            else:
                print("\nNo se encontraron animales en esa clase.")
        elif op == 2:
            car = input("\nCaracterística: ").strip()
            res = listar_por_caracteristica(animales, car)
            if res:
                print("\nResultados:")
                for a in res: print(" -", a)
            else:
                print("\nNo se encontraron.")
        elif op == 3:
            nombre = input("\nNombre del animal: ").strip()
            clase_in = input("Clase id o tipo: ").strip()
            feats = input("Características separadas por ';': ").strip()
            lista = [x.strip() for x in feats.split(";") if x.strip()]
            try:
                nuevo = agregar_animal(animales, by_id, by_tipo, nombre, clase_in, lista)
                print("\nAgregado →", nuevo)
            except Exception as e:
                print("Error:", e)
        elif op == 4:
            print("\nAgregar varios ENTER para terminar")
            while True:
                nombre = input("\nNombre: ").strip()
                if not nombre: break
                clase_in = input("Clase: ").strip()
                feats = input("Características (;): ").strip()
                lista = [x.strip() for x in feats.split(";") if x.strip()]
                try:
                    nuevo = agregar_animal(animales, by_id, by_tipo, nombre, clase_in, lista)
                    print("Agregado ", nuevo)
                except Exception as e:
                    print("Error:", e)
        elif op == 5:
            print("Guardando")
            guardar_datos(clases, animales)
            print("Listo Adios ")
            break