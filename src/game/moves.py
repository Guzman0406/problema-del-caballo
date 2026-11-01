# moves.py
# Lógica de los saltos del caballo.

from src.core.config import MOVIMIENTOS_CABALLO, TAMANO_TABLERO


def obtener_saltos_posibles(tablero, fila_actual, columna_actual):
    """
    Devuelve una lista de tuplas (fila, columna) a las que el caballo puede saltar.
    Solo devuelve movimientos dentro del tablero y en casillas vacías (0).
    """
    saltos_validos = []

    for cambio_fila, cambio_columna in MOVIMIENTOS_CABALLO:
        nueva_fila = fila_actual + cambio_fila
        nueva_columna = columna_actual + cambio_columna

        # ¿Está dentro del tablero?
        if 0 <= nueva_fila < TAMANO_TABLERO and 0 <= nueva_columna < TAMANO_TABLERO:
            # ¿La casilla está vacía?
            if tablero[nueva_fila][nueva_columna] == 0:
                saltos_validos.append((nueva_fila, nueva_columna))

    return saltos_validos