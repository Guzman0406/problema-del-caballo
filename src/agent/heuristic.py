# Heurística de Warnsdorff.
from src.game.moves import obtener_saltos_posibles


def contar_salidas_libres(tablero, fila, columna):
    """
    Regla de Warnsdorff: Cuenta cuántos movimientos posibles tiene una casilla.
    
    Mientras menor sea este número, más prioridad tiene para ser visitada.
    """
    saltos = obtener_saltos_posibles(tablero, fila, columna)
    return len(saltos)