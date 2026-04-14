def insertar_negocios_ejemplo():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM negocios")
    if c.fetchone()[0] > 0:
        conn.close()
        return
    negocios = []
    ofertas_map = {}
