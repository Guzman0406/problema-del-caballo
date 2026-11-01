# gui.py
# Visualización del tablero con matplotlib.

import matplotlib.pyplot as plt
import numpy as np
from src.core.config import TAMANO_TABLERO


def mostrar_resultado(tablero):
    """
    Dibuja el tablero con los números del recorrido (1 al 64).
    """
    # Convertimos el tablero a un arreglo de numpy para dibujarlo
    datos = np.array(tablero)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Colores: blanco para el fondo, azul para resaltar el inicio (1)
    ax.imshow(datos, cmap='Blues', alpha=0.7)

    # Poner las líneas del tablero
    for i in range(TAMANO_TABLERO + 1):
        ax.axhline(i - 0.5, color='black', linewidth=1)
        ax.axvline(i - 0.5, color='black', linewidth=1)

    # Poner las letras (columnas) y números (filas) como en el ajedrez
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ax.set_xticks(range(TAMANO_TABLERO))
    ax.set_xticklabels(letras)
    ax.set_yticks(range(TAMANO_TABLERO))
    ax.set_yticklabels(range(8, 0, -1))  # Filas de 8 a 1 (como en ajedrez)

    # Escribir el número de paso en cada casilla
    for fila in range(TAMANO_TABLERO):
        for columna in range(TAMANO_TABLERO):
            numero = tablero[fila][columna]
            ax.text(columna, fila, str(numero),
                    ha='center', va='center',
                    fontsize=10, color='black')

    ax.set_title("Recorrido del Caballo (Tour del Caballo)")
    plt.tight_layout()
    plt.show()