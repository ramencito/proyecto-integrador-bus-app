import os
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
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.ruta_imagen = os.path.join(self.base_dir, 'fondo.jpg')

        self.contenedor = tk.Frame(self.root, bg="#ffffff")
        self.contenedor.pack(fill="both", expand=True)

        self.mostrar_pantalla_bienvenida()

    def limpiar_pantalla(self):
        """Elimina todos los widgets activos en el contenedor."""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    # PANTALLA 1
    def mostrar_pantalla_bienvenida(self):
        self.limpiar_pantalla()

        color_upbc_morado = "#6A1B9A"
        self.contenedor.configure(bg=color_upbc_morado)

        if os.path.exists(self.ruta_imagen):

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

        frame_contenido = tk.Frame(self.contenedor, bg="#ffffff", padx=30, pady=25)
        frame_contenido.pack(fill="both", expand=True, side="bottom")

        lbl_titulo = tk.Label(frame_contenido, text="UPBC-BUS", font=("Segoe UI", 36, "bold"), fg=color_upbc_morado, bg="#ffffff")
        lbl_titulo.pack(pady=(5, 2))

        lbl_subtitulo = tk.Label(frame_contenido, text="Selecciona tu horario de clases:", font=("Segoe UI", 12, "bold"), fg="#555555", bg="#ffffff")
        lbl_subtitulo.pack(pady=(0, 20))

        # Botónes
        btn_matutino = tk.Button(
            frame_contenido, 
            text="Turno Matutino", 
            font=("Segoe UI", 12, "bold"), 
            bg=color_upbc_morado, 
            fg="white", 
            activebackground="#4A148C", 
            activeforeground="white",
            bd=0, 
            padx=10, 
            pady=12,
            cursor="hand2",
            command=self.mostrar_pantalla_mapa
        )
        btn_matutino.pack(fill="x", pady=8)

        btn_vespertino = tk.Button(
            frame_contenido, 
            text="Turno Vespertino", 
            font=("Segoe UI", 12, "bold"), 
            bg="#eeeeee", 
            fg="#555555", 
            activebackground="#cccccc", 
            activeforeground="#333333",
            bd=1, 
            relief="solid",
            padx=10, 
            pady=12,
            cursor="hand2",
            command=self.mostrar_pantalla_mapa
        )
        btn_vespertino.pack(fill="x", pady=8)

    # PANTALLA 2 MAPA
    def mostrar_pantalla_mapa(self):
        self.limpiar_pantalla()

        self.mapa = tkintermapview.TkinterMapView(self.contenedor, corner_radius=0)
        self.mapa.place(x=0, y=0, width=400, height=680)
        
        self.mapa.set_position(32.6258, -115.3770)
        self.mapa.set_zoom(15)
        self.mapa.set_marker(32.6258, -115.3770, text="Campus UPBC")

        # Menú Inferior
        self.panel_info = tk.Frame(self.contenedor, bg="#ffffff", bd=1, relief="solid", padx=15, pady=12)
        self.panel_info.place(x=0, y=490, width=400, height=190)

        handle = tk.Frame(self.panel_info, bg="#cccccc", width=40, height=4)
        handle.pack(pady=(0, 10))

        lbl_seccion = tk.Label(self.panel_info, text="Selecciona una Ruta de Transporte:", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#666666")
        lbl_seccion.pack(anchor="w", pady=(0, 10))

        frame_opciones_camion = tk.Frame(self.panel_info, bg="#ffffff")
        frame_opciones_camion.pack(fill="x", pady=5)

        #botones
        self.btn_amilpa = tk.Button(
            frame_opciones_camion,
            text="🚌 Ruta Amilpa\n(Próximo a llegar)",
            font=("Segoe UI", 10, "bold"),
            bg="#6A1B9A",
            fg="white",
            activebackground="#4A148C",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=10,
            cursor="hand2",
            command=None  
        )
        self.btn_amilpa.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_violeta = tk.Button(
            frame_opciones_camion,
            text="🚌 Ruta Violeta\n(En tránsito)",
            font=("Segoe UI", 10, "bold"),
            bg="#D4AF37", 
            fg="white",
            activebackground="#B89728",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=10,
            cursor="hand2",
            command=None  
        )
        self.btn_violeta.pack(side="right", fill="x", expand=True, padx=(6, 0))

        btn_regresar_inicio = tk.Button(
            self.panel_info,
            text="← Cambiar de Turno / Horario",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#999999",
            bd=0,
            cursor="hand2",
            command=self.mostrar_pantalla_bienvenida
        )
        btn_regresar_inicio.pack(side="bottom", pady=(5, 0))

# Disparador del bucle gráfico
if __name__ == "__main__":
    root = tk.Tk()
    app = BusMXLApp(root)
    root.mainloop()