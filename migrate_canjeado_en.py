import sqlite3

DB = 'negocios.db'

conn = sqlite3.connect(DB)
c = conn.cursor()

# Verificar si la columna ya existe
c.execute("PRAGMA table_info(cupones)")
cols = [row[1] for row in c.fetchall()]

if 'canjeado_en' not in cols:
    c.execute("ALTER TABLE cupones ADD COLUMN canjeado_en TIMESTAMP")
    conn.commit()
    print("✓ Columna canjeado_en agregada correctamente")
else:
    print("✓ La columna canjeado_en ya existe, nada que hacer")

conn.close()
