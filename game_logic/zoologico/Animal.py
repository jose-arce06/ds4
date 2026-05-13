# Animal.py
from dataclasses import dataclass
from typing import List, Iterable, Dict, Any

@dataclass
class Animal:
    nombre: str
    clase: str
    caracteristicas: List[str]

    def __init__(self, nombre: str, clase: str, caracteristicas: Iterable[str] | str):
        self.nombre = nombre.strip()
        self.clase = clase.strip()

        if isinstance(caracteristicas, str):
            raw = caracteristicas.strip()
            if raw == "":
                self.caracteristicas = []
            else:
                sep = ";" if ";" in raw else ","
                self.caracteristicas = [c.strip() for c in raw.split(sep) if c.strip()]
        else:
            self.caracteristicas = [str(c).strip() for c in caracteristicas if str(c).strip()]

    def __str__(self):
        car = "; ".join(self.caracteristicas) if self.caracteristicas else "—"
        return f"{self.nombre} (Clase: {self.clase}) → Características: {car}"

    def __repr__(self):
        return f"Animal(nombre={self.nombre!r}, clase={self.clase!r}, caracteristicas={self.caracteristicas!r})"
    

    def a_dict(self) -> Dict[str, Any]:
        return {
            "nombre": self.nombre,
            "clase": self.clase,
            "caracteristicas": ";".join(self.caracteristicas)
        }