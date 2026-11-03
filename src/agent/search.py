# El agente de búsqueda con Backtracking y heurística.

from src.game.moves import obtener_saltos_posibles
from src.agent.heuristic import contar_salidas_libres
from src.core.config import TAMANO_TABLERO

"Saber cual es el camino con menor salidas"
def ordenar_por_heuristica(tablero, saltos_posibles):
    con_prioridad = []
    for fila, columna in saltos_posibles:
        salidas_futuras = contar_salidas_libres(tablero, fila, columna)
        con_prioridad.append((salidas_futuras, (fila, columna)))
    "con_prioridad = [(3, (2,1)), (1, (5,0)), (2, (3,3))] ejemplo"

    con_prioridad.sort()
    "con_prioridad = [(1, (5,0)), (2, (3,3)), (3, (2,1))]"

    resultado = []
    for _, casilla in con_prioridad:
        resultado.append(casilla)
    return resultado
    "[(5,0), (3,3), (2,1)]"




def resolver_tour(tablero, fila_actual, columna_actual, paso_actual):
    """Backtracking: intenta completar el tour desde la posición actual."""
    if paso_actual == TAMANO_TABLERO * TAMANO_TABLERO:
        return True

    saltos = obtener_saltos_posibles(tablero, fila_actual, columna_actual) # trae las opciones sin orden
    saltos = ordenar_por_heuristica(tablero, saltos) # le da orden para saber a cual brincar

    for fila, columna in saltos:
        tablero[fila][columna] = paso_actual + 1

        if resolver_tour(tablero, fila, columna, paso_actual + 1):
            return True

        tablero[fila][columna] = 0  # no funcionó: deshacer y probar el siguiente

    return False
