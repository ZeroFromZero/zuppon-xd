#!/usr/bin/env python3
from database import get_connection

def convertir_precio(precio_str):
    """Convierte precio de dólares a guaraníes: $X.XX -> X.000 Gs (aprox)"""
    try:
        # Extrae el número del string ($3.50 -> 3.50)
        valor = float(precio_str.replace('$', '').replace('Gs', '').strip())
        # Convierte a guaraníes (aprox 1 USD = 7000 Gs)
        valor_gs = int(valor * 7000)
        # Formatea con separador de miles: 24500 -> 24.500
        return f"{valor_gs:,}".replace(",", ".") + " Gs"
    except:
        return precio_str

def actualizar_precios():
    """Actualiza todos los precios a formato guaraní"""
    conn = get_connection()
    c = conn.cursor()
    
    # Obtener todas las ofertas
    c.execute("SELECT id, precio_original, precio_oferta FROM ofertas")
    ofertas = c.fetchall()
    
    actualizado = 0
    for oferta_id, precio_orig, precio_ofer in ofertas:
        # Solo convert if still in $ format
        if precio_orig and '$' in str(precio_orig):
            nuevo_orig = convertir_precio(precio_orig)
            nuevo_ofer = convertir_precio(precio_ofer)
            
            c.execute('''
                UPDATE ofertas 
                SET precio_original = ?, precio_oferta = ?
                WHERE id = ?
            ''', (nuevo_orig, nuevo_ofer, oferta_id))
            
            actualizado += 1
    
    conn.commit()
    conn.close()
    
    print(f"✓ {actualizado} ofertas actualizadas a formato guaraní")
    print("✓ Formato: 245.000 Gs (con separador de miles y Gs al final)")

if __name__ == '__main__':
    actualizar_precios()
