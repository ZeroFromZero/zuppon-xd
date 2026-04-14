import sqlite3

def convert_to_gs():
    """Convertir todos los precios de $ a Gs"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    # Obtener todas las ofertas
    c.execute('SELECT id, precio_original, precio_oferta FROM ofertas')
    ofertas = c.fetchall()
    
    conversiones = []
    
    for oferta_id, precio_original, precio_oferta in ofertas:
        # Convertir precios: remover $ y convertir a Gs
        # Ejemplo: $100 -> Gs 75.000 (usando tasa aproximada 1$ = 750)
        
        try:
            # Limpiar y convertir precio original
            original_clean = precio_original.replace('$', '').strip()
            original_valor = float(original_clean)
            original_gs = int(original_valor * 7500)  # Tasa: 1$ = 7500Gs
            
            # Limpiar y convertir precio oferta
            oferta_clean = precio_oferta.replace('$', '').strip()
            oferta_valor = float(oferta_clean)
            oferta_gs = int(oferta_valor * 7500)  # Tasa: 1$ = 7500Gs
            
            new_original = f"Gs {original_gs:,}".replace(',', '.')
            new_oferta = f"Gs {oferta_gs:,}".replace(',', '.')
            
            conversiones.append((new_original, new_oferta, oferta_id))
            
        except Exception as e:
            print(f"Error en oferta {oferta_id}: {e}")
    
    # Actualizar ofertas
    for new_original, new_oferta, oferta_id in conversiones:
        c.execute('''
            UPDATE ofertas
            SET precio_original = ?, precio_oferta = ?
            WHERE id = ?
        ''', (new_original, new_oferta, oferta_id))
    
    conn.commit()
    
    # Mostrar resumen
    print(f"✓ {len(conversiones)} ofertas actualizadas a Gs")
    
    # Mostrar ejemplos
    c.execute('SELECT nombre, precio_original, precio_oferta FROM ofertas LIMIT 5')
    print("\nEjemplos de ofertas:")
    for nombre, original, oferta in c.fetchall():
        print(f"  • {nombre}: {original} → {oferta}")
    
    conn.close()

if __name__ == '__main__':
    convert_to_gs()
