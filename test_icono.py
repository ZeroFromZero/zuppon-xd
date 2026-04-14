import urllib.request, json

data = json.dumps({'categoria': 'Educación', 'img_url': 'https://img.icons8.com/color/64/graduation-cap.png', 'color': '#8e44ad'}).encode()
req = urllib.request.Request('http://127.0.0.1:5000/admin/icono-categoria', data=data, method='PUT')
req.add_header('Content-Type', 'application/json')
try:
    resp = urllib.request.urlopen(req, timeout=5)
    print('Respuesta:', resp.read().decode())
except Exception as e:
    print('Error:', e)

# Verificar en DB
import sqlite3
conn = sqlite3.connect('negocios.db')
c = conn.cursor()
c.execute("SELECT * FROM config_iconos")
rows = c.fetchall()
print('config_iconos:', rows)
conn.close()
