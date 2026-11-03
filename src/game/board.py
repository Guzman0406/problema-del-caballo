from src.core.config import TAMANO_TABLERO


def crear_tablero():
    """
    Crea una matriz de 8x8 llena de ceros.
    0 = casilla vacía.
    """
    tablero = []
    for i in range(TAMANO_TABLERO):
        fila = [0] * TAMANO_TABLERO
        tablero.append(fila)
    return tablero


def imprimir_tablero(tablero):
    """
    Imprime el tablero en la consola.
    """
    for fila in tablero:
        print(" ".join(f"{str(casilla):>4}" for casilla in fila))
    print("-" * 40)