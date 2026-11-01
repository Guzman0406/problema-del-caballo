# Tour del Caballo — Agente de Búsqueda

Agente que resuelve el **Tour del Caballo** en un tablero de ajedrez de 8x8: partiendo de una casilla inicial, encuentra una secuencia de movimientos en "L" que visite las 64 casillas exactamente una vez.

El algoritmo es una **búsqueda en profundidad con backtracking (DFS)**, optimizada con la **heurística de Warnsdorff** para reducir drásticamente los callejones sin salida y encontrar una solución en tiempo razonable.

## Requisitos

- Python 3.10+
- `matplotlib` y `numpy` (solo necesarios si se activa la visualización gráfica)

## Instalación

```bash
python3 -m venv venv

# Linux/macOS (bash o zsh)
source venv/bin/activate
# Linux/macOS (fish)
source venv/bin/activate.fish
# Windows (PowerShell)
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

> Si vas a usar la visualización gráfica (`MOSTRAR_GUI = True`) en Linux, matplotlib necesita un backend de ventanas (Tk). En distros basadas en Arch:
> ```bash
> sudo pacman -S tk
> ```

## Uso

```bash
python3 main.py
```

El programa pide una casilla inicial en notación de ajedrez, por ejemplo:

```
Ingresa la casilla inicial (ejemplo: (a, 5)):
```

Letras válidas: `a` a `h` (columna). Números válidos: `1` a `8` (fila). Si el formato o los valores son inválidos, se muestra un mensaje de error sin detener el programa de forma abrupta.

Al terminar, imprime en consola el tablero resuelto con el número de paso en cada casilla (1 al 64). Si `MOSTRAR_GUI = True` en `main.py`, además abre una ventana con el tablero dibujado.

## Arquitectura

```text
Caballo/
├── src/
│   ├── core/          # Reglas base y utilidades
│   │   ├── config.py       # Constantes: tamaño del tablero y movimientos del caballo
│   │   ├── errors.py       # Excepciones personalizadas para validar el input
│   │   └── coordinates.py  # Conversión entre notación de ajedrez "(a,5)" e índices de matriz
│   │
│   ├── game/          # Lógica del juego
│   │   ├── board.py        # Creación del tablero y su impresión en consola
│   │   └── moves.py        # Cálculo de los saltos válidos del caballo
│   │
│   ├── agent/         # El agente de búsqueda
│   │   ├── heuristic.py    # Regla de Warnsdorff (conteo de salidas libres)
│   │   └── search.py       # Backtracking: resuelve el tour
│   │
│   └── ui/
│       └── gui.py          # Visualización del resultado con matplotlib
│
├── main.py            # Punto de entrada
└── requirements.txt
```

### Flujo de ejecución

1. `main.py` pide la casilla inicial y la convierte a índices de matriz con `convertir_a_indices`.
2. Crea el tablero (`crear_tablero`) y marca la casilla inicial con el paso `1`.
3. Llama a `resolver_tour`, que:
   - En cada casilla, calcula los saltos legales con `obtener_saltos_posibles`.
   - Los ordena con `ordenar_por_heuristica` (Warnsdorff): primero el salto que deja **menos** opciones futuras, calculado con `contar_salidas_libres`.
   - Marca la siguiente casilla y se llama recursivamente.
   - Si un camino no lleva a una solución completa, deshace la marca (backtracking) y prueba la siguiente candidata.
4. Si se completan las 64 casillas, imprime el tablero resuelto y, opcionalmente, lo grafica.

### Conceptos del agente (PEAS)

- **Performance:** completar las 64 casillas, validez de los movimientos, eficiencia (nodos explorados y retrocesos).
- **Environment:** tablero 8x8, acotado, no cambia por causas externas.
- **Actuators:** mover el caballo (marcar/desmarcar casillas), actualizar la GUI.
- **Sensors:** lectura de la posición actual y del estado del tablero (casillas visitadas).

Entorno: determinista, monoagente, secuencial (no episódico), completamente observable, discreto, estático y conocido.

## Próximas modificaciones

<!-- Usa esta sección para ir registrando cambios o ideas a futuro del proyecto. -->
