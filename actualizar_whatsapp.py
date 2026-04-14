import sqlite3

def actualizar_whatsapp_todos():
    """Actualizar el WhatsApp de todos los negocios al número de Paraguay"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    # El número correcto para WhatsApp con código de Paraguay
    numero_whatsapp = '595982214686'  # +595 (Paraguay) 982 214 686
    
    # Actualizar todos los negocios
    c.execute('UPDATE negocios SET whatsapp = ?', (numero_whatsapp,))
    
    conn.commit()
    
    # Verificar cambios
    c.execute('SELECT COUNT(*) FROM negocios')
    total = c.fetchone()[0]
    
    c.execute('SELECT COUNT(DISTINCT whatsapp) FROM negocios')
    whatsapps_unicos = c.fetchone()[0]
    
    conn.close()
    
    print(f"✓ WhatsApp actualizado exitosamente")
    print(f"  • Total negocios: {total}")
    print(f"  • WhatsApp número: +{numero_whatsapp}")
    print(f"  • Teléfonos únicos: {whatsapps_unicos}")

if __name__ == '__main__':
    actualizar_whatsapp_todos()
