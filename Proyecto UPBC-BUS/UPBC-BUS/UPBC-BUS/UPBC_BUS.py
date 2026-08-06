import os
import json
import pyodbc  
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 
from PIL import Image, ImageTk
import tkintermapview

#Clase principal aplicacion
class BusMXLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UPBC-BUS")
        self.root.geometry("400x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        #Llamando imagen de fondo
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.ruta_imagen = os.path.join(self.base_dir, 'fondo.jpg')

        # Conexion a SQL
        self.server_sql = r'SILVER_NEO\SQLEXPRESS'
        self.database_sql = 'UPBC_Bus_DB'

        # Almacen marcador y linea de trayecto con animaciones
        self.marcador_autobus = None
        self.dibujo_trayecto = None
        
        self.coordenadas_animacion = []
        self.indice_micro_paso = 0
        self.job_animacion = None  
        self.intervalo_milisegundos = 250
        self.hora_objetivo_actual = None

        self.contenedor = tk.Frame(self.root, bg="#ffffff")
        self.contenedor.pack(fill="both", expand=True)

        self.mostrar_pantalla_bienvenida()

    def conectar_base_datos(self):
        """Abre un canal de datos seguro hacia SQL Server Management Studio."""
        try:
            conexion_str = (
                f"Driver={{ODBC Driver 17 for SQL Server}};"
                f"Server={self.server_sql};"
                f"Database={self.database_sql};"
                f"Trusted_Connection=yes;"
            )
            return pyodbc.connect(conexion_str)
        except Exception as e:
            print(f"⚠️ Error crítico de conexión a SQL Server: {e}")
            return None

    def limpiar_pantalla(self):
        """Detiene de forma segura cualquier animación activa antes de limpiar."""
        if self.job_animacion:
            self.root.after_cancel(self.job_animacion)
            self.job_animacion = None
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    #Interfaz de registro
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

        #Tarjeta inferior a datos
        frame_contenido = tk.Frame(self.contenedor, bg="#ffffff", padx=35, pady=20)
        frame_contenido.pack(fill="both", expand=True, side="bottom")

        lbl_titulo = tk.Label(frame_contenido, text="UPBC-BUS", font=("Segoe UI", 28, "bold"), fg=color_upbc_morado, bg="#ffffff")
        lbl_titulo.pack(pady=(0, 2))

        lbl_subtitulo = tk.Label(frame_contenido, text="Registro de Acceso Institucional", font=("Segoe UI", 11, "bold"), fg="#666666", bg="#ffffff")
        lbl_subtitulo.pack(pady=(0, 15))

        #Caja para nomre
        lbl_nombre = tk.Label(frame_contenido, text="Nombre Completo:", font=("Segoe UI", 10, "bold"), fg="#444444", bg="#ffffff")
        lbl_nombre.pack(anchor="w")
        self.txt_nombre = tk.Entry(frame_contenido, font=("Segoe UI", 11), bd=1, relief="solid")
        self.txt_nombre.pack(fill="x", pady=(2, 12), ipady=4)

        # Caja para matricula
        lbl_matricula = tk.Label(frame_contenido, text="Matrícula Universitaria:", font=("Segoe UI", 10, "bold"), fg="#444444", bg="#ffffff")
        lbl_matricula.pack(anchor="w")
        self.txt_matricula = tk.Entry(frame_contenido, font=("Segoe UI", 11), bd=1, relief="solid")
        self.txt_matricula.pack(fill="x", pady=(2, 20), ipady=4)

        # Botón de ingreso
        btn_ingresar = tk.Button(
            frame_contenido, text="Registrar e Ingresar", font=("Segoe UI", 12, "bold"), 
            bg=color_upbc_morado, fg="white", activebackground="#4A148C", activeforeground="white",
            bd=0, cursor="hand2", command=self.registrar_alumno_sql
        )
        btn_ingresar.pack(fill="x", ipady=6)

    def registrar_alumno_sql(self):
        """Valida las cajas de texto e inserta una fila en la tabla Alumnos_Registro."""
        nombre = self.txt_nombre.get().strip()
        matricula = self.txt_matricula.get().strip()

        #En caso de caja vacia
        if not nombre or not matricula:
            messagebox.showwarning("Campos Incompletos", "Por favor, escribe tu nombre y matrícula antes de ingresar.")
            return

        # Conexion a SQL
        conexion = self.conectar_base_datos()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO Alumnos_Registro (matricula, nombre_alumno) VALUES (?, ?)",
                    (matricula, nombre)
                )
                conexion.commit() # commit de guardado
                cursor.close()
                conexion.close()
                
                #Llevar a la siguiente pantalla
                self.mostrar_pantalla_mapa()
            except Exception as e:
                messagebox.showerror("Error SQL", f"No se pudo guardar el registro en SSMS: {e}")
        else:
            messagebox.showerror("Error de Servidor", "No hay conexión activa con SILVER_NEO\SQLEXPRESS")

    #Interfaz de Mapa
    def mostrar_pantalla_mapa(self):
        self.limpiar_pantalla()

        #Funcionabilidad del mapa
        self.mapa = tkintermapview.TkinterMapView(self.contenedor, corner_radius=0)
        self.mapa.place(x=0, y=0, width=400, height=680)
        self.mapa.set_position(32.6258, -115.3770)
        self.mapa.set_zoom(14)
        self.mapa.set_marker(32.6258, -115.3770, text="Campus UPBC")

        #Caja de otras unidades
        self.panel_info = tk.Frame(self.contenedor, bg="#ffffff", bd=1, relief="solid", padx=15, pady=10)
        self.panel_info.place(x=0, y=440, width=400, height=240)

        handle = tk.Frame(self.panel_info, bg="#cccccc", width=40, height=4)
        handle.pack(pady=(0, 5))

        self.lbl_seccion_titulo = tk.Label(self.panel_info, text="Rutas del día disponibles:", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#666666")
        self.lbl_seccion_titulo.pack(anchor="w", pady=1)

        self.lbl_tiempo_real = tk.Label(self.panel_info, text="Selecciona una ruta abajo para ver su estado...", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#ff7a1a")
        self.lbl_tiempo_real.pack(anchor="w", pady=1)

        #Menu inferior de otras unidades scrolleable
        tk.Label(self.panel_info, text="🗂️ Horarios del día (Haz clic para monitorear):", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#999999").pack(anchor="w", pady=(4, 0))
        
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

        #Botones de rutas
        frame_opciones_camion = tk.Frame(self.panel_info, bg="#ffffff")
        frame_opciones_camion.pack(fill="x", pady=(5, 2))

        self.btn_amilpa = tk.Button(
            frame_opciones_camion, text="🚌 Ruta Amilpa", font=("Segoe UI", 10, "bold"),
            bg="#6A1B9A", fg="white", activebackground="#4A148C", activeforeground="white",
            bd=0, padx=10, pady=8, cursor="hand2", command=lambda: self.consultar_tiempo_real_ruta("amilpa")
        )
        self.btn_amilpa.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_violeta = tk.Button(
            frame_opciones_camion, text="🚌 Ruta Violeta", font=("Segoe UI", 10, "bold"),
            bg="#D4AF37", fg="white", activebackground="#B89728", activeforeground="white",
            bd=0, padx=10, pady=8, cursor="hand2", command=lambda: self.consultar_tiempo_real_ruta("violeta")
        )
        self.btn_violeta.pack(side="right", fill="x", expand=True, padx=(6, 0))

        btn_regresar_inicio = tk.Button(
            self.panel_info, text="← Cerrar Sesión / Salir", font=("Segoe UI", 9, "bold"),
            bg="#ffffff", fg="#999999", bd=0, cursor="hand2", command=self.mostrar_pantalla_bienvenida
        )
        btn_regresar_inicio.pack(side="bottom", pady=(2, 0))
    
        #Llamando consultas en tiempo real
    def consultar_tiempo_real_ruta(self, clave_ruta, horario_forzado=None):
        """Extrae TODOS los horarios de SQL Server eliminando el filtro de turno."""
        if self.job_animacion:
            self.root.after_cancel(self.job_animacion)
            self.job_animacion = None

        conexion = self.conectar_base_datos()
        if not conexion:
            self.lbl_tiempo_real.config(text="❌ Error de conexión al servidor SQL", fg="#d32f2f")
            return

        cursor = conexion.cursor()
        info_ruta = {}
        horarios_turno = []
        puntos_reales_calle = []

        try:
            #Traer datos de ruta seleccionada
            cursor.execute("SELECT id_ruta, nombre_completo, trayecto FROM Rutas WHERE nombre_corto = ?", (clave_ruta,))
            fila_ruta = cursor.fetchone()
            if not fila_ruta:
                conexion.close()
                return
            
            id_ruta_sql = fila_ruta[0]
            info_ruta["nombre_completo"] = fila_ruta[1]
            info_ruta["trayecto"] = fila_ruta[2]

            cursor.execute(
                "SELECT hora_llegada FROM Horarios_Ruta WHERE id_ruta = ? ORDER BY hora_llegada ASC",
                (id_ruta_sql,)
            )
            horarios_turno = [fila[0] for fila in cursor.fetchall()]

            cursor.execute(
                "SELECT latitud, longitud FROM Coordenadas_Ruta WHERE id_ruta = ? ORDER BY secuencia ASC",
                (id_ruta_sql,)
            )
            puntos_reales_calle = [(float(fila[0]), float(fila[1])) for fila in cursor.fetchall()]

        except Exception as e:
            print(f"❌ Error al consultar SSMS: {e}")
        finally:
            cursor.close()
            conexion.close()

        #Proceso con el horario del sistema
        ahora = datetime.now()
        hora_actual_str = ahora.strftime("%H:%M")
        
        proximo_horario = horario_forzado
        unidades_futuras = []

        if not proximo_horario:
            for h in horarios_turno:
                if h > hora_actual_str:
                    if not proximo_horario: proximo_horario = h
                    else: unidades_futuras.append(h)
        else:
            for h in horarios_turno:
                if h > hora_actual_str and h != proximo_horario:
                    unidades_futuras.append(h)

        if self.marcador_autobus: self.marcador_autobus.delete()
        if self.dibujo_trayecto: self.dibujo_trayecto.delete()
        for widget in self.frame_lista_horarios.winfo_children(): widget.destroy()

        if proximo_horario and puntos_reales_calle:
            fmt = "%H:%M"
            diferencia = datetime.strptime(proximo_horario, fmt) - datetime.strptime(hora_actual_str, fmt)
            minutos_faltantes = int(diferencia.total_seconds() / 60)
            if minutos_faltantes <= 0: minutos_faltantes = 1  

            self.lbl_seccion_titulo.config(text=f"📍 {info_ruta['nombre_completo']}")
            self.lbl_tiempo_real.config(text=f"⏱️ Arribo a UPBC: {proximo_horario} (Faltan {minutos_faltantes} min)", fg="#ff7a1a")

            #Ciclo de unidades
            if not unidades_futuras:
                tk.Label(self.frame_lista_horarios, text=" No hay más unidades próximas", font=("Segoe UI", 9, "italic"), bg="#f9f9f9", fg="#777777").pack(padx=10, pady=5)
            for uf in unidades_futuras[:5]:
                btn_uf = tk.Button(
                    self.frame_lista_horarios, text=f" 🚌 Unidad: {uf} ", font=("Segoe UI", 9, "bold"),
                    bg="#eeeeee", fg="#444444", bd=1, relief="solid", padx=5, pady=2, cursor="hand2",
                    command=lambda h_clic=uf: self.consultar_tiempo_real_ruta(clave_ruta, horario_forzado=h_clic)
                )
                btn_uf.pack(side="left", padx=4, pady=5)

            #Linea de ruta en mapa
            color_linea = "#6A1B9A" if clave_ruta == "amilpa" else "#D4AF37"
            self.dibujo_trayecto = self.mapa.set_path(puntos_reales_calle, color=color_linea, width=4)

            #Pasos que sigue en tiks
            self.coordenadas_animacion = []
            densidad_pasos = 4  
            for i in range(len(puntos_reales_calle) - 1):
                lat_i, lng_i = puntos_reales_calle[i]
                lat_f, lng_f = puntos_reales_calle[i+1]
                for j in range(densidad_pasos):
                    fraction = j / densidad_pasos
                    inter_lat = lat_i + (lat_f - lat_i) * fraction
                    inter_lng = lng_i + (lng_f - lng_i) * fraction
                    self.coordenadas_animacion.append((inter_lat, inter_lng))
            
            #Tomar horario del sistemma para calculo con tiempo restante
            self.hora_objetivo_actual = proximo_horario  
            segundos_reales = minutos_faltantes * 60 
            milisegundos_totales = segundos_reales * 1000
            total_micro_pasos = len(self.coordenadas_animacion)
            
            self.intervalo_milisegundos = int(milisegundos_totales / total_micro_pasos)
            self.intervalo_milisegundos = max(200, self.intervalo_milisegundos)

            self.indice_micro_paso = 0
            if len(self.coordenadas_animacion) > 0:
                lat_init, lng_init = self.coordenadas_animacion[0]
                self.marcador_autobus = self.mapa.set_marker(lat_init, lng_init, text=f"🚍 {clave_ruta.upper()}")
                self.mapa.set_position(lat_init, lng_init)

            self.animar_movimiento_autobus()
        else:
            self.lbl_seccion_titulo.config(text=f"📍 {info_ruta.get('nombre_completo', 'Autobús')}")
            self.lbl_tiempo_real.config(text="❌ No hay más corridas programadas para el día de hoy.", fg="#d32f2f")
            tk.Label(self.frame_lista_horarios, text=" Trayectos concluidos por hoy", font=("Segoe UI", 9, "italic"), bg="#f9f9f9", fg="#777777").pack(padx=10, pady=5)
            self.mapa.set_position(32.6258, -115.3770)

    #Animacion de movimiento acorde al sistema anterior
    def animar_movimiento_autobus(self):
        """Mueve el autobús de forma fluida y recalcula la cuenta regresiva en cada micro-paso."""
        if self.indice_micro_paso >= len(self.coordenadas_animacion):
            self.lbl_tiempo_real.config(text="🏁 ¡El autobús ha llegado al Campus UPBC!", fg="#00a79d")
            return

        lat, lng = self.coordenadas_animacion[self.indice_micro_paso]
        self.marcador_autobus.set_position(lat, lng)

        ahora = datetime.now()
        hora_actual_str = ahora.strftime("%H:%M")
        
        try:
            fmt = "%H:%M"
            diferencia = datetime.strptime(self.hora_objetivo_actual, fmt) - datetime.strptime(hora_actual_str, fmt)
            minutos_faltantes = int(diferencia.total_seconds() / 60)
            
            if minutos_faltantes > 0:
                self.lbl_tiempo_real.config(
                    text=f"⏱️ Arribo a UPBC: {self.hora_objetivo_actual} (Faltan {minutos_faltantes} min)", 
                    fg="#ff7a1a"
                )
            else:
                self.lbl_tiempo_real.config(text="⏱️ El autobús está por arribar al Campus UPBC", fg="#ff7a1a")
        except Exception:
            pass

        self.indice_micro_paso += 1
        self.job_animacion = self.root.after(self.intervalo_milisegundos, self.animar_movimiento_autobus)

#Ciclo principal de la aplicacion
if __name__ == "__main__":
    root = tk.Tk()
    app = BusMXLApp(root)
    root.mainloop()