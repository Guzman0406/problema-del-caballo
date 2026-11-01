# coordinates.py
# Convierte entre coordenadas de ajedrez y coordenadas de matriz.

from src.core.errors import ColumnaInvalidaError, FilaInvalidaError, FormatoCoordenadaError
from src.core.config import TAMANO_TABLERO
# Arreglo con las letras válidas para las columnas
LETRAS_VALIDAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def convertir_a_indices(coordenada_str):
    """
    Recibe un texto como "(a, 5)" y devuelve la tupla (fila, columna).
    Ejemplo: "(a, 5)" -> (4, 0)
    """
    # 1. Limpiamos espacios y paréntesis
    coordenada_str = coordenada_str.replace("(", "").replace(")", "").replace(" ", "")

    # 2. Verificamos que tenga una coma
    if "," not in coordenada_str:
        raise FormatoCoordenadaError()

    # 3. Separamos letra y número
    letra, numero_str = coordenada_str.split(",")
    letra = letra.lower()

    # 4. Validar la columna (letra)
    if letra not in LETRAS_VALIDAS:
        raise ColumnaInvalidaError(letra)

    columna = LETRAS_VALIDAS.index(letra)

    # 5. Validar la fila (número)
    try:
        numero = int(numero_str)
        if numero < 1 or numero > TAMANO_TABLERO:
            raise FilaInvalidaError(numero)
    except ValueError:
        raise FilaInvalidaError(numero_str)

    fila = numero - 1  # Convertimos del 1-8 al 0-7

    return (fila, columna)


def convertir_a_coordenada(fila, columna):
    """
    Hace lo contrario. Recibe (4, 0) y devuelve "(a, 5)".
    Útil para mostrar mensajes al usuario.
    """
    letra = LETRAS_VALIDAS[columna]
    numero = fila + 1
    return f"({letra}, {numero})"