import csv
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import numpy as np

from src.agent.search import resolver_tour
from src.core.config import TAMANO_TABLERO
from src.core.coordinates import convertir_a_coordenada
from src.game.board import crear_tablero

CARPETA_SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
LETRAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def correr_todas_las_casillas():
    resultados = []
    for fila in range(TAMANO_TABLERO):
        for columna in range(TAMANO_TABLERO):
            tablero = crear_tablero()
            tablero[fila][columna] = 1
            exito = resolver_tour(tablero, fila, columna, 1)
            resultados.append((fila, columna, exito))
    return resultados


def guardar_csv(resultados):
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    ruta = os.path.join(CARPETA_SALIDA, "resultados.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["casilla", "fila", "columna", "tiene_solucion"])
        for fila, columna, exito in resultados:
            escritor.writerow([convertir_a_coordenada(fila, columna), fila, columna, exito])
    return ruta


def graficar(resultados):
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    matriz = np.zeros((TAMANO_TABLERO, TAMANO_TABLERO))
    for fila, columna, exito in resultados:
        matriz[fila][columna] = 1 if exito else 0

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(matriz, cmap="RdYlGn", vmin=0, vmax=1)

    ax.set_xticks(range(TAMANO_TABLERO))
    ax.set_xticklabels(LETRAS)
    ax.set_yticks(range(TAMANO_TABLERO))
    ax.set_yticklabels(range(1, TAMANO_TABLERO + 1))

    for fila in range(TAMANO_TABLERO):
        for columna in range(TAMANO_TABLERO):
            simbolo = "OK" if matriz[fila][columna] == 1 else "X"
            ax.text(columna, fila, simbolo, ha="center", va="center", fontsize=9, color="black")

    total_exitos = int(matriz.sum())
    ax.set_title(f"Tour del Caballo: casillas con solucion ({total_exitos}/{TAMANO_TABLERO * TAMANO_TABLERO})")
    plt.tight_layout()

    ruta = os.path.join(CARPETA_SALIDA, "mapa_soluciones.png")
    plt.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def main():
    inicio = time.time()
    resultados = correr_todas_las_casillas()
    duracion = time.time() - inicio

    ruta_csv = guardar_csv(resultados)
    ruta_png = graficar(resultados)

    fallos = [(fila, columna) for fila, columna, exito in resultados if not exito]
    total = TAMANO_TABLERO * TAMANO_TABLERO
    print(f"Resultados: {total - len(fallos)}/{total} casillas con solucion.")
    if fallos:
        print("Casillas SIN solucion:", [convertir_a_coordenada(fila, columna) for fila, columna in fallos])
    else:
        print("Todas las casillas tienen solucion con este algoritmo.")
    print(f"Tiempo del barrido: {duracion:.4f} s")
    print(f"CSV guardado en: {ruta_csv}")
    print(f"Grafica guardada en: {ruta_png}")


if __name__ == "__main__":
    main()
