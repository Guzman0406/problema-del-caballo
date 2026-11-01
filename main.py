# main.py
# Punto de entrada del proyecto.

from src.core.coordinates import convertir_a_indices
from src.game.board import crear_tablero, imprimir_tablero
from src.agent.search import resolver_tour
from src.core.errors import ColumnaInvalidaError, FilaInvalidaError, FormatoCoordenadaError

# Cambia este valor a True para ver la gráfica al final.
# Déjalo en False para probar solo por consola.
MOSTRAR_GUI = True


def main():
    print("=" * 50)
    print("   TOUR DEL CABALLO - AGENTE DE BÚSQUEDA")
    print("=" * 50)

    entrada = input("Ingresa la casilla inicial (ejemplo: (a, 5)): ")

    try:
        # Convertir la entrada del usuario a índices de matriz
        fila_inicial, columna_inicial = convertir_a_indices(entrada)

        # Crear el tablero
        tablero = crear_tablero()

        # Marcar la casilla inicial como paso 1
        tablero[fila_inicial][columna_inicial] = 1

        # Resolver el tour
        print("\nBuscando solución...")
        exito = resolver_tour(tablero, fila_inicial, columna_inicial, 1)

        if exito:
            print("\n¡Solución encontrada!\n")
            imprimir_tablero(tablero)

            if MOSTRAR_GUI:
                from src.ui.gui import mostrar_resultado
                mostrar_resultado(tablero)
        else:
            print("No se encontró solución desde esa casilla.")

    except (ColumnaInvalidaError, FilaInvalidaError, FormatoCoordenadaError) as error:
        print(f"\n{error}")


if __name__ == "__main__":
    main()