from database import get_connection, hash_password

conn = get_connection()
c = conn.cursor()

# Contraseña igual para todos
contrasena = 'admin123'
contrasena_hash = hash_password(contrasena)

# Obtener todos los negocios
c.execute('SELECT id, nombre FROM negocios')
negocios = c.fetchall()

print('✅ ASIGNANDO CREDENCIALES A TODOS LOS NEGOCIOS:')
print(f'Contraseña para todos: admin123\n')

for negocio in negocios:
    negocio_id = negocio['id']
    nombre = negocio['nombre']
    
    # Usuario basado en el nombre (simplificado)
    usuario = f'admin_{negocio_id}'
    
    # Actualizar negocio
    c.execute('''
        UPDATE negocios 
        SET usuario = ?, contrasena = ?
        WHERE id = ?
    ''', (usuario, contrasena_hash, negocio_id))
    
    print(f'✓ {nombre}')
    print(f'  Usuario: {usuario}')
    print(f'  Contraseña: admin123\n')

conn.commit()
conn.close()

print('✅ ¡Credenciales asignadas a todos los negocios!')
print('📝 Ejemplo de login:')
print('   Usuario: admin_1')
print('   Contraseña: admin123')
