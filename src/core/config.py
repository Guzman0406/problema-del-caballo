
# Tamaño del tablero (8x8)
TAMANO_TABLERO = 8

# Los 8 movimientos posibles del caballo (cambio_fila, cambio_columna)
# Recuerda: En matrices las filas crecen hacia ABAJO.
MOVIMIENTOS_CABALLO = [
    (-2, -1), (-2, 1),   # Arriba 2, Izquierda/Derecha 1
    (-1, -2), (-1, 2),   # Arriba 1, Izquierda/Derecha 2
    (1, -2),  (1, 2),    # Abajo 1, Izquierda/Derecha 2
    (2, -1),  (2, 1)     # Abajo 2, Izquierda/Derecha 1
]