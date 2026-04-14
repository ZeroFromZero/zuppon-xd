from database import get_connection, generate_credentials, hash_password

conn = get_connection()
c = conn.cursor()

# Obtener todos los negocios sin credenciales
c.execute('SELECT id, nombre FROM negocios WHERE usuario IS NULL OR usuario = ""')
negocios = c.fetchall()

print(f"Generando credenciales para {len(negocios)} negocios...\n")

for negocio in negocios:
    negocio_id = negocio['id']
    nombre = negocio['nombre']
    
    # Generar credenciales
    usuario, contrasena = generate_credentials(nombre)
    contrasena_hash = hash_password(contrasena)
    
    # Actualizar en BD
    c.execute('''
        UPDATE negocios 
        SET usuario = ?, contrasena = ?
        WHERE id = ?
    ''', (usuario, contrasena_hash, negocio_id))
    
    print(f"✓ {nombre}")
    print(f"  Usuario: {usuario}")
    print()

conn.commit()
conn.close()
print("¡Credenciales generadas para todos los negocios!")
