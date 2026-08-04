import os
import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkintermapview

class BusMXLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UPBC-BUS")
        self.root.geometry("400x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        # Localización de recursos en la carpeta actual del proyecto
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.ruta_imagen = os.path.join(self.base_dir, 'fondo.jpg')
        self.ruta_json = os.path.join(self.base_dir, 'rutas.json')

        self.turno_seleccionado = None
        self.datos_transporte = self.cargar_datos_externos()

        # Variables para almacenar trazos y unidades en el mapa
        self.marcador_autobus = None
        self.dibujo_trayecto = None
        
        # Variables core para controlar los hilos de animación fluida
        self.ruta_activa = None
        self.coordenadas_animacion = []
        self.indice_micro_paso = 0
        self.job_animacion = None  
        self.intervalo_milisegundos = 250

        self.contenedor = tk.Frame(self.root, bg="#ffffff")
        self.contenedor.pack(fill="both", expand=True)

        self.mostrar_pantalla_bienvenida()

    def cargar_datos_externos(self):
        """Lee la fuente de datos externa JSON de horarios y paraderos."""
        if os.path.exists(self.ruta_json):
            try:
                with open(self.ruta_json, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def limpiar_pantalla(self):
        """Detiene de forma segura cualquier hilo o animación activa antes de limpiar widgets."""
        if self.job_animacion:
            self.root.after_cancel(self.job_animacion)
            self.job_animacion = None
        for widget in self.contenedor.winfo_children():
            widget.destroy()
    # ==========================================
    # PANTALLA 1: BIENVENIDA
    # ==========================================
    def mostrar_pantalla_bienvenida(self):
        self.limpiar_pantalla()
        color_upbc_morado = "#6A1B9A"
        self.contenedor.configure(bg=color_upbc_morado)

        if os.path.exists(self.ruta_imagen):
            try:
                img_original = Image.open(self.ruta_imagen).convert("RGBA")
                ancho, alto = 400, 260
                img_rediseño = img_original.resize((ancho, alto), Image.Resampling.LANCZOS)
                
                datos_pixeles = img_rediseño.load()
                punto_inicio_fade = int(alto * 0.4) 
                
                for y in range(alto):
                    if y > punto_inicio_fade:
                        factor_transparencia = 1.0 - ((y - punto_inicio_fade) / (alto - punto_inicio_fade))
                        factor_transparencia = max(0.0, min(1.0, factor_transparencia))
                        for x in range(ancho):
                            r, g, b, a = datos_pixeles[x, y]
                            nuevo_alfa = int(a * factor_transparencia)
                            datos_pixeles[x, y] = (r, g, b, nuevo_alfa)

                self.foto_fondo = ImageTk.PhotoImage(img_rediseño)
                lbl_imagen = tk.Label(self.contenedor, image=self.foto_fondo, bg=color_upbc_morado)
                lbl_imagen.image = self.foto_fondo  
                lbl_imagen.pack(fill="x", side="top")
            except Exception:
                lbl_respaldo = tk.Label(self.contenedor, bg=color_upbc_morado, height=12)
                lbl_respaldo.pack(fill="x", side="top")
        else:
            lbl_respaldo = tk.Label(self.contenedor, bg=color_upbc_morado, height=12)
            lbl_respaldo.pack(fill="x", side="top")

        frame_contenido = tk.Frame(self.contenedor, bg="#ffffff", padx=30, pady=25)
        frame_contenido.pack(fill="both", expand=True, side="bottom")

        lbl_titulo = tk.Label(frame_contenido, text="UPBC-BUS", font=("Segoe UI", 36, "bold"), fg=color_upbc_morado, bg="#ffffff")
        lbl_titulo.pack(pady=(5, 2))

        lbl_subtitulo = tk.Label(frame_contenido, text="Selecciona tu horario de clases:", font=("Segoe UI", 12, "bold"), fg="#555555", bg="#ffffff")
        lbl_subtitulo.pack(pady=(0, 20))

        btn_matutino = tk.Button(
            frame_contenido, text="Turno Matutino", font=("Segoe UI", 12, "bold"), 
            bg=color_upbc_morado, fg="white", bd=0, padx=10, pady=12, cursor="hand2",
            command=lambda: self.seleccionar_turno("matutino")
        )
        btn_matutino.pack(fill="x", pady=8)

        btn_vespertino = tk.Button(
            frame_contenido, text="Turno Vespertino", font=("Segoe UI", 12, "bold"), 
            bg="#eeeeee", fg="#555555", activebackground="#cccccc", activeforeground="#333333",
            bd=1, relief="solid", padx=10, pady=12, cursor="hand2",
            command=lambda: self.seleccionar_turno("vespertino")
        )
        btn_vespertino.pack(fill="x", pady=8)

    def seleccionar_turno(self, turno):
        self.turno_seleccionado = turno
        self.mostrar_pantalla_mapa()

    # ==========================================
    # PANTALLA 2: MAPA INTERACTIVO
    # ==========================================
    def mostrar_pantalla_mapa(self):
        self.limpiar_pantalla()

        # 1. Configuración del mapa nativo de fondo
        self.mapa = tkintermapview.TkinterMapView(self.contenedor, corner_radius=0)
        self.mapa.place(x=0, y=0, width=400, height=680)
        self.mapa.set_position(32.6258, -115.3770)
        self.mapa.set_zoom(14)
        self.mapa.set_marker(32.6258, -115.3770, text="Campus UPBC")

        # 2. Tarjeta base inferior con altura corregida de la caja de scrolls
        self.panel_info = tk.Frame(self.contenedor, bg="#ffffff", bd=1, relief="solid", padx=15, pady=10)
        self.panel_info.place(x=0, y=440, width=400, height=240)

        handle = tk.Frame(self.panel_info, bg="#cccccc", width=40, height=4)
        handle.pack(pady=(0, 5))

        self.lbl_seccion_titulo = tk.Label(self.panel_info, text=f"Rutas disponibles ({self.turno_seleccionado.capitalize()}):", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#666666")
        self.lbl_seccion_titulo.pack(anchor="w", pady=1)

        self.lbl_tiempo_real = tk.Label(self.panel_info, text="Selecciona una ruta abajo para ver su estado...", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#ff7a1a")
        self.lbl_tiempo_real.pack(anchor="w", pady=1)

        # 3. Menú Deslizable Horizontal de Próximas Unidades Programadas (Clickeables)
        tk.Label(self.panel_info, text="🗂️ Próximas salidas (Haz clic para monitorear):", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#999999").pack(anchor="w", pady=(4, 0))
        
        self.frame_scroll_container = tk.Frame(self.panel_info, bg="#f9f9f9", bd=1, relief="sunken", height=50)
        self.frame_scroll_container.pack(fill="x", pady=5)

        self.canvas_horarios = tk.Canvas(self.frame_scroll_container, bg="#f9f9f9", bd=0, highlightthickness=0, height=45)
        scrollbar_h = tk.Scrollbar(self.frame_scroll_container, orient="horizontal", command=self.canvas_horarios.xview)
        self.frame_lista_horarios = tk.Frame(self.canvas_horarios, bg="#f9f9f9")

        self.frame_lista_horarios.bind("<Configure>", lambda e: self.canvas_horarios.configure(scrollregion=self.canvas_horarios.bbox("all")))
        self.canvas_horarios.create_window((0, 0), window=self.frame_lista_horarios, anchor="nw")
        self.canvas_horarios.configure(xscrollcommand=scrollbar_h.set)

        self.canvas_horarios.pack(fill="x", side="top")
        scrollbar_h.pack(fill="x", side="bottom")

        # Fila inferior fija para conmutar entre las dos empresas de camiones
        frame_opciones_camion = tk.Frame(self.panel_info, bg="#ffffff")
        frame_opciones_camion.pack(fill="x", pady=(5, 2))

        self.btn_amilpa = tk.Button(
            frame_opciones_camion, text="🚌 Ruta Amilpa", font=("Segoe UI", 10, "bold"),
            bg="#6A1B9A", fg="white", activebackground="#4A148C", activeforeground="white",
        command=lambda: self.consultar_tiempo_real_ruta("amilpa")
        )
        self.btn_amilpa.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_violeta = tk.Button(
            frame_opciones_camion, text="🚌 Ruta Violeta", font=("Segoe UI", 10, "bold"),
            bg="#D4AF37", fg="white", activebackground="#B89728", activeforeground="white",
        command=lambda: self.consultar_tiempo_real_ruta("violeta")
        )
        self.btn_violeta.pack(side="right", fill="x", expand=True, padx=(6, 0))

        btn_regresar_inicio = tk.Button(
            self.panel_info, text="← Cambiar de Turno / Horario", font=("Segoe UI", 9, "bold"),
            bg="#ffffff", fg="#999999", bd=0, cursor="hand2", command=self.mostrar_pantalla_bienvenida
        )
        btn_regresar_inicio.pack(side="bottom", pady=(2, 0))
    # ==========================================
    # SISTEMA DE SIMULACIÓN PROPORCIONAL Y FILTRADOS
    # ==========================================
    def consultar_tiempo_real_ruta(self, clave_ruta, horario_forzado=None):
        """Calcula el tiempo real usando el trazado local exacto del JSON sin depender de internet."""
        if self.job_animacion:
            self.root.after_cancel(self.job_animacion)
            self.job_animacion = None

        info_ruta = self.datos_transporte.get(clave_ruta, {})
        if not info_ruta: 
            return

        horarios_turno = info_ruta["horarios_upbc"].get(self.turno_seleccionado, [])
        ahora = datetime.now()
        hora_actual_str = ahora.strftime("%H:%M")
        
        proximo_horario = horario_forzado
        unidades_futuras = []

        if not proximo_horario:
            for h in horarios_turno:
                if h > hora_actual_str:
                    if not proximo_horario:
                        proximo_horario = h
                    else:
                        unidades_futuras.append(h)
        else:
            for h in horarios_turno:
                if h > hora_actual_str and h != proximo_horario:
                    unidades_futuras.append(h)

        if self.marcador_autobus: 
            self.marcador_autobus.delete()
            self.marcador_autobus = None
        if self.dibujo_trayecto: 
            self.dibujo_trayecto.delete()
            self.dibujo_trayecto = None
            
        for widget in self.frame_lista_horarios.winfo_children(): 
            widget.destroy()

        if proximo_horario:
            fmt = "%H:%M"
            diferencia = datetime.strptime(proximo_horario, fmt) - datetime.strptime(hora_actual_str, fmt)
            minutos_faltantes = int(diferencia.total_seconds() / 60)
            if minutos_faltantes <= 0: 
                minutos_faltantes = 1  

            self.lbl_seccion_titulo.config(text=f"📍 {info_ruta['nombre_completo']} — En Monitoreo")
            self.lbl_tiempo_real.config(text=f"⏱️ Llega a UPBC: {proximo_horario} (Faltan {minutos_faltantes} min)", fg="#ff7a1a")

            if not unidades_futuras:
                tk.Label(self.frame_lista_horarios, text=" No hay más unidades próximas", font=("Segoe UI", 9, "italic"), bg="#f9f9f9", fg="#777777").pack(padx=10, pady=5)
            for uf in unidades_futuras[:4]:
                btn_uf = tk.Button(
                    self.frame_lista_horarios, text=f" 🚌 Unidad: {uf} ", font=("Segoe UI", 9, "bold"),
                    bg="#eeeeee", fg="#444444", bd=1, relief="solid", padx=5, pady=2, cursor="hand2",
                    command=lambda h_clic=uf: self.consultar_tiempo_real_ruta(clave_ruta, horario_forzado=h_clic)
                )
                btn_uf.pack(side="left", padx=4, pady=5)

            # ====================================================================
            # TRAZADO LOCAL DIRECTO (MIGAJAS DE PAN INMANIPULABLES)
            # ====================================================================
            color_linea = "#6A1B9A" if clave_ruta == "amilpa" else "#D4AF37"
            
            # Cargamos de forma forzada la lista densa de coordenadas urbanas de Mexicali
            puntos_reales_calle = info_ruta["camino_perfecto_calles"]

            # 1. Dibujamos la línea que sigue las avenidas de forma nativa
            self.dibujo_trayecto = self.mapa.set_path(puntos_reales_calle, color=color_linea, width=4)

            # 2. Generación de micro-pasos fluidos sobre el trazado local
            self.coordenadas_animacion = []
            densidad_pasos = 4  # Densidad mayor para suavizar el movimiento en las esquinas
            for i in range(len(puntos_reales_calle) - 1):
                lat_i, lng_i = puntos_reales_calle[i]
                lat_f, lng_f = puntos_reales_calle[i+1]
                for j in range(densidad_pasos):
                    fraction = j / densidad_pasos
                    inter_lat = lat_i + (lat_f - lat_i) * fraction
                    inter_lng = lng_i + (lng_f - lng_i) * fraction
                    self.coordenadas_animacion.append((inter_lat, inter_lng))
            
            # --- TELEMETRÍA EN TIEMPO REAL STRICTO ---
            segundos_reales = minutos_faltantes * 60 
            milisegundos_totales = segundos_reales * 1000
            total_micro_pasos = len(self.coordenadas_animacion)
            
            self.intervalo_milisegundos = int(milisegundos_totales / total_micro_pasos)
            self.intervalo_milisegundos = max(200, self.intervalo_milisegundos)

            # Inicializar el marcador en el primer micro-paso de la calle de forma segura
            self.indice_micro_paso = 0
            if len(self.coordenadas_animacion) > 0:
                lat_init, lng_init = self.coordenadas_animacion[0]
                self.marcador_autobus = self.mapa.set_marker(lat_init, lng_init, text=f"🚍 {clave_ruta.upper()}")
                self.mapa.set_position(lat_init, lng_init)

            self.animar_movimiento_autobus()
        else:
            self.lbl_seccion_titulo.config(text=f"📍 {info_ruta['nombre_completo']}")
            self.lbl_tiempo_real.config(text="❌ No hay más corridas programadas para este turno.", fg="#d32f2f")
            tk.Label(self.frame_lista_horarios, text=" Trayectos concluidos por hoy", font=("Segoe UI", 9, "italic"), bg="#f9f9f9", fg="#777777").pack(padx=10, pady=5)
            self.mapa.set_position(32.6258, -115.3770)

    def animar_movimiento_autobus(self):
        """Mueve el autobús de forma fluida usando la velocidad proporcional calculada."""
        if self.indice_micro_paso >= len(self.coordenadas_animacion):
            self.lbl_tiempo_real.config(text="🏁 ¡El autobús ha llegado al Campus UPBC!", fg="#00a79d")
            return

        lat, lng = self.coordenadas_animacion[self.indice_micro_paso]
        self.marcador_autobus.set_position(lat, lng)

        self.indice_micro_paso += 1
        self.job_animacion = self.root.after(self.intervalo_milisegundos, self.animar_movimiento_autobus)

# ==========================================
# DISPARADOR FINAL DE LA INTERFAZ NATIVA
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = BusMXLApp(root)
    root.mainloop()
