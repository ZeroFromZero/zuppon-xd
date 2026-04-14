from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
from datetime import datetime, timedelta
import json, secrets, io, base64, re
import urllib.request
import qrcode
from database import init_db, get_connection, insertar_negocios_ejemplo, hash_password, verify_password, generate_credentials

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_fortissima'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value) if isinstance(value, str) else value
    except:
        return []

init_db()
insertar_negocios_ejemplo()

def dict_from_row(row):
    d = dict(zip(row.keys(), row))
    for campo in ('servicios', 'fotos'):
        if campo in d and d[campo]:
            try:
                d[campo] = json.loads(d[campo]) if isinstance(d[campo], str) else d[campo]
            except:
                d[campo] = []
    return d

# ── PÁGINAS ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/negocio/<int:negocio_id>')
def detalle_negocio(negocio_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM negocios WHERE id = ?', (negocio_id,))
    negocio = c.fetchone()
    # Registrar visita solo si no visitó en los últimos 30 min (evita contar recargas)
    if negocio:
        cookie_key = f'visited_{negocio_id}'
        if not request.cookies.get(cookie_key):
            c.execute('INSERT INTO visitas (negocio_id) VALUES (?)', (negocio_id,))
            conn.commit()
    conn.close()
    if negocio:
        resp = make_response(render_template('detalle.html', negocio=dict_from_row(negocio)))
        if not request.cookies.get(f'visited_{negocio_id}'):
            resp.set_cookie(f'visited_{negocio_id}', '1', max_age=1800)  # 30 min
        return resp
    return "Negocio no encontrado", 404

@app.route('/negocio/panel')
def negocio_panel():
    if 'negocio_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM negocios WHERE id = ?', (session['negocio_id'],))
    negocio = c.fetchone()
    conn.close()
    if negocio:
        return render_template('negocio_panel.html', negocio=dict_from_row(negocio))
    return redirect(url_for('login'))

# ── API PÚBLICA ───────────────────────────────────────────────────────────────

@app.route('/api/negocios')
def get_negocios():
    categoria = request.args.get('categoria', 'todos')
    orden = request.args.get('orden', 'rating')
    conn = get_connection()
    c = conn.cursor()
    query = 'SELECT * FROM negocios'
    params = []
    if categoria != 'todos':
        query += ' WHERE categoria = ?'
        params.append(categoria)
    if orden == 'rating':
        query += ' ORDER BY rating DESC'
    elif orden == 'reviews':
        query += ' ORDER BY reviews DESC'
    else:
        query += ' ORDER BY id DESC'
    c.execute(query, params)
    negocios = [dict_from_row(row) for row in c.fetchall()]
    conn.close()
    return jsonify(negocios)

@app.route('/api/negocio/<int:negocio_id>')
def get_negocio(negocio_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM negocios WHERE id = ?', (negocio_id,))
    negocio = c.fetchone()
    conn.close()
    if negocio:
        return jsonify(dict_from_row(negocio))
    return jsonify({'error': 'No encontrado'}), 404

@app.route('/api/ofertas_home')
def get_ofertas_home():
    categoria = request.args.get('categoria', 'todos')
    orden = request.args.get('orden', 'descuento')
    ciudad = request.args.get('ciudad', 'todas')
    conn = get_connection()
    c = conn.cursor()
    query = '''
        SELECT o.*, n.nombre as negocio_nombre, n.categoria, n.whatsapp, n.telefono,
               n.imagen as negocio_imagen
        FROM ofertas o JOIN negocios n ON o.negocio_id = n.id
    '''
    params = []
    conditions = []
    if categoria != 'todos':
        conditions.append('n.categoria = ?')
        params.append(categoria)
    if ciudad != 'todas':
        conditions.append('n.ciudad = ?')
        params.append(ciudad)
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    # Excluir ofertas expiradas
    expiry_clause = "(o.fecha_vencimiento IS NULL OR o.fecha_vencimiento > datetime('now'))"
    query += (' AND ' if conditions else ' WHERE ') + expiry_clause
    query += ' ORDER BY o.id DESC' if orden == 'reciente' else ' ORDER BY o.orden, o.id'
    c.execute(query, params)
    ofertas = [dict_from_row(row) for row in c.fetchall()]
    conn.close()
    return jsonify(ofertas)

@app.route('/api/ofertas/<int:negocio_id>')
def get_ofertas(negocio_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM ofertas WHERE negocio_id = ? ORDER BY orden, id', (negocio_id,))
    ofertas = [dict_from_row(row) for row in c.fetchall()]
    conn.close()
    return jsonify(ofertas)

@app.route('/api/valoraciones/<int:negocio_id>')
def get_valoraciones(negocio_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM valoraciones WHERE negocio_id = ? ORDER BY fecha DESC', (negocio_id,))
    valoraciones = [dict_from_row(row) for row in c.fetchall()]
    conn.close()
    return jsonify(valoraciones)

@app.route('/api/valoracion', methods=['POST'])
def add_valoracion():
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO valoraciones (negocio_id, nombre, rating, comentario) VALUES (?, ?, ?, ?)',
              (data['negocio_id'], data['nombre'], int(data['rating']), data['comentario']))
    vid = c.lastrowid
    c.execute('SELECT AVG(rating) as p, COUNT(*) as t FROM valoraciones WHERE negocio_id = ?', (data['negocio_id'],))
    r = c.fetchone()
    c.execute('UPDATE negocios SET rating=?, reviews=? WHERE id=?', (round(r['p'], 1), r['t'], data['negocio_id']))
    conn.commit()
    c.execute('SELECT * FROM valoraciones WHERE id = ?', (vid,))
    val = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'valoracion': val})

# ── API LOGIN ─────────────────────────────────────────────────────────────────

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM negocios WHERE usuario = ?', (data.get('usuario', ''),))
    negocio = c.fetchone()
    conn.close()
    if negocio and verify_password(data.get('contrasena', ''), negocio['contrasena']):
        session['negocio_id'] = negocio['id']
        session['negocio_nombre'] = negocio['nombre']
        return jsonify({'success': True, 'negocio_id': negocio['id']})
    return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401

@app.route('/api/negocio/cambiar-contrasena', methods=['POST'])
def cambiar_contrasena():
    if 'negocio_id' not in session:
        return jsonify({'success': False, 'message': 'No autenticado'}), 401
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM negocios WHERE id = ?', (session['negocio_id'],))
    negocio = c.fetchone()
    if not verify_password(data.get('contrasena_actual', ''), negocio['contrasena']):
        conn.close()
        return jsonify({'success': False, 'message': 'Contraseña actual incorrecta'}), 401
    c.execute('UPDATE negocios SET contrasena=? WHERE id=?', (hash_password(data['contrasena_nueva']), session['negocio_id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Contraseña actualizada'})

# ── ADMIN ─────────────────────────────────────────────────────────────────────

@app.route('/admin/negocios', methods=['GET'])
def admin_get_negocios():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT n.*,
            COUNT(o.id) as total_ofertas,
            SUM(CASE WHEN o.fecha_vencimiento > datetime('now') THEN 1 ELSE 0 END) as ofertas_activas
        FROM negocios n
        LEFT JOIN ofertas o ON o.negocio_id = n.id
        GROUP BY n.id
        ORDER BY n.id DESC
    ''')
    negocios = [dict_from_row(row) for row in c.fetchall()]
    conn.close()
    return jsonify(negocios)

# ── CIUDADES ──────────────────────────────────────────────────────────────────

@app.route('/api/ciudades')
def get_ciudades():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM ciudades ORDER BY nombre')
    ciudades = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(ciudades)

@app.route('/admin/ciudad', methods=['POST'])
def admin_add_ciudad():
    data = request.json
    nombre = (data.get('nombre') or '').strip()
    if not nombre:
        return jsonify({'success': False, 'message': 'Nombre requerido'}), 400
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO ciudades (nombre) VALUES (?)', (nombre,))
        conn.commit()
        ciudad_id = c.lastrowid
        conn.close()
        return jsonify({'success': True, 'ciudad': {'id': ciudad_id, 'nombre': nombre}})
    except Exception:
        conn.close()
        return jsonify({'success': False, 'message': 'La ciudad ya existe'}), 400

@app.route('/admin/ciudad/<int:ciudad_id>', methods=['DELETE'])
def admin_delete_ciudad(ciudad_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM ciudades WHERE id = ?', (ciudad_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/admin/negocio', methods=['POST'])
def admin_add_negocio():
    data = request.json or {}
    usuario = (data.get('usuario') or '').strip()
    contrasena = (data.get('contrasena') or '').strip()
    nombre = (data.get('nombre') or '').strip()
    if not nombre:
        return jsonify({'success': False, 'message': 'Nombre requerido'}), 400
    if not usuario or not contrasena:
        u, p = generate_credentials(nombre)
        if not usuario: usuario = u
        if not contrasena: contrasena = p
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO negocios (nombre, categoria, rating, reviews, imagen, promocion, descuento,
                                  direccion, mapsLink, telefono, whatsapp, horario, descripcion,
                                  servicios, usuario, contrasena, fotos, ciudad)
            VALUES (?, ?, 0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nombre, data.get('categoria', ''),
            data.get('imagen', 'https://images.unsplash.com/photo-1556740749-887f6717d7e4?w=400&h=300&fit=crop'),
            data.get('promocion', ''), int(data.get('descuento') or 0),
            data.get('direccion', ''), data.get('mapsLink', ''),
            data.get('telefono', ''), data.get('whatsapp', ''), data.get('horario', ''),
            data.get('descripcion', ''), json.dumps(data.get('servicios', [])),
            usuario, hash_password(contrasena),
            json.dumps(data.get('fotos', [])), data.get('ciudad', '')
        ))
        nuevo_id = c.lastrowid
        conn.commit()
        c.execute('SELECT * FROM negocios WHERE id = ?', (nuevo_id,))
        nuevo = dict_from_row(c.fetchone())
        conn.close()
        return jsonify({'success': True, 'negocio': nuevo, 'contrasena_plain': contrasena, 'usuario': usuario})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/negocio/<int:negocio_id>', methods=['PUT'])
def admin_update_negocio(negocio_id):
    data = request.json or {}
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT rating, reviews, contrasena FROM negocios WHERE id = ?', (negocio_id,))
    cur = c.fetchone()
    if not cur:
        conn.close()
        return jsonify({'success': False, 'message': 'Negocio no encontrado'}), 404
    contrasena_final = cur['contrasena']
    if data.get('contrasena'):
        contrasena_final = hash_password(data['contrasena'])
    try:
        c.execute('''
            UPDATE negocios SET nombre=?, categoria=?, rating=?, reviews=?, imagen=?, promocion=?,
                descuento=?, direccion=?, mapsLink=?, telefono=?, whatsapp=?, horario=?,
                descripcion=?, servicios=?, usuario=?, contrasena=?, fotos=?, ciudad=?
            WHERE id=?
        ''', (
            data.get('nombre', ''), data.get('categoria', ''),
            cur['rating'], cur['reviews'],
            data.get('imagen', ''), data.get('promocion', ''), int(data.get('descuento') or 0),
            data.get('direccion', ''), data.get('mapsLink', ''),
            data.get('telefono', ''), data.get('whatsapp', ''), data.get('horario', ''),
            data.get('descripcion', ''), json.dumps(data.get('servicios', [])),
            data.get('usuario', ''), contrasena_final,
            json.dumps(data.get('fotos', [])), data.get('ciudad', ''), negocio_id
        ))
        conn.commit()
        c.execute('SELECT * FROM negocios WHERE id = ?', (negocio_id,))
        negocio = dict_from_row(c.fetchone())
        conn.close()
        return jsonify({'success': True, 'negocio': negocio})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/negocio/<int:negocio_id>', methods=['DELETE'])
def admin_delete_negocio(negocio_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM valoraciones WHERE negocio_id = ?', (negocio_id,))
    c.execute('DELETE FROM ofertas WHERE negocio_id = ?', (negocio_id,))
    c.execute('DELETE FROM negocios WHERE id = ?', (negocio_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

def extraer_coords_de_mapslink(url):
    """Resuelve un link de Google Maps (corto o largo) y extrae lat,lng."""
    try:
        # Seguir redirecciones para links cortos (maps.app.goo.gl)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        final_url = resp.url
        # Buscar patrón @lat,lng o ll=lat,lng en la URL final
        m = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', final_url)
        if m:
            return float(m.group(1)), float(m.group(2))
        m = re.search(r'll=(-?\d+\.\d+),(-?\d+\.\d+)', final_url)
        if m:
            return float(m.group(1)), float(m.group(2))
        # Buscar en el contenido HTML
        content = resp.read().decode('utf-8', errors='ignore')
        m = re.search(r'"(-?\d{1,3}\.\d{4,}),(-?\d{1,3}\.\d{4,})"', content)
        if m:
            return float(m.group(1)), float(m.group(2))
    except Exception:
        pass
    return None, None

@app.route('/admin/negocio/<int:negocio_id>/coords-desde-link', methods=['POST'])
def coords_desde_link(negocio_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT mapsLink, lat, lng FROM negocios WHERE id=?', (negocio_id,))
    row = c.fetchone()
    if not row or not row['mapsLink']:
        conn.close()
        return jsonify({'success': False, 'error': 'Sin mapsLink'})
    if row['lat'] and row['lng']:
        conn.close()
        return jsonify({'success': True, 'lat': row['lat'], 'lng': row['lng'], 'source': 'saved'})
    lat, lng = extraer_coords_de_mapslink(row['mapsLink'])
    if lat and lng:
        c.execute('UPDATE negocios SET lat=?, lng=? WHERE id=?', (lat, lng, negocio_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'lat': lat, 'lng': lng, 'source': 'mapslink'})
    conn.close()
    return jsonify({'success': False, 'error': 'No se pudieron extraer coordenadas'})


@app.route('/admin/negocio/<int:negocio_id>/posicion', methods=['PUT'])
def admin_update_posicion(negocio_id):
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE negocios SET lat=?, lng=? WHERE id=?',
              (data.get('lat'), data.get('lng'), negocio_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/iconos-categoria', methods=['GET'])
def get_iconos_categoria():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT categoria, img_url, color FROM config_iconos')
    rows = {r['categoria']: {'img_url': r['img_url'], 'color': r['color']} for r in c.fetchall()}
    conn.close()
    return jsonify(rows)

@app.route('/admin/icono-categoria', methods=['PUT'])
def set_icono_categoria():
    try:
        data = request.get_json(force=True, silent=True) or {}
        cat = (data.get('categoria') or '').strip()
        if not cat:
            return jsonify({'success': False, 'error': 'Categoría requerida'}), 400
        conn = get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO config_iconos (categoria, img_url, color) VALUES (?,?,?)
                     ON CONFLICT(categoria) DO UPDATE SET img_url=excluded.img_url, color=excluded.color''',
                  (cat, data.get('img_url', ''), data.get('color', '#667eea')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ── OFERTAS (panel negocio + admin) ──────────────────────────────────────────

@app.route('/api/ofertas-negocio/<int:negocio_id>')
def get_ofertas_negocio(negocio_id):
    # Permitir acceso si es el negocio dueño O si viene del admin (sin sesión de negocio)
    if 'negocio_id' in session and session['negocio_id'] != negocio_id:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM ofertas WHERE negocio_id = ? ORDER BY id DESC', (negocio_id,))
    ofertas = [dict_from_row(row) for row in c.fetchall()]
    conn.close()
    return jsonify(ofertas)

@app.route('/admin/oferta', methods=['POST'])
def admin_crear_oferta():
    """Endpoint para admin — sin restricción de sesión de negocio"""
    data = request.json
    negocio_id = data.get('negocio_id')
    if not negocio_id:
        return jsonify({'error': 'negocio_id requerido'}), 400
    duracion = int(data.get('duracion_horas', 24))
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO ofertas (negocio_id, nombre, descripcion, precio_original, precio_oferta,
                             imagen, duracion_horas, fecha_vencimiento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (negocio_id, data['nombre'], data.get('descripcion', ''),
         data.get('precio_original', '0'), data.get('precio_oferta', '0'),
         data.get('imagen', ''), duracion,
         datetime.now() + timedelta(hours=duracion)))
    oid = c.lastrowid
    conn.commit()
    c.execute('SELECT * FROM ofertas WHERE id = ?', (oid,))
    oferta = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'oferta': oferta})

@app.route('/admin/oferta/<int:oferta_id>', methods=['PUT'])
def admin_actualizar_oferta(oferta_id):
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    duracion = data.get('duracion_horas')
    fv = datetime.now() + timedelta(hours=int(duracion)) if duracion else None
    c.execute('''UPDATE ofertas SET nombre=?, descripcion=?, precio_original=?, precio_oferta=?,
            imagen=?, duracion_horas=?, fecha_vencimiento=? WHERE id=?''',
        (data['nombre'], data.get('descripcion', ''), data.get('precio_original', '0'),
         data.get('precio_oferta', '0'), data.get('imagen', ''), duracion, fv, oferta_id))
    conn.commit()
    c.execute('SELECT * FROM ofertas WHERE id = ?', (oferta_id,))
    oferta = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'oferta': oferta})

@app.route('/admin/oferta/<int:oferta_id>', methods=['DELETE'])
def admin_eliminar_oferta(oferta_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM ofertas WHERE id = ?', (oferta_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


    data = request.json
    negocio_id = data.get('negocio_id') or session.get('negocio_id')
    if not negocio_id:
        return jsonify({'error': 'No autorizado'}), 401
    # Solo bloquear si hay sesión de negocio Y el negocio_id no coincide
    if 'negocio_id' in session and int(session['negocio_id']) != int(negocio_id):
        return jsonify({'error': 'No autorizado'}), 401
    duracion = int(data.get('duracion_horas', 24))
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO ofertas (negocio_id, nombre, descripcion, precio_original, precio_oferta,
                             imagen, duracion_horas, fecha_vencimiento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (negocio_id, data['nombre'], data.get('descripcion', ''),
          data.get('precio_original', '0'), data.get('precio_oferta', '0'),
          data.get('imagen', ''), duracion,
          datetime.now() + timedelta(hours=duracion)))
    oid = c.lastrowid
    conn.commit()
    c.execute('SELECT * FROM ofertas WHERE id = ?', (oid,))
    oferta = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'oferta': oferta})

@app.route('/api/oferta/<int:oferta_id>', methods=['PUT'])
@app.route('/api/oferta/<int:oferta_id>', methods=['PUT'])
def actualizar_oferta(oferta_id):
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT negocio_id FROM ofertas WHERE id = ?', (oferta_id,))
    r = c.fetchone()
    if not r:
        conn.close()
        return jsonify({'error': 'No encontrada'}), 404
    # Bloquear solo si hay sesión de negocio Y no coincide (admin sin sesión puede editar)
    if 'negocio_id' in session and int(session['negocio_id']) != int(r['negocio_id']):
        conn.close()
        return jsonify({'error': 'No autorizado'}), 401
    duracion = data.get('duracion_horas')
    fv = datetime.now() + timedelta(hours=int(duracion)) if duracion else None
    c.execute('''
        UPDATE ofertas SET nombre=?, descripcion=?, precio_original=?, precio_oferta=?,
            imagen=?, duracion_horas=COALESCE(?, duracion_horas),
            fecha_vencimiento=COALESCE(?, fecha_vencimiento)
        WHERE id=?
    ''', (data['nombre'], data.get('descripcion', ''), data.get('precio_original', '0'),
          data.get('precio_oferta', '0'), data.get('imagen', ''), duracion, fv, oferta_id))
    conn.commit()
    c.execute('SELECT * FROM ofertas WHERE id = ?', (oferta_id,))
    oferta = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'oferta': oferta})

@app.route('/api/oferta/<int:oferta_id>', methods=['DELETE'])
def eliminar_oferta(oferta_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT negocio_id FROM ofertas WHERE id = ?', (oferta_id,))
    r = c.fetchone()
    if not r:
        conn.close()
        return jsonify({'error': 'No encontrada'}), 404
    # Bloquear solo si hay sesión de negocio Y no coincide
    if 'negocio_id' in session and int(session['negocio_id']) != int(r['negocio_id']):
        conn.close()
        return jsonify({'error': 'No autorizado'}), 401
    c.execute('DELETE FROM ofertas WHERE id = ?', (oferta_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/visitas/<int:negocio_id>')
def get_visitas(negocio_id):
    if 'negocio_id' not in session or session['negocio_id'] != negocio_id:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    hoy = datetime.now().strftime('%Y-%m-%d')
    c.execute("SELECT COUNT(*) FROM visitas WHERE negocio_id=?", (negocio_id,))
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM visitas WHERE negocio_id=? AND fecha LIKE ?", (negocio_id, hoy+'%'))
    hoy_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM visitas WHERE negocio_id=? AND fecha >= datetime('now','-7 days')", (negocio_id,))
    semana = c.fetchone()[0]
    conn.close()
    return jsonify({'total': total, 'hoy': hoy_count, 'semana': semana})


@app.route('/api/cupones-negocio/<int:negocio_id>')
def get_cupones_negocio(negocio_id):
    if 'negocio_id' not in session or session['negocio_id'] != negocio_id:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT c.id, c.codigo, c.oferta_nombre, c.oferta_descripcion,
               c.precio_original, c.precio_oferta, c.reclamado_en, c.expira_en,
               c.canjeado, c.canjeado_en, u.username as usuario_nombre
        FROM cupones c
        JOIN usuarios u ON c.usuario_id = u.id
        JOIN ofertas o ON c.oferta_id = o.id
        WHERE o.negocio_id = ?
        ORDER BY c.reclamado_en DESC
    ''', (negocio_id,))
    cupones = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(cupones)

@app.route('/api/validar-cupon/<int:negocio_id>/<string:codigo>')
def validar_cupon(negocio_id, codigo):
    if 'negocio_id' not in session or session['negocio_id'] != negocio_id:
        return jsonify({'valido': False, 'mensaje': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''
        SELECT c.id, c.codigo, c.oferta_nombre, c.precio_original, c.precio_oferta,
               c.expira_en, c.reclamado_en, c.canjeado, u.username as usuario_nombre
        FROM cupones c
        JOIN usuarios u ON c.usuario_id = u.id
        JOIN ofertas o ON c.oferta_id = o.id
        WHERE c.codigo = ? AND o.negocio_id = ?
    ''', (codigo.upper(), negocio_id))
    cupon = c.fetchone()
    conn.close()
    if not cupon:
        return jsonify({'valido': False, 'mensaje': 'Código no encontrado'})
    if cupon['canjeado']:
        return jsonify({'valido': False, 'mensaje': 'Este cupón ya fue canjeado'})
    if cupon['expira_en'] < ahora:
        return jsonify({'valido': False, 'mensaje': 'Este cupón está expirado'})
    return jsonify({'valido': True, 'cupon': dict(cupon)})


@app.route('/api/cupon/<int:cupon_id>/canjear', methods=['POST'])
def canjear_cupon(cupon_id):
    if 'negocio_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT c.id, c.canjeado, c.expira_en FROM cupones c
        JOIN ofertas o ON c.oferta_id = o.id
        WHERE c.id = ? AND o.negocio_id = ?
    ''', (cupon_id, session['negocio_id']))
    cupon = c.fetchone()
    if not cupon:
        conn.close()
        return jsonify({'error': 'Cupón no encontrado'}), 404
    if cupon['canjeado']:
        conn.close()
        return jsonify({'error': 'Ya fue canjeado'}), 400
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if cupon['expira_en'] < ahora:
        conn.close()
        return jsonify({'error': 'Cupón expirado'}), 400
    c.execute('UPDATE cupones SET canjeado=1, canjeado_en=? WHERE id=?', (ahora, cupon_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})



@app.route('/api/pedidos/<int:negocio_id>')
def get_pedidos(negocio_id):
    if 'negocio_id' not in session or session['negocio_id'] != negocio_id:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pedidos WHERE negocio_id = ? ORDER BY fecha_creacion DESC', (negocio_id,))
    pedidos = [dict_from_row(row) for row in c.fetchall()]
    conn.close()
    return jsonify(pedidos)

@app.route('/api/pedido', methods=['POST'])
def crear_pedido():
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO pedidos (negocio_id, cliente_nombre, cliente_email, cliente_telefono, descripcion)
                 VALUES (?, ?, ?, ?, ?)''',
              (data['negocio_id'], data['cliente_nombre'],
               data.get('cliente_email', ''), data.get('cliente_telefono', ''), data['descripcion']))
    pid = c.lastrowid
    conn.commit()
    c.execute('SELECT * FROM pedidos WHERE id = ?', (pid,))
    pedido = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'id': pid, 'pedido': pedido})

@app.route('/api/pedido/<int:pedido_id>/estado', methods=['PUT'])
def actualizar_estado_pedido(pedido_id):
    if 'negocio_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT negocio_id FROM pedidos WHERE id = ?', (pedido_id,))
    r = c.fetchone()
    if not r or r['negocio_id'] != session['negocio_id']:
        conn.close()
        return jsonify({'error': 'No autorizado'}), 401
    estado = data.get('estado', 'pendiente')
    fc = datetime.now() if estado == 'completado' else None
    c.execute('UPDATE pedidos SET estado=?, notas_admin=?, fecha_completado=? WHERE id=?',
              (estado, data.get('notas', ''), fc, pedido_id))
    conn.commit()
    c.execute('SELECT * FROM pedidos WHERE id = ?', (pedido_id,))
    pedido = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'pedido': pedido})

# ── PRODUCTOS ─────────────────────────────────────────────────────────────────

@app.route('/api/productos/<int:negocio_id>')
def get_productos(negocio_id):
    if 'negocio_id' not in session or session['negocio_id'] != negocio_id:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM productos WHERE negocio_id = ? ORDER BY orden, id', (negocio_id,))
    productos = [dict_from_row(row) for row in c.fetchall()]
    conn.close()
    return jsonify(productos)

@app.route('/api/producto', methods=['POST'])
def crear_producto():
    if 'negocio_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COALESCE(MAX(orden), -1) + 1 FROM productos WHERE negocio_id = ?', (session['negocio_id'],))
    orden = c.fetchone()[0]
    c.execute('''INSERT INTO productos (negocio_id, nombre, descripcion, precio, categoria, imagen, disponible, orden)
                 VALUES (?, ?, ?, ?, ?, ?, 1, ?)''',
              (session['negocio_id'], data['nombre'], data.get('descripcion', ''),
               data['precio'], data.get('categoria', 'General'), data.get('imagen', ''), orden))
    pid = c.lastrowid
    conn.commit()
    c.execute('SELECT * FROM productos WHERE id = ?', (pid,))
    producto = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'producto': producto})

@app.route('/api/producto/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    if 'negocio_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.json
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT negocio_id FROM productos WHERE id = ?', (producto_id,))
    r = c.fetchone()
    if not r or r['negocio_id'] != session['negocio_id']:
        conn.close()
        return jsonify({'error': 'No autorizado'}), 401
    c.execute('''UPDATE productos SET nombre=?, descripcion=?, precio=?, categoria=?, imagen=?, disponible=?
                 WHERE id=?''',
              (data['nombre'], data.get('descripcion', ''), data['precio'],
               data.get('categoria', 'General'), data.get('imagen', ''),
               1 if data.get('disponible', True) else 0, producto_id))
    conn.commit()
    c.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
    producto = dict_from_row(c.fetchone())
    conn.close()
    return jsonify({'success': True, 'producto': producto})

@app.route('/api/producto/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    if 'negocio_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT negocio_id FROM productos WHERE id = ?', (producto_id,))
    r = c.fetchone()
    if not r or r['negocio_id'] != session['negocio_id']:
        conn.close()
        return jsonify({'error': 'No autorizado'}), 401
    c.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/producto/<int:producto_id>/disponible', methods=['PUT'])
def toggle_disponible(producto_id):
    if 'negocio_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT negocio_id, disponible FROM productos WHERE id = ?', (producto_id,))
    r = c.fetchone()
    if not r or r['negocio_id'] != session['negocio_id']:
        conn.close()
        return jsonify({'error': 'No autorizado'}), 401
    nuevo = 0 if r['disponible'] else 1
    c.execute('UPDATE productos SET disponible=? WHERE id=?', (nuevo, producto_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'disponible': nuevo})

# ================== USUARIOS / CUPONES ==================

@app.route('/usuario/login', methods=['GET', 'POST'])
def usuario_login():
    if request.method == 'POST':
        data = request.json or {}
        username = data.get('username', '')
        password = data.get('password', '')
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM usuarios WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['usuario_id'] = user['id']
            session['usuario_nombre'] = user['username']
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401
    return render_template('usuario_login.html')

@app.route('/usuario/logout')
def usuario_logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nombre', None)
    return redirect(url_for('usuario_login'))

@app.route('/usuario/cupones')
def mis_cupones():
    return render_template('mis_cupones.html')

@app.route('/api/reclamar_oferta', methods=['POST'])
def reclamar_oferta():
    data = request.json
    oferta_id = data.get('oferta_id')
    conn = get_connection()
    conn.isolation_level = 'EXCLUSIVE'
    c = conn.cursor()
    c.execute('SELECT o.*, n.nombre as negocio_nombre, n.whatsapp FROM ofertas o JOIN negocios n ON o.negocio_id=n.id WHERE o.id=?', (oferta_id,))
    oferta = c.fetchone()
    if not oferta:
        conn.close()
        return jsonify({'success': False, 'message': 'Oferta no encontrada'}), 404
    oferta_dict = dict(oferta)
    codigo = secrets.token_hex(4).upper()
    expira_en = (datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    qr_data = f"CUPON:{codigo}|OFERTA:{oferta_dict['nombre']}|NEGOCIO:{oferta_dict['negocio_nombre']}|PRECIO:{oferta_dict['precio_oferta']}|EXPIRA:{expira_en}"
    qr_img = qrcode.make(qr_data)
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    qr_b64 = base64.b64encode(buf.getvalue()).decode()
    conn.close()
    cupon = {
        'codigo': codigo,
        'qr_base64': qr_b64,
        'negocio_nombre': oferta_dict['negocio_nombre'],
        'negocio_whatsapp': oferta_dict['whatsapp'],
        'oferta_nombre': oferta_dict['nombre'],
        'oferta_descripcion': oferta_dict.get('descripcion') or '',
        'precio_original': oferta_dict['precio_original'],
        'precio_oferta': oferta_dict['precio_oferta'],
        'oferta_imagen': oferta_dict.get('imagen') or '',
        'reclamado_en': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'expira_en': expira_en,
        'canjeado': 0,
        'oferta_id': oferta_id
    }
    return jsonify({'success': True, 'cupon': cupon})

@app.route('/api/cupon/<int:cupon_id>', methods=['DELETE'])
def eliminar_cupon(cupon_id):
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'message': 'No autenticado'}), 401
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id FROM cupones WHERE id=? AND usuario_id=?', (cupon_id, session['usuario_id']))
    if not c.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'No encontrado'}), 404
    c.execute('DELETE FROM cupones WHERE id=?', (cupon_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    import socket
    local_ip = '127.0.0.1'
    try:
        hostname = socket.gethostname()
        ips = socket.getaddrinfo(hostname, None, socket.AF_INET)
        all_ips = list(set(r[4][0] for r in ips))
        for prefix in ('192.168.', '10.', '172.'):
            match = next((ip for ip in all_ips if ip.startswith(prefix)), None)
            if match:
                local_ip = match
                break
    except Exception:
        pass
    print(f"\n{'='*52}")
    print(f"  Servidor corriendo")
    print(f"  Local:   http://127.0.0.1:5000")
    print(f"  Red:     http://{local_ip}:5000")
    print(f"  Conectate al mismo WiFi y abrí")
    print(f"  la URL de Red en cualquier dispositivo")
    print(f"{'='*52}\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
