class ColumnaInvalidaError(Exception):
    """Se lanza cuando la columna no está entre 'a' y 'h'."""
    def __init__(self, letra):
        self.mensaje = f"Error: La columna '{letra}' no es válida. Debe ser una letra de la 'a' a la 'h'."
        super().__init__(self.mensaje)


class FilaInvalidaError(Exception):
    """Se lanza cuando la fila no está entre 1 y 8."""
    def __init__(self, numero):
        self.mensaje = f"Error: La fila '{numero}' no es válida. Debe ser un número del 1 al 8."
        super().__init__(self.mensaje)


class FormatoCoordenadaError(Exception):
    """Se lanza cuando el formato de la coordenada es incorrecto."""
    def __init__(self):
        self.mensaje = "Error: Formato incorrecto. Usa (letra, número), por ejemplo: (a, 5)."
        super().__init__(self.mensaje)