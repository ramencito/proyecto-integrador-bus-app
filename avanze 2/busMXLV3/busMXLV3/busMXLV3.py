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

        # 2. Bloque de Contenido / Textos
        frame_contenido = tk.Frame(self.contenedor, bg="#ffffff", padx=30, pady=40)
        frame_contenido.pack(fill="both", expand=True)

        lbl_titulo = tk.Label(frame_contenido, text="BusMXL", font=("Segoe UI", 36, "bold"), fg="#00a79d", bg="#ffffff")
        lbl_titulo.pack(pady=(10, 5))

        lbl_subtitulo = tk.Label(frame_contenido, text="¡Bienvenido!", font=("Segoe UI", 18, "bold"), fg="#000000", bg="#ffffff")
        lbl_subtitulo.pack(pady=(0, 40))

        btn_ingresar = tk.Button(
            frame_contenido, 
            text="INGRESAR A LA APLICACIÓN", 
            font=("Segoe UI", 11, "bold"), 
            bg="#00a79d", 
            fg="white", 
            activebackground="#008c84", 
            activeforeground="white",
            bd=1, 
            relief="solid",
            padx=10, 
            pady=12,
            cursor="hand2",
            command=self.mostrar_pantalla_mapa
        )
        btn_ingresar.pack(fill="x", side="bottom", pady=20)

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

    # LOGICA DE INTERACCION DEL PANEL
    def cerrar_panel(self):
        """Oculta la tarjeta de información y muestra el botón flotante."""
        self.panel_info.place_forget()
        self.btn_mostrar_panel.place(x=20, y=610, width=130, height=35)

    def abrir_panel(self):
        """Muestra la tarjeta de información de nuevo y oculta el botón flotante."""
        self.btn_mostrar_panel.place_forget()
        self.panel_info.place(x=0, y=460, width=400, height=220)

# Ejecución de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = BusMXLApp(root)
    root.mainloop()
