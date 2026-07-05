import tkinter as tk
import tkintermapview

ventana = tk.Tk()
ventana.title("Prueba de Mapa Mexicali")
ventana.geometry("500x700") 

mapa_widget = tkintermapview.TkinterMapView(ventana, width=500, height=700, corner_radius=0)
mapa_widget.pack(fill="both", expand=True)
mapa_widget.set_position(32.6278, -115.4545)
mapa_widget.set_zoom(13)
marcador = mapa_widget.set_marker(32.6275, -115.4442, text="Parada UABC - Línea 9")

ventana.mainloop()
