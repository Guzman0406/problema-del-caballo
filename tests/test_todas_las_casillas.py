import pytest

from src.agent.search import resolver_tour
from src.core.config import TAMANO_TABLERO
from src.core.coordinates import convertir_a_coordenada
from src.game.board import crear_tablero

TODAS_LAS_CASILLAS = [
    (fila, columna)
    for fila in range(TAMANO_TABLERO)
    for columna in range(TAMANO_TABLERO)
]


@pytest.mark.parametrize(
    "fila,columna",
    TODAS_LAS_CASILLAS,
    ids=[convertir_a_coordenada(fila, columna) for fila, columna in TODAS_LAS_CASILLAS],
)
def test_resolver_tour_desde_casilla(fila, columna):
    tablero = crear_tablero()
    tablero[fila][columna] = 1

    exito = resolver_tour(tablero, fila, columna, 1)

    assert exito, (
        f"No se encontro un tour completo empezando en "
        f"{convertir_a_coordenada(fila, columna)}"
    )
