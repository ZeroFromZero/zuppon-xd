import sqlite3

def update_cafe_aroma():
    """Actualizar descripción de Café Aroma Gourmet"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    nueva_descripcion = """Café Aroma Gourmet es el destino perfecto para los amantes del café artesanal en Encarnación. Con más de 15 años de experiencia, somos especialistas en la preparación de bebidas de café premium, seleccionando granos de las mejores plantaciones de América Latina. Nuestro ambiente acogedor y elegante, decorado con detalles rústicos que combinan calidez y sofisticación, es ideal para disfrutar en pareja, con amigos o para trabajar en un espacio tranquilo. 

Ofrecemos un menú variado que incluye desde clásicos espresso, cappuccino y americano, hasta bebidas innovadoras creadas por nuestros baristas certificados. Acompañamos cada café con pasteles artesanales, sándwiches gourmet y opciones vegetarianas. Nuestro equipo es atento y capacitado, siempre dispuesto a recomendarte la mejor opción según tus preferencias. 

El ambiente música seleccionada, el aroma inconfundible del café recién tostado, y la comodidad de nuestros espacios con wifi gratis hacen de Café Aroma tu lugar favorito para relajarte. Abierto todos los días para que disfrutes de un verdadero café de calidad, hecho con pasión y dedicación."""
    
    c.execute('''
        UPDATE negocios 
        SET descripcion = ?
        WHERE nombre = ?
    ''', (nueva_descripcion, 'Café Aroma'))
    
    conn.commit()
    
    # Verificar la actualización
    c.execute('SELECT id, nombre, descripcion FROM negocios WHERE nombre = ?', ('Café Aroma',))
    resultado = c.fetchone()
    
    if resultado:
        print(f"✓ Descripción actualizada para: {resultado[1]}")
        print(f"\nDescripción (primeros 200 caracteres):")
        print(resultado[2][:200] + "...")
    else:
        print("⚠ Negocio no encontrado. Asegúrate de que existe en la base de datos.")
    
    conn.close()

if __name__ == '__main__':
    update_cafe_aroma()
