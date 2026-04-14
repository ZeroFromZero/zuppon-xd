from database import get_connection

c = get_connection().cursor()
c.execute('SELECT nombre, precio_original, precio_oferta FROM ofertas WHERE nombre LIKE "%Python%"')
rows = c.fetchall()
for row in rows:
    print(f'{row[0]}: {row[1]} -> {row[2]}')
