import random
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from src.core.config import TAMANO_TABLERO
from src.core.errors import ColumnaInvalidaError, FilaInvalidaError, FormatoCoordenadaError
from src.core.coordinates import convertir_a_indices, convertir_a_coordenada
from src.game.board import crear_tablero
from src.game.moves import obtener_saltos_posibles
from src.agent.heuristic import contar_salidas_libres
from src.agent.search import resolver_tour, ordenar_por_heuristica

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

CELDA = 54
MARGEN = 24  # espacio alrededor del tablero para las coordenadas
LETRAS_COLUMNAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

BG_APP = "#0f1115"
BG_PANEL = "#171a21"
BG_PANEL_ALT = "#1d212b"
BORDER = "#262b36"
TEXT_PRIMARY = "#e8ecf1"
TEXT_MUTED = "#8891a1"
ACCENT = "#22c58b"
ACCENT_HOVER = "#1b9f70"
ACCENT_SOFT = "#15332a"
DESCARTADA = "#5b6577"
TRAZO = "#394257"
BOARD_LIGHT = "#2a2f3c"
BOARD_DARK = "#181c25"
VISITADA = "#1f6f5c"
CABALLO = "#f2b84b"


class AppCaballo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tour del Caballo")
        self.configure(fg_color=BG_APP)
        self.resizable(False, False)

        self.tablero_resuelto = None
        self.tablero_parcial = None
        self.posicion_actual = None
        self.paso_animacion = 1
        self.animando = False
        self.pausado = False
        self.after_id = None
        self.callback_pendiente = None

        self._construir_header()
        self._construir_cuerpo()

    # ---------- construcción de la interfaz ----------

    def _construir_header(self):
        header = ctk.CTkFrame(self, fg_color=BG_PANEL, corner_radius=14)
        header.pack(fill="x", padx=16, pady=(16, 10))

        izquierda = ctk.CTkFrame(header, fg_color="transparent")
        izquierda.pack(side="left", padx=14, pady=12)

        fila_titulo = ctk.CTkFrame(izquierda, fg_color="transparent")
        fila_titulo.pack(anchor="w")
        ctk.CTkLabel(fila_titulo, text="♞", font=ctk.CTkFont(size=22), text_color=ACCENT, width=28).pack(side="left")
        ctk.CTkLabel(
            fila_titulo, text="Tour del Caballo", font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_PRIMARY
        ).pack(side="left", padx=(6, 10))
        ctk.CTkLabel(
            fila_titulo, text="Heurística de Warnsdorff", font=ctk.CTkFont(size=10, weight="bold"),
            text_color=ACCENT, fg_color=ACCENT_SOFT, corner_radius=10, height=22, anchor="center",
        ).pack(side="left")

        ctk.CTkLabel(
            izquierda, text="Visualizador interactivo del recorrido del caballo",
            font=ctk.CTkFont(size=11), text_color=TEXT_MUTED, anchor="w",
        ).pack(anchor="w", pady=(4, 0))

        derecha = ctk.CTkFrame(header, fg_color="transparent")
        derecha.pack(side="right", padx=14, pady=12)
        self.lbl_progreso = ctk.CTkLabel(
            derecha, text="Progreso: 0 / 64", font=ctk.CTkFont(size=12, weight="bold"), text_color=TEXT_PRIMARY
        )
        self.lbl_progreso.pack(anchor="e")
        self.barra_progreso = ctk.CTkProgressBar(
            derecha, width=180, progress_color=ACCENT, fg_color=BOARD_DARK
        )
        self.barra_progreso.set(0)
        self.barra_progreso.pack(anchor="e", pady=(6, 0))

    def _construir_cuerpo(self):
        cuerpo = ctk.CTkFrame(self, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # ----- columna izquierda: tablero -----
        col_izq = ctk.CTkFrame(cuerpo, fg_color=BG_PANEL, corner_radius=14)
        col_izq.pack(side="left", padx=(0, 10))

        self.lbl_estado = ctk.CTkLabel(
            col_izq, text="● Listo para comenzar", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_MUTED, anchor="w",
        )
        self.lbl_estado.pack(anchor="w", padx=14, pady=(14, 8))

        tam = CELDA * TAMANO_TABLERO
        tam_canvas = tam + 2 * MARGEN
        self.canvas = tk.Canvas(col_izq, width=tam_canvas, height=tam_canvas, bg=BG_PANEL_ALT, highlightthickness=0)
        self.canvas.pack(padx=14, pady=(0, 10))

        self.celdas = {}
        self.knight_id = None
        self.trail_ids = []
        self.candidato_ids = []
        self._dibujar_tablero_vacio()

        ctk.CTkLabel(
            col_izq,
            text=("\U0001F4A1  Regla de Warnsdorff: el caballo salta a la casilla candidata que, desde ahí, "
                  "tiene el MENOR número de salidas libres hacia casillas aún no visitadas."),
            font=ctk.CTkFont(size=11), text_color=TEXT_MUTED, wraplength=tam_canvas, justify="left",
            fg_color=BG_PANEL_ALT, corner_radius=10, anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 14))

        # ----- columna derecha: configuración + registro -----
        col_der = ctk.CTkFrame(cuerpo, fg_color="transparent")
        col_der.pack(side="left", fill="both", expand=True)

        panel_config = ctk.CTkFrame(col_der, fg_color=BG_PANEL, corner_radius=14)
        panel_config.pack(fill="x")

        ctk.CTkLabel(
            panel_config, text="⚙  PANEL DE CONFIGURACIÓN", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_PRIMARY, anchor="w",
        ).pack(anchor="w", padx=14, pady=(14, 10))

        ctk.CTkLabel(
            panel_config, text="Casilla inicial (ej. (a, 5)):", font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED, anchor="w",
        ).pack(anchor="w", padx=14)

        fila_entry = ctk.CTkFrame(panel_config, fg_color="transparent")
        fila_entry.pack(fill="x", padx=14, pady=(4, 12))
        self.entrada = ctk.CTkEntry(
            fila_entry, placeholder_text="(a, 5)", fg_color=BOARD_DARK, border_color=BORDER,
            text_color=TEXT_PRIMARY,
        )
        self.entrada.insert(0, "(a, 5)")
        self.entrada.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            fila_entry, text="\U0001F3B2 Azar", width=66, fg_color=BOARD_DARK, hover_color=BORDER,
            text_color=TEXT_PRIMARY, command=self._casilla_aleatoria,
        ).pack(side="left", padx=(8, 0))

        ctk.CTkLabel(
            panel_config, text="Retraso por paso:", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED, anchor="w",
        ).pack(anchor="w", padx=14)
        self.velocidad = ctk.CTkSlider(
            panel_config, from_=150, to=1500, number_of_steps=27,
            progress_color=ACCENT, button_color=ACCENT, button_hover_color=ACCENT_HOVER,
            command=self._actualizar_etiqueta_velocidad,
        )
        self.velocidad.set(600)
        self.velocidad.pack(fill="x", padx=14, pady=(4, 2))
        self.lbl_velocidad = ctk.CTkLabel(
            panel_config, text="600 ms", font=ctk.CTkFont(size=11, weight="bold"), text_color=ACCENT, anchor="e",
        )
        self.lbl_velocidad.pack(fill="x", padx=14, pady=(0, 14))

        self.btn_resolver = ctk.CTkButton(
            panel_config, text="▶  Resolver y animar", fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color="#07231a", font=ctk.CTkFont(size=13, weight="bold"), height=36,
            command=self._iniciar,
        )
        self.btn_resolver.pack(fill="x", padx=14, pady=(0, 8))

        fila_botones = ctk.CTkFrame(panel_config, fg_color="transparent")
        fila_botones.pack(fill="x", padx=14, pady=(0, 14))
        self.btn_pausar = ctk.CTkButton(
            fila_botones, text="⏸ Pausar", fg_color=BOARD_DARK, hover_color=BORDER, text_color=TEXT_PRIMARY,
            state="disabled", command=self._alternar_pausa,
        )
        self.btn_pausar.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(
            fila_botones, text="↺ Reiniciar", fg_color=BOARD_DARK, hover_color=BORDER, text_color=TEXT_PRIMARY,
            command=self._reiniciar,
        ).pack(side="left", fill="x", expand=True, padx=(6, 0))

        panel_log = ctk.CTkFrame(col_der, fg_color=BG_PANEL, corner_radius=14)
        panel_log.pack(fill="both", expand=True, pady=(10, 0))

        fila_log_header = ctk.CTkFrame(panel_log, fg_color="transparent")
        fila_log_header.pack(fill="x", padx=14, pady=(12, 6))
        ctk.CTkLabel(
            fila_log_header, text="\U0001F5D2  REGISTRO DE DECISIONES", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")
        self.lbl_pasos = ctk.CTkLabel(
            fila_log_header, text="0 pasos", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED,
        )
        self.lbl_pasos.pack(side="right")

        self.registro = ctk.CTkTextbox(
            panel_log, fg_color=BG_PANEL_ALT, text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=11, family="Consolas"), wrap="word",
        )
        self.registro.pack(fill="both", expand=True, padx=14, pady=(0, 10))
        self._log_inicial()
        self.registro.configure(state="disabled")

        fila_chips = ctk.CTkFrame(panel_log, fg_color="transparent")
        fila_chips.pack(fill="x", padx=14, pady=(0, 14))
        ctk.CTkLabel(fila_chips, text="● Elegido (menor grado)", font=ctk.CTkFont(size=10), text_color=ACCENT).pack(side="left")
        ctk.CTkLabel(fila_chips, text="● Descartadas", font=ctk.CTkFont(size=10), text_color=DESCARTADA).pack(side="left", padx=(12, 0))

    # ---------- tablero (Canvas) ----------

    def _dibujar_tablero_vacio(self):
        self.canvas.delete("all")
        self.celdas = {}
        self.trail_ids = []
        self.candidato_ids = []
        for fila in range(TAMANO_TABLERO):
            for columna in range(TAMANO_TABLERO):
                x1, y1 = MARGEN + columna * CELDA, MARGEN + fila * CELDA
                x2, y2 = x1 + CELDA, y1 + CELDA
                color = BOARD_LIGHT if (fila + columna) % 2 == 0 else BOARD_DARK
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                texto = self.canvas.create_text(
                    x1 + CELDA / 2, y1 + CELDA / 2, text="", font=("Consolas", 12, "bold"), fill=TEXT_PRIMARY
                )
                self.celdas[(fila, columna)] = (rect, texto)
        self._dibujar_coordenadas()
        self.knight_id = self.canvas.create_text(-50, -50, text="♞", font=("Arial", 24), fill=CABALLO)

    def _dibujar_coordenadas(self):
        # columnas a-h de izquierda a derecha y filas 1-8
        fin = MARGEN + CELDA * TAMANO_TABLERO
        fuente = ("Consolas", 11, "bold")
        for i in range(TAMANO_TABLERO):
            centro = MARGEN + i * CELDA + CELDA / 2
            letra = LETRAS_COLUMNAS[i]
            self.canvas.create_text(centro, MARGEN / 2, text=letra, fill=TEXT_MUTED, font=fuente)
            self.canvas.create_text(centro, fin + MARGEN / 2, text=letra, fill=TEXT_MUTED, font=fuente)
            self.canvas.create_text(MARGEN / 2, centro, text=str(i + 1), fill=TEXT_MUTED, font=fuente)
            self.canvas.create_text(fin + MARGEN / 2, centro, text=str(i + 1), fill=TEXT_MUTED, font=fuente)

    def _centro(self, fila, columna):
        return MARGEN + columna * CELDA + CELDA / 2, MARGEN + fila * CELDA + CELDA / 2

    def _mover_caballo(self, fila, columna):
        x, y = self._centro(fila, columna)
        self.canvas.coords(self.knight_id, x, y)
        self.canvas.tag_raise(self.knight_id)

    def _marcar_celda(self, fila, columna, numero):
        rect, texto = self.celdas[(fila, columna)]
        self.canvas.itemconfig(rect, fill=VISITADA)
        self.canvas.itemconfig(texto, text=str(numero), fill="white")
        self.canvas.tag_raise(texto)

    def _limpiar_candidatos(self):
        for item_id in self.candidato_ids:
            self.canvas.delete(item_id)
        self.candidato_ids = []

    def _siguiente_real(self, valor_paso):
        for fila in range(TAMANO_TABLERO):
            for columna in range(TAMANO_TABLERO):
                if self.tablero_resuelto[fila][columna] == valor_paso:
                    return (fila, columna)
        return None

    # ---------- registro de decisiones ----------

    def _log_inicial(self):
        self.registro.insert("end", "Selecciona una casilla y pulsa 'Resolver y animar'\npara ver cómo opera la heurística, paso a paso.\n")

    def _log(self, texto):
        self.registro.configure(state="normal")
        self.registro.insert("end", texto + "\n")
        self.registro.see("end")
        self.registro.configure(state="disabled")

    def _reset_log(self):
        self.registro.configure(state="normal")
        self.registro.delete("1.0", "end")
        self.registro.configure(state="disabled")

    # ---------- utilidades de interfaz ----------

    def _actualizar_etiqueta_velocidad(self, valor):
        self.lbl_velocidad.configure(text=f"{int(round(valor))} ms")

    def _casilla_aleatoria(self):
        fila, columna = random.randint(0, TAMANO_TABLERO - 1), random.randint(0, TAMANO_TABLERO - 1)
        self.entrada.delete(0, "end")
        self.entrada.insert(0, convertir_a_coordenada(fila, columna))

    def _set_estado(self, texto, color):
        self.lbl_estado.configure(text=texto, text_color=color)

    def _programar(self, ms, callback):
        self.callback_pendiente = callback
        self.after_id = self.after(int(ms), callback)

    # ---------- control: iniciar / pausar / reiniciar ----------

    def _iniciar(self):
        if self.animando:
            return

        try:
            fila_inicial, columna_inicial = convertir_a_indices(self.entrada.get())
        except (ColumnaInvalidaError, FilaInvalidaError, FormatoCoordenadaError) as error:
            messagebox.showerror("Coordenada inválida", str(error))
            return

        tablero = crear_tablero()
        tablero[fila_inicial][columna_inicial] = 1

        self._set_estado("● Buscando solución...", TEXT_MUTED)
        self.update_idletasks()

        exito = resolver_tour(tablero, fila_inicial, columna_inicial, 1)

        if not exito:
            self._set_estado("● No se encontró solución desde esa casilla", "#e8847a")
            return

        self.tablero_resuelto = tablero
        self._dibujar_tablero_vacio()
        self._reset_log()

        self.tablero_parcial = crear_tablero()
        self.tablero_parcial[fila_inicial][columna_inicial] = 1
        self.posicion_actual = (fila_inicial, columna_inicial)
        self.paso_animacion = 1

        self._marcar_celda(fila_inicial, columna_inicial, 1)
        self._mover_caballo(fila_inicial, columna_inicial)
        self._log(f"Paso 1: inicio en {convertir_a_coordenada(fila_inicial, columna_inicial)}")
        self._actualizar_progreso()

        self.animando = True
        self.pausado = False
        self.btn_resolver.configure(state="disabled")
        self.btn_pausar.configure(state="normal", text="⏸ Pausar")
        self._set_estado("● Animando el recorrido...", ACCENT)

        self._animar_decision()

    def _alternar_pausa(self):
        if not self.animando:
            return
        if not self.pausado:
            self.pausado = True
            if self.after_id is not None:
                self.after_cancel(self.after_id)
                self.after_id = None
            self.btn_pausar.configure(text="▶ Reanudar")
            self._set_estado("⏸ Pausado", TEXT_MUTED)
        else:
            self.pausado = False
            self.btn_pausar.configure(text="⏸ Pausar")
            self._set_estado("● Animando el recorrido...", ACCENT)
            if self.callback_pendiente is not None:
                self.callback_pendiente()

    def _reiniciar(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.callback_pendiente = None
        self.animando = False
        self.pausado = False
        self.tablero_resuelto = None
        self.tablero_parcial = None
        self.paso_animacion = 1

        self._dibujar_tablero_vacio()
        self._reset_log()
        self._log_inicial_reiniciado()
        self.barra_progreso.set(0)
        self.lbl_progreso.configure(text="Progreso: 0 / 64")
        self.lbl_pasos.configure(text="0 pasos")
        self.btn_resolver.configure(state="normal")
        self.btn_pausar.configure(state="disabled", text="⏸ Pausar")
        self._set_estado("● Listo para comenzar", TEXT_MUTED)

    def _log_inicial_reiniciado(self):
        self.registro.configure(state="normal")
        self.registro.insert("end", "Reiniciado. Selecciona una casilla y pulsa 'Resolver y animar'.\n")
        self.registro.configure(state="disabled")

    def _actualizar_progreso(self):
        self.barra_progreso.set(self.paso_animacion / (TAMANO_TABLERO * TAMANO_TABLERO))
        self.lbl_progreso.configure(text=f"Progreso: {self.paso_animacion} / {TAMANO_TABLERO * TAMANO_TABLERO}")
        self.lbl_pasos.configure(text=f"{self.paso_animacion} pasos")

    # ---------- animación de la decisión (Warnsdorff en vivo) ----------

    def _animar_decision(self):
        if self.paso_animacion >= TAMANO_TABLERO * TAMANO_TABLERO:
            self.animando = False
            self.btn_resolver.configure(state="normal")
            self.btn_pausar.configure(state="disabled")
            self._set_estado("✓ ¡Tour completo!", ACCENT)
            return

        fila_actual, columna_actual = self.posicion_actual
        candidatos = obtener_saltos_posibles(self.tablero_parcial, fila_actual, columna_actual)
        candidatos_ordenados = ordenar_por_heuristica(self.tablero_parcial, candidatos)
        # La casilla real del siguiente paso se lee del tour ya resuelto, no se
        # asume "siempre la de menor grado": si el agente tuvo que retroceder
        # en este tramo, la elegida puede no ser la primera de la lista.
        elegido = self._siguiente_real(self.paso_animacion + 1)

        self._mostrar_opciones(fila_actual, columna_actual, candidatos_ordenados, elegido)

        retraso = self.velocidad.get()
        self._programar(retraso, lambda: self._confirmar_decision(fila_actual, columna_actual, elegido, retraso))

    def _mostrar_opciones(self, fila_actual, columna_actual, candidatos, elegido):
        self._limpiar_candidatos()
        x0, y0 = self._centro(fila_actual, columna_actual)
        for (fila, columna) in candidatos:
            x1, y1 = self._centro(fila, columna)
            es_elegido = (fila, columna) == elegido
            color = ACCENT if es_elegido else DESCARTADA
            ancho = 3 if es_elegido else 2
            trazo = () if es_elegido else (4, 3)
            linea = self.canvas.create_line(x0, y0, x1, y1, fill=color, width=ancho, arrow=tk.LAST, dash=trazo)
            self.candidato_ids.append(linea)

            grado = contar_salidas_libres(self.tablero_parcial, fila, columna)
            etiqueta = self.canvas.create_text(x1, y1 - 17, text=str(grado), fill=color, font=("Consolas", 10, "bold"))
            self.candidato_ids.append(etiqueta)

    def _confirmar_decision(self, fila_actual, columna_actual, elegido, retraso):
        self._limpiar_candidatos()

        fila, columna = elegido
        x0, y0 = self._centro(fila_actual, columna_actual)
        x1, y1 = self._centro(fila, columna)
        linea = self.canvas.create_line(x0, y0, x1, y1, fill=TRAZO, width=2)
        self.trail_ids.append(linea)

        grado_elegido = contar_salidas_libres(self.tablero_parcial, fila, columna)

        self.paso_animacion += 1
        self.tablero_parcial[fila][columna] = self.paso_animacion
        self._marcar_celda(fila, columna, self.paso_animacion)
        self._mover_caballo(fila, columna)
        self.posicion_actual = (fila, columna)

        self._log(
            f"Paso {self.paso_animacion - 1}→{self.paso_animacion}: "
            f"{convertir_a_coordenada(fila_actual, columna_actual)} → "
            f"{convertir_a_coordenada(fila, columna)}  (grado {grado_elegido})"
        )
        self._actualizar_progreso()

        self._programar(max(80, retraso // 3), self._animar_decision)


def main():
    app = AppCaballo()
    app.mainloop()


if __name__ == "__main__":
    main()
