import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkintermapview

class BusMXLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BusMXL")
        self.root.geometry("400x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.ruta_imagen = os.path.join(self.base_dir, 'fondo.jpg')

        self.contenedor = tk.Frame(self.root, bg="#ffffff")
        self.contenedor.pack(fill="both", expand=True)

        self.mostrar_pantalla_bienvenida()

    def limpiar_pantalla(self):
        """Elimina todos los widgets activos en el contenedor."""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        # PANTALLA 1: BIENVENIDA
    def mostrar_pantalla_bienvenida(self):
        self.limpiar_pantalla()

        if os.path.exists(self.ruta_imagen):
            img_original = Image.open(self.ruta_imagen)
            img_rediseño = img_original.resize((400, 250), Image.Resampling.LANCZOS)
            self.foto_fondo = ImageTk.PhotoImage(img_rediseño)
            
            lbl_imagen = tk.Label(self.contenedor, image=self.foto_fondo, bg="#ffffff")
            lbl_imagen.pack(fill="x", side="top")
        else:
            lbl_respaldo = tk.Label(self.contenedor, bg="#e5e5e5", height=10)
            lbl_respaldo.pack(fill="x", side="top")

        frame_contenido = tk.Frame(self.contenedor, bg="#ffffff", padx=30, pady=20)
        frame_contenido.pack(fill="both", expand=True)

        lbl_titulo = tk.Label(frame_contenido, text="BusMXL", font=("Segoe UI", 36, "bold"), fg="#00a79d", bg="#ffffff")
        lbl_titulo.pack(pady=(5, 2))

        lbl_subtitulo = tk.Label(frame_contenido, text="¡Bienvenido!", font=("Segoe UI", 16, "bold"), fg="#000000", bg="#ffffff")
        lbl_subtitulo.pack(pady=(0, 15))

        btn_permitir_ubi = tk.Button(
            frame_contenido, 
            text="Permitir ubicación", 
            font=("Segoe UI", 11, "bold"), 
            bg="#00a79d", 
            fg="white", 
            activebackground="#008c84", 
            activeforeground="white",
            bd=1, 
            relief="solid",
            padx=10, 
            pady=10,
            cursor="hand2",
            command=self.mostrar_pantalla_mapa
        )
        btn_permitir_ubi.pack(fill="x", pady=5)

        btn_manual_ubi = tk.Button(
            frame_contenido, 
            text="Ingresar zona manualmente", 
            font=("Segoe UI", 11, "bold"), 
            bg="#eeeeee", 
            fg="#555555", 
            activebackground="#cccccc", 
            activeforeground="#333333",
            bd=1, 
            relief="solid",
            padx=10, 
            pady=10,
            cursor="hand2",
            command=self.mostrar_pantalla_zonas  # <-- Acción actualizada aquí
        )
        btn_manual_ubi.pack(fill="x", pady=5)

        # PANTALLA INTERMEDIA: INGRESAR ZONA MANUALMENTE
    def mostrar_pantalla_zonas(self):
        self.limpiar_pantalla()

        frame_zonas = tk.Frame(self.contenedor, bg="#ffffff", padx=25, pady=30)
        frame_zonas.pack(fill="both", expand=True)

        lbl_titulo_seccion = tk.Label(frame_zonas, text="Ingresa tu zona", font=("Segoe UI", 20, "bold"), fg="#00a79d", bg="#ffffff")
        lbl_titulo_seccion.pack(anchor="w", pady=(0, 2))

        lbl_descripcion = tk.Label(frame_zonas, text="Escribe una colonia, avenida o zona de Mexicali.", font=("Segoe UI", 10), fg="#666666", bg="#ffffff")
        lbl_descripcion.pack(anchor="w", pady=(0, 20))

        frame_input = tk.Frame(frame_zonas, bg="#f5f5f5", bd=1, relief="solid", padx=10, pady=8)
        frame_input.pack(fill="x", pady=(0, 25))

        lbl_search_icon = tk.Label(frame_input, text="🔍", font=("Segoe UI", 11), bg="#f5f5f5", fg="#888888")
        lbl_search_icon.pack(side="left", padx=(0, 5))

        entry_zona = tk.Entry(frame_input, font=("Segoe UI", 11), bd=0, bg="#f5f5f5", fg="#000000")
        entry_zona.insert(0, "Mexicali, Baja California")
        entry_zona.pack(side="left", fill="x", expand=True)

        sugerencias = [
            {"nombre": "📍 XXXXXXX", "lat": 32.6635, "lng": -115.4855, "zoom": 15},
            {"nombre": "📍 XXXXXXX", "lat": 32.6520, "lng": -115.4920, "zoom": 15},
            {"nombre": "📍 XXXXXXX", "lat": 32.6601, "lng": -115.4050, "zoom": 14},
            {"nombre": "📍 XXXXXXX", "lat": 32.6315, "lng": -115.4420, "zoom": 15},
            {"nombre": "📍 UPBC", "lat": 32.6258, "lng": -115.3770, "zoom": 14}
        ]
        for zona in sugerencias:
            btn_zona = tk.Button(
                frame_zonas,
                text=zona["nombre"],
                font=("Segoe UI", 11, "bold"),
                anchor="w",
                bg="#ffffff",
                fg="#333333",
                activebackground="#f5f5f5",
                activeforeground="#00a79d",
                bd=1,
                relief="solid",
                padx=15,
                pady=12,
                cursor="hand2",
                # Al hacer clic, pasa las coordenadas específicas a la función encargada de inicializar el mapa
                command=lambda z=zona: self.mostrar_pantalla_mapa_con_coordenadas(z["lat"], z["lng"], z["zoom"])
            )
            btn_zona.pack(fill="x", pady=6)

        btn_volver = tk.Button(
            frame_zonas,
            text="← Volver al inicio",
            font=("Segoe UI", 10, "bold"),
            bg="#eeeeee",
            fg="#555555",
            bd=0,
            cursor="hand2",
            command=self.mostrar_pantalla_bienvenida
        )
        btn_volver.pack(side="bottom", fill="x", pady=10)

    def mostrar_pantalla_mapa_con_coordenadas(self, lat, lng, zoom_personalizado=13):
        """Inicializa la pantalla del mapa moviendo la cámara al sector seleccionado."""
        self.mostrar_pantalla_mapa()
        # Reposiciona el mapa activo según la zona seleccionada de forma inmediata
        self.mapa.set_position(lat, lng)
        self.mapa.set_zoom(zoom_personalizado)

    # PANTALLA 2: MAPA INTERACTIVO PRINCIPAL

    def mostrar_pantalla_mapa(self):
        self.limpiar_pantalla()

        self.mapa = tkintermapview.TkinterMapView(self.contenedor, corner_radius=0)
        self.mapa.place(x=0, y=0, width=400, height=680)
        
        self.mapa.set_position(32.6278, -115.4545)
        self.mapa.set_zoom(13)

        self.mapa.set_marker(32.6275, -115.4442, text="Parada UABC - Línea 9")

        self.frame_busqueda = tk.Frame(self.contenedor, bg="#ffffff", bd=1, relief="solid", padx=10, pady=5)
        self.frame_busqueda.place(x=20, y=20, width=360, height=45)

        lbl_icono = tk.Label(self.frame_busqueda, text="🔍", font=("Segoe UI", 12), bg="#ffffff", fg="#666666")
        lbl_icono.pack(side="left", padx=(0, 5))

        self.entry_buscar = tk.Entry(self.frame_busqueda, font=("Segoe UI", 11), bd=0, bg="#ffffff", fg="#333333")
        self.entry_buscar.insert(0, "Buscar ruta o parada... (Ej. UABC)")
        self.entry_buscar.pack(side="left", fill="both", expand=True)
        self.entry_buscar.bind("<FocusIn>", lambda e: self.entry_buscar.delete(0, 'end') if self.entry_buscar.get() == "Buscar ruta o parada... (Ej. UABC)" else None)

        self.btn_mostrar_panel = tk.Button(
            self.contenedor, 
            text="📋 Mostrar Info", 
            font=("Segoe UI", 10, "bold"), 
            bg="#00a79d", 
            fg="white",
            command=self.abrir_panel
        )

        self.panel_info = tk.Frame(self.contenedor, bg="#ffffff", bd=1, relief="solid", padx=20, pady=15)
        self.panel_info.place(x=0, y=460, width=400, height=220)

        handle = tk.Frame(self.panel_info, bg="#cccccc", width=40, height=4)
        handle.pack(pady=(0, 15))

        lbl_parada = tk.Label(self.panel_info, text="PARADA: Frente a UABC", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#000000")
        lbl_parada.pack(anchor="w")

        lbl_bus1 = tk.Label(self.panel_info, text="⏳ Próximo Autobús: Ruta 9 - 7 min", font=("Segoe UI", 11), bg="#ffffff", fg="#333333")
        lbl_bus1.pack(anchor="w", pady=5)

        lbl_bus2 = tk.Label(self.panel_info, text="🚌 Siguiente Unidad: Ruta 9 - 22 min", font=("Segoe UI", 11), bg="#ffffff", fg="#333333")
        lbl_bus2.pack(anchor="w", pady=(0, 15))

        frame_botones = tk.Frame(self.panel_info, bg="#ffffff")
        frame_botones.pack(fill="x", side="bottom")

        btn_favorito = tk.Button(frame_botones, text="⭐ Favorito", font=("Segoe UI", 10, "bold"), bg="#e6f6f5", fg="#00a79d", bd=1, relief="solid", padx=8, pady=8)
        btn_favorito.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_cerrar = tk.Button(frame_botones, text="Cerrar", font=("Segoe UI", 10, "bold"), bg="#eeeeee", fg="#555555", bd=1, relief="solid", padx=8, pady=8, command=self.cerrar_panel)
        btn_cerrar.pack(side="right", fill="x", expand=True, padx=(5, 0))

        self.btn_ajustar_vista = tk.Button(
            self.contenedor,
            text="⚙️ Ajustar área",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#333333",
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.mostrar_pantalla_sin_paradas  # Llama a la nueva interfaz
        )
        self.btn_ajustar_vista.place(x=20, y=415, width=110, height=30)
        frame_botones = tk.Frame(self.panel_info, bg="#ffffff")
        frame_botones.pack(fill="x", side="bottom")
        btn_favorito = tk.Button(frame_botones, text="⭐ Favorito", font=("Segoe UI", 9, "bold"), bg="#e6f6f5", fg="#00a79d", bd=1, relief="solid", padx=4, pady=8)
        btn_favorito.pack(side="left", fill="x", expand=True, padx=(0, 2))
        btn_seguimiento = tk.Button(
            frame_botones, 
            text="👁️ En Vivo", 
            font=("Segoe UI", 9, "bold"), 
            bg="#00a79d", 
            fg="white", 
            activebackground="#008c84", 
            activeforeground="white",
            bd=1, 
            relief="solid", 
            padx=4, 
            pady=8,
            cursor="hand2",
            command=self.mostrar_pantalla_seguimiento
        )
        btn_seguimiento.pack(side="left", fill="x", expand=True, padx=2)
        btn_cerrar = tk.Button(frame_botones, text="Cerrar", font=("Segoe UI", 9, "bold"), bg="#eeeeee", fg="#555555", bd=1, relief="solid", padx=4, pady=8, command=self.cerrar_panel)
        btn_cerrar.pack(side="right", fill="x", expand=True, padx=(2, 0))


    # LOGICA DE INTERACCION DEL PANEL
    def cerrar_panel(self):
        """Oculta la tarjeta de información y muestra el botón flotante."""
        self.panel_info.place_forget()
        self.btn_mostrar_panel.place(x=20, y=610, width=130, height=35)

    def abrir_panel(self):
        """Muestra la tarjeta de información de nuevo y oculta el botón flotante."""
        self.btn_mostrar_panel.place_forget()
        self.panel_info.place(x=0, y=460, width=400, height=220)

    # PANTALLA 3: SIN PARADAS EN ESTA ÁREA
    def mostrar_pantalla_sin_paradas(self):
        self.limpiar_pantalla()

        frame_vacio = tk.Frame(self.contenedor, bg="#ffffff", padx=30)
        frame_vacio.pack(fill="both", expand=True)
        spacer_top = tk.Frame(frame_vacio, bg="#ffffff", height=120)
        spacer_top.pack(fill="x")

        lbl_icono_mapa = tk.Label(
            frame_vacio, 
            text="🗺️", 
            font=("Segoe UI", 48), 
            bg="#f5f5f5", 
            fg="#00a79d",
            width=2,
            height=1,
            bd=1,
            relief="solid"
        )
        lbl_icono_mapa.pack(pady=20)
        lbl_alerta_titulo = tk.Label(
            frame_vacio, 
            text="Sin paradas en esta área", 
            font=("Segoe UI", 16, "bold"), 
            fg="#000000", 
            bg="#ffffff",
            wraplength=320
        )
        lbl_alerta_titulo.pack(pady=(10, 5))
        lbl_alerta_desc = tk.Label(
            frame_vacio, 
            text="No encontramos paradas activas en el área visible. Intenta ajustar el mapa o buscar en otra zona de Mexicali.", 
            font=("Segoe UI", 10), 
            fg="#666666", 
            bg="#ffffff",
            justify="center",
            wraplength=300
        )
        lbl_alerta_desc.pack(pady=(0, 40))

        btn_reajustar = tk.Button(
            frame_vacio,
            text="🔄 Ajustar mapa / área",
            font=("Segoe UI", 11, "bold"),
            bg="#ff7a1a",  
            fg="white",
            activebackground="#e0650d",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=12,
            cursor="hand2",
            command=lambda: self.mostrar_pantalla_mapa_con_coordenadas(
                32.6258, -115.3770, 15, 
                "PARADA: Av. Claridad (UPBC)", 
                "⏳ Próximo Autobús: Ruta Palaco - 10 min", 
                "🚌 Siguiente Unidad: Enlace Periférico - 25 min"
            )
        )
        btn_reajustar.pack(fill="x", pady=10)

        btn_cancelar = tk.Button(
            frame_vacio,
            text="Cancelar",
            font=("Segoe UI", 10, "bold"),
            bg="#eeeeee",
            fg="#555555",
            bd=0,
            cursor="hand2",
            command=self.mostrar_pantalla_mapa
        )
        btn_cancelar.pack(fill="x", pady=5)

    # PANTALLA 4: SEGUIMIENTO ACTIVO EN VIVO
    def mostrar_pantalla_seguimiento(self):
        self.limpiar_pantalla()
        frame_seguimiento = tk.Frame(self.contenedor, bg="#ffffff", padx=20, pady=15)
        frame_seguimiento.pack(fill="both", expand=True)

        frame_header = tk.Frame(frame_seguimiento, bg="#ffffff")
        frame_header.pack(fill="x", pady=(0, 15))

        btn_atras = tk.Button(frame_header, text="‹", font=("Segoe UI", 16, "bold"), bg="#eeeeee", fg="#333333", bd=0, width=2, height=1, cursor="hand2", command=self.mostrar_pantalla_mapa)
        btn_atras.pack(side="left", padx=(0, 10))

        frame_info_ruta = tk.Frame(frame_header, bg="#ffffff")
        frame_info_ruta.pack(side="left", fill="x", expand=True)

        frame_badge_linea = tk.Frame(frame_info_ruta, bg="#ffffff")
        frame_badge_linea.pack(anchor="w")
        
        lbl_badge = tk.Label(frame_badge_linea, text="Ruta X", font=("Segoe UI", 9, "bold"), bg="#ff7a1a", fg="white", padx=6, pady=2)
        lbl_badge.pack(side="left", padx=(0, 5))
        
        lbl_titulo_seg = tk.Label(frame_badge_linea, text="Seguimiento activo", font=("Segoe UI", 12, "bold"), fg="#000000", bg="#ffffff")
        lbl_titulo_seg.pack(side="left")

        lbl_trayecto = tk.Label(frame_info_ruta, text="XXXXXX -> XXXXXXXX", font=("Segoe UI", 9), fg="#666666", bg="#ffffff")
        lbl_trayecto.pack(anchor="w", pady=(2, 0))

        lbl_status_live = tk.Label(frame_header, text="● EN VIVO", font=("Segoe UI", 9, "bold"), fg="#00a79d", bg="#e6f6f5", padx=8, pady=4)
        lbl_status_live.pack(side="right")

        card_estimacion = tk.Frame(frame_seguimiento, bg="#f9f9f9", bd=1, relief="solid", padx=15, pady=15)
        card_estimacion.pack(fill="x", pady=(0, 20))

        lbl_llega_en = tk.Label(card_estimacion, text="Llega en", font=("Segoe UI", 10), fg="#666666", bg="#f9f9f9")
        lbl_llega_en.pack(anchor="w")

        frame_tiempo_grande = tk.Frame(card_estimacion, bg="#f9f9f9")
        frame_tiempo_grande.pack(fill="x", anchor="w")

        lbl_numero_min = tk.Label(frame_tiempo_grande, text="X", font=("Segoe UI", 36, "bold"), fg="#ff7a1a", bg="#f9f9f9")
        lbl_numero_min.pack(side="left")
        
        lbl_texto_min = tk.Label(frame_tiempo_grande, text="min", font=("Segoe UI", 14, "bold"), fg="#ff7a1a", bg="#f9f9f9")
        lbl_texto_min.pack(side="left", padx=5, pady=(15, 0))

        lbl_ubicacion_actual = tk.Label(card_estimacion, text="📍 XXXXXXXXXXXXXXXXX", font=("Segoe UI", 9, "bold"), fg="#333333", bg="#f9f9f9", justify="left", wraplength=220)
        lbl_ubicacion_actual.pack(anchor="w", pady=(5, 0))

        frame_telemetria = tk.Frame(card_estimacion, bg="#f9f9f9")
        frame_telemetria.place(x=230, y=10)
        tk.Label(frame_telemetria, text="⏱️ A tiempo", font=("Segoe UI", 8, "bold"), fg="#00a79d", bg="#e6f6f5", padx=4, pady=2).pack(pady=2, anchor="e")
        tk.Label(frame_telemetria, text="📡 XX km/h", font=("Segoe UI", 8), fg="#666666", bg="#eeeeee", padx=4, pady=2).pack(pady=2, anchor="e")

        tk.Label(frame_seguimiento, text="Recorrido de la ruta", font=("Segoe UI", 10, "bold"), fg="#666666", bg="#ffffff").pack(anchor="w", pady=(0, 10))

        frame_linea_tiempo = tk.Frame(frame_seguimiento, bg="#ffffff")
        frame_linea_tiempo.pack(fill="both", expand=True)

        paradas = [
            {"nombre": "XXXXXXXXXXX", "estado": "pasado"},
            {"nombre": "XXXXXXXXXXX", "estado": "pasado"},
            {"nombre": "XXXXXXXXXXX", "estado": "pasado"},
            {"nombre": "XXXXXXXXXXX", "estado": "actual"},
            {"nombre": "XXXXXXXXXXX", "estado": "siguiente"},
            {"nombre": "XXXXXXXXXXX", "estado": "siguiente"}
        ]

        for p in paradas:
            item_frame = tk.Frame(frame_linea_tiempo, bg="#ffffff")
            item_frame.pack(fill="x", pady=4)

            if p["estado"] == "pasado":
                lbl_icon = tk.Label(item_frame, text="✓", font=("Segoe UI", 10, "bold"), fg="#00a79d", bg="#e6f6f5", width=2, bd=1, relief="solid")
                lbl_name = tk.Label(item_frame, text=p["nombre"], font=("Segoe UI", 10), fg="#888888", bg="#ffffff")
            elif p["estado"] == "actual":
                lbl_icon = tk.Label(item_frame, text="🚌", font=("Segoe UI", 10), fg="white", bg="#ff7a1a", width=2, bd=1, relief="solid")

                lbl_name = tk.Label(item_frame, text=f"{p['nombre']}\n← Tu parada • xxxx min", font=("Segoe UI", 10, "bold"), fg="#ff7a1a", bg="#ffffff", justify="left")
            else:
                lbl_icon = tk.Label(item_frame, text="○", font=("Segoe UI", 10), fg="#bbbbbb", bg="#ffffff", width=2)
                lbl_name = tk.Label(item_frame, text=p["nombre"], font=("Segoe UI", 10), fg="#555555", bg="#ffffff")

            lbl_icon.pack(side="left", padx=(0, 10))
            lbl_name.pack(side="left", anchor="w")

        frame_alertas = tk.Frame(frame_seguimiento, bg="#fff4ec", bd=1, relief="solid", padx=12, pady=10)
        frame_alertas.pack(fill="x", side="bottom", pady=(10, 0))

        lbl_alerta_icon = tk.Label(frame_alertas, text="🔔 Alertas activadas — te avisamos al llegar", font=("Segoe UI", 9, "bold"), fg="#ff7a1a", bg="#fff4ec")
        lbl_alerta_icon.pack(side="left")

        self.alerta_activa = True
        self.btn_switch = tk.Button(frame_alertas, text="ON ", font=("Segoe UI", 8, "bold"), bg="#ff7a1a", fg="white", bd=0, width=5, cursor="hand2", command=self.alternar_switch_alerta)
        self.btn_switch.pack(side="right")

        lbl_nota_notif = tk.Label(frame_seguimiento, text="ⓘ Recibirás una notificación cuando el autobús esté a 2 minutos de tu parada.", font=("Segoe UI", 8), fg="#666666", bg="#ffffff", justify="left", wraplength=340)
        lbl_nota_notif.pack(fill="x", side="bottom", pady=(5, 0))

    def alternar_switch_alerta(self):
        """Cambia de estado el botón de alerta activada/desactivada en tiempo real."""
        if self.alerta_activa:
            self.btn_switch.config(text="OFF", bg="#cccccc", fg="#666666")
            self.alerta_activa = False
        else:
            self.btn_switch.config(text="ON ", bg="#ff7a1a", fg="white")
            self.alerta_activa = True

# Ejecución de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = BusMXLApp(root)
    root.mainloop()
