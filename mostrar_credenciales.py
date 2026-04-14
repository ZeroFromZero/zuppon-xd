#!/usr/bin/env python3
"""
Regenera credenciales con usuarios LIMPIOS sin caracteres especiales
"""
from database import get_connection, hash_password
import secrets
import string

def generar_usuario_limpio(nombre):
    """Generar usuario limpios sin caracteres especiales"""
    # Convertir a minúsculas
    usuario = nombre.lower()
    
    # Reemplazar caracteres especiales
    usuario = usuario.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    usuario = usuario.replace('ñ', 'n').replace('"', '').replace("'", '')
    usuario = usuario.replace('á', 'a').replace('à', 'a')
    
    # Reemplazar espacios y caracteres especiales con _
    usuario = ''.join(c if c.isalnum() else '_' for c in usuario)
    
    # Limitar a 20 caracteres
    usuario = usuario[:20].rstrip('_')
    
    # Agregar número aleatorio
    usuario = usuario + '_' + ''.join(secrets.choice(string.digits) for _ in range(4))
    
    return usuario

def generar_contrasena():
    """Generar contraseña aleatoria de 8 caracteres"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))

conn = get_connection()
c = conn.cursor()

# Obtener TODOS los negocios
c.execute('SELECT id, nombre FROM negocios ORDER BY nombre')
negocios = c.fetchall()

print(f"\n🔐 REGENERANDO CREDENCIALES LIMPIAS PARA {len(negocios)} NEGOCIOS...\n")

credenciales_txt = "=" * 80 + "\n"
credenciales_txt += "CREDENCIALES DE ACCESO - PANEL DE NEGOCIOS\n"
credenciales_txt += "=" * 80 + "\n\n"
credenciales_txt += f"Servidor: http://localhost:5000/login\n\n"

for negocio in negocios:
    negocio_id = negocio['id']
    nombre = negocio['nombre']
    
    # Generar credenciales LIMPIAS
    usuario = generar_usuario_limpio(nombre)
    contrasena = generar_contrasena()
    contrasena_hash = hash_password(contrasena)
    
    # Actualizar en BD
    c.execute('''
        UPDATE negocios 
        SET usuario = ?, contrasena = ?
        WHERE id = ?
    ''', (usuario, contrasena_hash, negocio_id))
    
    print(f"✓ {nombre}")
    print(f"  Usuario: {usuario}")
    print(f"  Contraseña: {contrasena}\n")
    
    credenciales_txt += f"NEGOCIO: {nombre}\n"
    credenciales_txt += f"  Usuario:     {usuario}\n"
    credenciales_txt += f"  Contraseña:  {contrasena}\n"
    credenciales_txt += "-" * 80 + "\n"

conn.commit()
conn.close()

# Guardar en archivo
with open('CREDENCIALES.txt', 'w', encoding='utf-8') as f:
    f.write(credenciales_txt)

print("\n✅ ¡Credenciales LIMPIAS regeneradas!")
print("📝 Abre CREDENCIALES.txt para copiar el usuario y contraseña exactamente")
