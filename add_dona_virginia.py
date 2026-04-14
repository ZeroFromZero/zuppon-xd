import sqlite3

def add_dona_virginia():
    """Agregar negocio Doña Virginia con pizzas, lomitos y alimentos"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    # Agregar negocio
    dona_virginia = (
        'Doña Virginia - Pizzería & Comidas',
        'Restaurante',
        4.9,
        389,
        'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop',
        'Pizza familiar + lomito + bebida: 45% descuento. Delivery gratis compra mayor a Gs 100.000',
        45,
        'Calle Comercial 888, Asunción',
        '',
        '+595981234567',
        '595981234567',
        'Lun-Dom 10am-11pm',
        'Bienvenido a Doña Virginia, el lugar donde la tradición y el sabor se encuentran en cada platillo. Durante más de tres décadas, hemos sido el destino favorito de familias que buscan disfrutar de comida auténtica, preparada con ingredientes frescos y seleccionados cuidadosamente. Nuestras pizzas artesanales se elaboran con masa casera fermentada en frío durante 24 horas, acompañadas de mozzarella importada y receta de salsa de tomate exclusiva. Los lomitos son un clásico que preparamos con carnes premium, jamón de primera calidad y piña frita. Ofrecemos delivery a toda la capital, ambiente familiar acogedor, y personal capacitado que garantiza la mejor atención. Somos referencia en comida casera paraguaya y internacional. Visítanos y forma parte de nuestra familia gastronómica.',
        'Pizza,Lomito,Empanadas,Delivery,Carnes'
    )
    
    c.execute('''
        INSERT INTO negocios (nombre, categoria, rating, reviews, imagen, promocion, descuento, 
                            direccion, mapsLink, telefono, whatsapp, horario, descripcion, servicios)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dona_virginia)
    
    conn.commit()
    
    # Obtener el ID del nuevo negocio
    c.execute('SELECT id FROM negocios WHERE nombre = ?', ('Doña Virginia - Pizzería & Comidas',))
    negocio_id = c.fetchone()[0]
    
    # Agregar productos/ofertas
    productos = [
        ('Pizza Familiar Grande', 'Deliciosa pizza de 8 porciones preparada con masa casera fermentada, cubierta generosamente con queso mozzarella importado, jamón premium y champiñones frescos salteados. Perfecta para compartir en familia. Crujiente en los bordes y suave en el centro. Incluye bebida de cortesía.',
         'Gs 85.000', 'Gs 46.750', 'https://images.unsplash.com/photo-1604068549290-dea0e4a305ba?w=400&h=300&fit=crop'),
        ('Lomito Tradicional', 'Icónico sándwich paraguayo con carne tierna y jugosa, jamón de primera calidad, queso fundido, y piña frita caramelizada que le da ese toque dulce inconfundible. Acompañado con papas crocantes caseras. Una auténtica experiencia de sabor que define la gastronomía local.',
         'Gs 45.000', 'Gs 24.750', 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop'),
        ('Empanadas Variadas x6', 'Seis empanadas recién horneadas con rellenos diversos: carne molida jugosa, queso derretido con cebolla, y pollo desmenuzado con especias. Masa crocante y dorada, preparadas en nuestro horno artesanal. Ideales para entrada, almuerzo o merienda.',
         'Gs 30.000', 'Gs 16.500', 'https://images.unsplash.com/photo-1566215061694-ca94e1f84b69?w=400&h=300&fit=crop'),
        ('Milanesa de Pollo', 'Milanesa de pechuga de pollo de 300 gramos, empanizada con pan casero tostado, cocida en aceite de oliva. Tierna por dentro, crujiente por fuera. Acompañada con papas caseras recién fritas y ensalada fresca de temporada.',
         'Gs 52.500', 'Gs 28.875', 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop'),
        ('Carne a la Parrilla', 'Corte premium de carne vacuna a la parrilla con punto justo. Jugosa, tierna y sabrosa, acompañada con paper de verduras frescas, ensalada criolla con tomate, cebolla y cilantro, más pan casero casero recién salido del horno. Experiencia gourmet garantizada.',
         'Gs 67.500', 'Gs 37.125', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop'),
        ('Sopa Casera', 'Sopa tradicional hecha diariamente con caldo de pollo casero, verduras de temporada (zanahoria, apio, papa), fideos caseros artesanales y pollo tierno. Caliente, reconfortante y elaborada con la receta de generaciones. Perfecta para cualquier ocasión.',
         'Gs 22.500', 'Gs 12.375', 'https://images.unsplash.com/photo-1476124369162-f4978d68f779?w=400&h=300&fit=crop'),
        ('Chipa Guazú', 'Chipa tradicional paraguaya hecha con maíz molido fresco, queso derretido y huevos. Crujiente y jugosa, salida del horno a diario. Sabor auténtico de la cocina paraguaya. Perfecta como desayuno, almuerzo o cena, acompañada con leche o té.',
         'Gs 15.000', 'Gs 8.250', 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop'),
        ('Set Completo Familia', 'Pack especial para familias: una pizza familiar + dos deliciosos lomitos + seis empanadas variadas + bebida grande. Todo lo que necesitas para una comida en familia completa, con sabores que complacerán a todos. Ahorro garantizado y calidad sin compromisos.',
         'Gs 180.000', 'Gs 99.000', 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop'),
    ]
    
    for orden, (nombre, descripcion, precio_original, precio_oferta, imagen) in enumerate(productos, 1):
        c.execute('''
            INSERT INTO ofertas (negocio_id, nombre, descripcion, precio_original, precio_oferta, imagen, orden)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (negocio_id, nombre, descripcion, precio_original, precio_oferta, imagen, orden))
    
    conn.commit()
    
    print(f"✓ Doña Virginia agregado exitosamente (ID: {negocio_id})")
    print(f"✓ {len(productos)} productos/ofertas agregados")
    print("\nProductos de Doña Virginia:")
    for nombre, _, _, _, _ in productos:
        print(f"  • {nombre}")
    
    conn.close()

if __name__ == '__main__':
    add_dona_virginia()
