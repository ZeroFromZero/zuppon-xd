import sqlite3
conn = sqlite3.connect('negocios.db')
c = conn.cursor()
c.execute('PRAGMA table_info(negocios)')
cols = [r[1] for r in c.fetchall()]
print('Columnas:', cols)
missing = [col for col in ['ciudad', 'fotos', 'lat', 'lng'] if col not in cols]
print('Faltan:', missing)
for col in missing:
    try:
        c.execute(f'ALTER TABLE negocios ADD COLUMN {col} TEXT')
        print(f'Agregada: {col}')
    except Exception as e:
        print(f'Error {col}: {e}')
conn.commit()
conn.close()
