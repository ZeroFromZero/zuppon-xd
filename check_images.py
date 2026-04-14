import sqlite3

conn = sqlite3.connect('negocios.db')
c = conn.cursor()

# Verificar negocios sin imagen
c.execute('SELECT id, nombre, imagen FROM negocios')
negocios = c.fetchall()

sin_imagen = [n for n in negocios if not n[2] or n[2] == '']
print(f'Negocios sin imagen: {len(sin_imagen)}')
for n in sin_imagen:
    print(f'  ID {n[0]}: {n[1]}')

conn.close()
