import os
import threading
from flask import Flask, send_from_directory
import webview

# 1. CREAMOS EL SERVIDOR WEB LOCAL INVISIBLE
server = Flask(__name__)

# Permitir que el servidor busque las imágenes en tu carpeta actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
@server.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(BASE_DIR, filename)


# ==========================================
# PANTALLA 1: BIENVENIDA / INGRESO
# ==========================================
@server.route('/')
def pantalla_bienvenida():
    html_bienvenida = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BusMXL - Bienvenido</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            body { background-color: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
            .phone-container { width: 100%; max-width: 400px; height: 680px; background-color: #ffffff; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; position: relative; display: flex; flex-direction: column; justify-content: space-between; align-items: center; }
            .top-image { width: 100%; height: 220px; position: relative; background-image: url('/assets/fondo.jpg'); background-size: cover; background-position: center; }
            .fade-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(255,255,255,0) 30%, rgba(255,255,255,1) 100%); }
            .content-wrapper { padding: 0 30px 45px 30px; width: 100%; z-index: 2; flex-grow: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; }
            .header-block { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; width: 100%; margin-bottom: 45px; }
            .main-title { color: #00a79d; font-weight: 700; margin-bottom: 20px; font-size: 40px; letter-spacing: 0.5px; width: 100%; text-align: center; }
            .welcome-text { font-weight: 700; color: #000000; letter-spacing: 0.5px; margin-bottom: 35px; font-size: 22px; }
            .btn-ingresar { background-color: #00a79d; color: white; width: 100%; border: 1.5px solid #000000; border-radius: 25px; padding: 14px; font-weight: 700; font-size: 14px; letter-spacing: 0.5px; cursor: pointer; text-transform: uppercase; transition: background 0.2s; text-decoration: none; text-align: center; display: block; }
            .btn-ingresar:hover { background-color: #008c84; }
        </style>
    </head>
    <body>
        <div class="phone-container">
            <div class="top-image">
                <div class="fade-overlay"></div>
            </div>
            <div class="content-wrapper">
                <div class="header-block">
                    <h2 class="main-title">BusMXL</h2>
                    <svg width="75" height="75" viewBox="0 0 24 24" fill="#00a79d" style="display: block; margin: 0 auto;">
                        <path d="M4 16c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h10v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1c.55 0 1-.45 1-1V6c0-3.5-3.58-4-8-4s-8 .5-8 4v9c0 .55.45 1 1 1v1zm2-10c0-.55.45-1 1-1h10c.55 0 1 .45 1 1v3H6V6zm2.5 8c-.83 0-1.5-.67-1.5-1.5S7.67 11 8.5 11s1.5 0.67 1.5 1.5S9.33 14 8.5 14zm7 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5 0.67 1.5 1.5-0.67 1.5-1.5 1.5zM5 20c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1H5v1zm11-1v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h-3z"/>
                    </svg>
                </div>
                <h4 class="welcome-text">¡Bienvenido!</h4>
                <a href="/mapa" class="btn-ingresar">Ingresar a la aplicación</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_bienvenida


# ==========================================
# PANTALLA 2: MAPA INTERACTIVO PRINCIPAL
# ==========================================
@server.route('/mapa')
def pantalla_mapa():
    html_mapa = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BusMXL - Monitoreo</title>
        <link rel="stylesheet" href="https://unpkg.com" />
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            body { background-color: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
            .phone-container { width: 100%; max-width: 400px; height: 680px; background-color: #ffffff; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; position: relative; display: flex; flex-direction: column; justify-content: space-between; }
            #map { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; background-color: #e5e5e5; }
            .search-box-wrapper { position: relative; z-index: 10; padding: 15px 12px; width: 100%; }
            .search-box { display: flex; align-items: center; background-color: #ffffff; border-radius: 10px; padding: 0 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border: 1px solid #e0e0e0; height: 50px; }
            .search-icon { margin-right: 10px; font-size: 16px; }
            .search-input { border: none; outline: none; width: 100%; font-size: 14px; color: #333; background: transparent; }
            .info-panel { position: relative; z-index: 10; background-color: #ffffff; border-radius: 24px 24px 0 0; padding: 25px 20px; box-shadow: 0 -5px 20px rgba(0,0,0,0.1); width: 100%; transition: transform 0.3s ease-in-out; }
            .info-panel.oculto { transform: translateY(105%); position: absolute; bottom: 0; }
            .panel-handle { width: 40px; height: 4px; background-color: #ccc; border-radius: 2px; margin: 0 auto 15px auto; }
            .panel-title { font-weight: 700; color: #000000; font-size: 16px; margin-bottom: 15px; }
            .info-list { margin-bottom: 20px; }
            .info-item { display: flex; align-items: center; margin-bottom: 10px; font-size: 14px; color: #333333; }
            .info-item-icon { margin-right: 10px; font-size: 16px; width: 20px; text-align: center; }
            .btn-group { display: flex; gap: 10px; }
            .btn-action { flex: 1; border: none; padding: 12px; font-size: 13px; font-weight: 700; border-radius: 10px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
            .btn-favorites { background-color: #e6f6f5; color: #00a79d; border: 1px solid #00a79d; }
            .btn-close { background-color: #eeeeee; color: #555555; border: 1px solid #cccccc; }
            .btn-flotante { position: absolute; bottom: 20px; left: 15px; z-index: 9; background-color: #00a79d; color: white; border: none; padding: 10px 15px; font-size: 12px; font-weight: bold; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); cursor: pointer; display: none; }
        </style>
    </head>
    <body>
        <div class="phone-container">
            <div id="map"></div>
            <div class="search-box-wrapper">
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="search-input" placeholder="Buscar ruta o parada... (Ej. UABC, Novena)">
                </div>
            </div>
            <button class="btn-flotante" id="btnMostrar" onclick="alternarPanel(true)">📋 Mostrar Info</button>
            <div class="info-panel" id="miPanel">
                <div class="panel-handle"></div>
                <h5 class="panel-title">PARADA: Frente a UABC</h5>
                <div class="info-list">
                    <div class="info-item"><span class="info-item-icon">⏳</span><span><strong>Próximo Autobús:</strong> Ruta 9 - 7 min</span></div>
                    <div class="info-item"><span class="info-item-icon">🚌</span><span><strong>Siguiente Unidad:</strong> Ruta 9 - 22 min</span></div>
                    <div class="info-item"><span class="info-item-icon">☀️</span><span><strong>Clima Actual:</strong> 43°C</span></div>
                </div>
                <div class="btn-group">
                    <button class="btn-action btn-favorites">⭐ Guardar en Favoritos</button>
                    <button class="btn-action btn-close" onclick="alternarPanel(false)">❌ Cerrar Panel</button>
                </div>
            </div>
        </div>
        <script src="https://unpkg.com"></script>
        <script>
            const map = L.map('map', { zoomControl: false }).setView([32.6245, -115.4410], 14);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap'
            }).addTo(map);
            L.marker([32.6245, -115.4410]).addTo(map).bindPopup("<b>Autobús Ruta 9</b><br>En camino a la parada.").openPopup();
            window.addEventListener('load', () => {
                setTimeout(() => { map.invalidateSize(); }, 300);
            });
            function alternarPanel(mostrar) {
                const panel = document.getElementById('miPanel');
                const btn = document.getElementById('btnMostrar');
                if (mostrar) {
                    panel.classList.remove('oculto');
                    btn.style.display = 'none';
                } else {
                    panel.classList.add('oculto');
                    btn.style.display = 'block';
                }
                setTimeout(() => { map.invalidateSize(); }, 350);
            }
        </script>
    </body>
    </html>
    """
    return html_mapa
def run_server():
    server.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    webview.create_window('BusMXL - Aplicación de Monitoreo', url='http://127.0.0.1:5000', width=450, height=750, resizable=False)
    webview.start()