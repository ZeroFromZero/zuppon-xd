import sqlite3
import json
from datetime import datetime
import hashlib
import secrets
import string

def init_db():
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS negocios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL, categoria TEXT NOT NULL,
            rating REAL DEFAULT 0, reviews INTEGER DEFAULT 0,
            imagen TEXT, promocion TEXT NOT NULL, descuento INTEGER NOT NULL,
            direccion TEXT NOT NULL, mapsLink TEXT,
            telefono TEXT NOT NULL, whatsapp TEXT NOT NULL,
            horario TEXT NOT NULL, descripcion TEXT, servicios TEXT,
            usuario TEXT UNIQUE, contrasena TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS valoraciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            negocio_id INTEGER NOT NULL, nombre TEXT NOT NULL,
            rating INTEGER NOT NULL, comentario TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (negocio_id) REFERENCES negocios (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS ofertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            negocio_id INTEGER NOT NULL, nombre TEXT NOT NULL,
            descripcion TEXT, precio_original TEXT NOT NULL,
            precio_oferta TEXT NOT NULL, imagen TEXT, orden INTEGER DEFAULT 0,
            fecha_vencimiento TIMESTAMP, duracion_horas INTEGER DEFAULT 48,
            FOREIGN KEY (negocio_id) REFERENCES negocios (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            negocio_id INTEGER NOT NULL, cliente_nombre TEXT NOT NULL,
            cliente_email TEXT, cliente_telefono TEXT,
            descripcion TEXT NOT NULL, estado TEXT DEFAULT 'pendiente',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_completado TIMESTAMP, notas_admin TEXT,
            FOREIGN KEY (negocio_id) REFERENCES negocios (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            negocio_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio TEXT NOT NULL,
            categoria TEXT DEFAULT 'General',
            imagen TEXT,
            disponible INTEGER DEFAULT 1,
            orden INTEGER DEFAULT 0,
            FOREIGN KEY (negocio_id) REFERENCES negocios (id)
        )
    ''')
    # Tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Tabla de cupones
    c.execute('''
        CREATE TABLE IF NOT EXISTS cupones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            oferta_id INTEGER NOT NULL,
            negocio_nombre TEXT NOT NULL,
            oferta_nombre TEXT NOT NULL,
            oferta_descripcion TEXT DEFAULT '',
            precio_original TEXT NOT NULL DEFAULT '',
            precio_oferta TEXT NOT NULL,
            codigo TEXT UNIQUE NOT NULL,
            qr_base64 TEXT NOT NULL,
            reclamado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expira_en TIMESTAMP NOT NULL,
            canjeado INTEGER DEFAULT 0,
            canjeado_en TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (oferta_id) REFERENCES ofertas (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS config_iconos (
            categoria TEXT PRIMARY KEY,
            img_url TEXT,
            color TEXT DEFAULT '#667eea'
        )
    ''')
    try:
        c.execute('ALTER TABLE negocios ADD COLUMN fotos TEXT')
    except Exception:
        pass
    try:
        c.execute('ALTER TABLE negocios ADD COLUMN lat REAL')
    except Exception:
        pass
    try:
        c.execute('ALTER TABLE negocios ADD COLUMN lng REAL')
    except Exception:
        pass
    try:
        c.execute('ALTER TABLE negocios ADD COLUMN ciudad TEXT DEFAULT ""')
    except Exception:
        pass
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS ciudades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )''')
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE cupones ADD COLUMN oferta_descripcion TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE cupones ADD COLUMN oferta_imagen TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            negocio_id INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (negocio_id) REFERENCES negocios (id)
        )''')
    except Exception:
        pass
    # Insertar/actualizar usuario de prueba
    try:
        c.execute("INSERT OR IGNORE INTO usuarios (username, password) VALUES ('usuario1', '123')")
        c.execute("UPDATE usuarios SET password='123' WHERE username='usuario1'")
    except Exception:
        pass
    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect('negocios.db')
    conn.row_factory = sqlite3.Row
    return conn


def insertar_negocios_ejemplo():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM negocios")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    negocios = [
        ("Pizzeria Don Giuseppe", "Restaurante",
         "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&h=400&fit=crop",
         "Pizza familiar 15% OFF", 15, "Maria Auxiliadora, Itapua, Paraguay",
         "+595971100001", "595971100001", "Lun-Dom 6pm-11pm",
         "Pizzeria Don Giuseppe es el restaurante italiano mas querido de Maria Auxiliadora. Fundada en 2010 por la familia Rossi, ofrecemos pizzas artesanales horneadas en horno de lena a 400 grados. Nuestra masa se fermenta 48 horas para lograr una textura crujiente por fuera y suave por dentro. Usamos tomates San Marzano importados, mozzarella fresca local y ingredientes de primera calidad. Capacidad para 60 personas, salon privado para eventos, servicio de delivery en toda la zona.",
         json.dumps(["https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&h=400&fit=crop"])),
        ("Cafe Aroma", "Cafeteria",
         "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&h=400&fit=crop",
         "Cafe + medialunas 20% OFF", 20, "Encarnacion, Itapua, Paraguay",
         "+595971100002", "595971100002", "Lun-Vie 7am-8pm, Sab 8am-6pm",
         "Cafe Aroma es el punto de encuentro favorito de Encarnacion desde 2015. Trabajamos con granos de cafe de origen unico de las sierras de Misiones, tostados artesanalmente cada semana. Ofrecemos espresso, cappuccino, cold brew y mas de 15 variedades de te. Nuestras medialunas y facturas se hornean cada manana a las 5am. Contamos con WiFi gratuito, enchufes en cada mesa y un ambiente ideal para trabajar o reunirse. Capacidad 40 personas, terraza exterior disponible.",
         json.dumps(["https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=600&h=400&fit=crop"])),
        ("Gym Fitness Pro", "Gimnasio",
         "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&h=400&fit=crop",
         "Membresia mensual 20% OFF", 20, "Coronel Bogado, Itapua, Paraguay",
         "+595971100003", "595971100003", "Lun-Vie 6am-10pm, Sab 7am-8pm, Dom 8am-2pm",
         "Gym Fitness Pro es el gimnasio mas completo de Coronel Bogado con mas de 500 socios activos. Contamos con zona de pesas libre, maquinas cardio de ultima generacion, sala de spinning con 20 bicicletas, area de crossfit y clases grupales de yoga, zumba y pilates. Nuestros 4 entrenadores certificados ofrecen planes personalizados incluidos en la membresia. Vestuarios con duchas calientes, estacionamiento gratuito y bar de proteinas. Abierto los 365 dias del ano.",
         json.dumps(["https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1540497077202-7c8a3999166f?w=600&h=400&fit=crop"])),
        ("Peluqueria Estilo & Arte", "Peluqueria",
         "https://images.unsplash.com/photo-1562322506-f9a60b3b4f25?w=600&h=400&fit=crop",
         "Corte + lavado 25% OFF", 25, "Encarnacion, Itapua, Paraguay",
         "+595971100004", "595971100004", "Mar-Vie 9am-7pm, Sab 8am-6pm",
         "Peluqueria Estilo & Arte cuenta con 8 anos de experiencia y un equipo de 5 estilistas certificados en Buenos Aires y Sao Paulo. Especializados en colorimetria avanzada, balayage, mechas californianas, keratina brasilena y tratamientos de hidratacion profunda. Usamos exclusivamente productos Wella, Schwarzkopf y Loreal Professional. Cada servicio incluye diagnostico capilar gratuito. Reservas online disponibles. Ambiente moderno y relajado con musica en vivo los sabados.",
         json.dumps(["https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1560066984-138daaa4e4e1?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&h=400&fit=crop"])),
        ("Instituto EduTech Paraguay", "Educacion",
         "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=600&h=400&fit=crop",
         "Curso de programacion 30% OFF", 30, "Asuncion, Paraguay",
         "+595971100005", "595971100005", "Lun-Vie 8am-9pm, Sab 8am-1pm",
         "Instituto EduTech Paraguay es el centro de formacion tecnologica lider del pais con mas de 2.000 egresados. Ofrecemos cursos de Python, JavaScript, diseño UX/UI, marketing digital y ciberseguridad. Modalidades: presencial en Asuncion, online en vivo y grabado. Duracion: 3 meses intensivos (120 horas). Horarios: manana 8am-12pm, tarde 2pm-6pm o noche 6pm-9pm. Certificacion internacional reconocida por empresas de la region. Bolsa de trabajo activa con mas de 50 empresas aliadas. Clases de prueba gratuitas disponibles.",
         json.dumps(["https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=600&h=400&fit=crop"])),
        ("Boutique Moda Femenina", "Moda",
         "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=600&h=400&fit=crop",
         "Compra 2 prendas y lleva 1 gratis", 33, "Encarnacion, Itapua, Paraguay",
         "+595971100006", "595971100006", "Lun-Sab 9am-8pm, Dom 10am-2pm",
         "Boutique Moda Femenina trae las ultimas tendencias de Buenos Aires, Sao Paulo y Miami directamente a Encarnacion. Renovamos coleccion cada 30 dias con mas de 200 prendas nuevas. Trabajamos con marcas nacionales e importadas: vestidos, blusas, pantalones, ropa deportiva y accesorios. Servicio de asesoramiento de imagen personalizado sin costo. Tallas XS a XXL disponibles. Envios a todo el pais en 48 horas. Programa de fidelidad: acumula puntos y canjea descuentos.",
         json.dumps(["https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600&h=400&fit=crop"])),
        ("Farmacia San Rafael", "Farmacia",
         "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&h=400&fit=crop",
         "15% OFF en medicamentos genericos", 15, "Coronel Bogado, Itapua, Paraguay",
         "+595971100007", "595971100007", "Lun-Dom 7am-10pm",
         "Farmacia San Rafael lleva 20 anos cuidando la salud de Coronel Bogado y alrededores. Contamos con mas de 5.000 productos: medicamentos de marca y genericos, cosmeticos, ortopedia, nutricion deportiva y productos naturales. Farmaceutico de guardia las 24 horas para consultas. Servicio de delivery en toda la ciudad. Convenios con las principales aseguradoras medicas del pais. Programa de medicacion cronica con descuentos especiales para pacientes frecuentes.",
         json.dumps(["https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1563213126-a4273aed2016?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1576602976047-174e57a47881?w=600&h=400&fit=crop"])),
        ("Club Deportivo Itapua", "Deportes",
         "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&h=400&fit=crop",
         "Inscripcion anual 25% OFF", 25, "Encarnacion, Itapua, Paraguay",
         "+595971100008", "595971100008", "Lun-Dom 6am-10pm",
         "Club Deportivo Itapua es el complejo deportivo mas grande de la region con 5 hectareas de instalaciones. Disciplinas disponibles: futbol (4 canchas de cesped sintetico), tenis (6 canchas), natacion (pileta olimpica y recreativa), basquet, voley y atletismo. Clases para ninos desde 4 anos, adultos y adultos mayores. Torneos internos mensuales. Cafeteria y vestuarios modernos. La membresia anual incluye acceso ilimitado a todas las instalaciones y 2 clases grupales por semana.",
         json.dumps(["https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1529900748604-07564a03e7a6?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=600&h=400&fit=crop"])),
        ("Sushi Nikkei Encarnacion", "Restaurante",
         "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=600&h=400&fit=crop",
         "2x1 en rolls los martes", 50, "Encarnacion, Itapua, Paraguay",
         "+595971100009", "595971100009", "Mar-Dom 12pm-3pm y 7pm-11pm",
         "Sushi Nikkei Encarnacion fusiona la tradicion japonesa con sabores latinoamericanos en el corazon de Encarnacion. Nuestro chef principal se formo en Tokio y Lima durante 8 anos. El pescado llega fresco cada manana desde Asuncion. Menu de mas de 40 variedades de rolls, nigiris, sashimi y platos calientes. Carta de vinos y sake seleccionada. Ambiente intimo con capacidad para 35 personas. Reservas recomendadas los fines de semana. Opcion de omakase (menu degustacion) con aviso previo.",
         json.dumps(["https://images.unsplash.com/photo-1617196034183-421b4040ed20?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1562802378-063ec186a863?w=600&h=400&fit=crop"])),
        ("Libreria Cultural del Sur", "Educacion",
         "https://images.unsplash.com/photo-1507842217343-583f20270319?w=600&h=400&fit=crop",
         "Libro + cafe gratis 20% OFF", 20, "Encarnacion, Itapua, Paraguay",
         "+595971100010", "595971100010", "Lun-Sab 8am-8pm",
         "Libreria Cultural del Sur es mucho mas que una libreria: es un espacio cultural con mas de 15.000 titulos disponibles. Secciones de literatura, ciencias, infantil, academico, autoayuda y arte. Organizamos presentaciones de libros, talleres de escritura y club de lectura mensual. Nuestro cafe interno sirve bebidas artesanales mientras lees. Servicio de pedidos especiales con entrega en 72 horas. Descuentos permanentes para docentes y estudiantes con credencial. Envios a todo Paraguay.",
         json.dumps(["https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600&h=400&fit=crop"])),
        ("Spa & Bienestar Lotus", "Spa",
         "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=600&h=400&fit=crop",
         "Masaje relajante 30% OFF", 30, "Encarnacion, Itapua, Paraguay",
         "+595971100011", "595971100011", "Lun-Dom 9am-9pm",
         "Spa & Bienestar Lotus es el refugio de relajacion mas exclusivo de Encarnacion. Ofrecemos masajes terapeuticos, masajes con piedras calientes, reflexologia, faciales con productos organicos, envolturas corporales y aromaterapia. Nuestras 6 cabinas privadas estan disenadas para una experiencia de total privacidad. Sauna finlandesa y jacuzzi disponibles. Todos nuestros terapeutas tienen certificacion internacional. Paquetes para parejas y grupos disponibles. Reserva con 24 horas de anticipacion.",
         json.dumps(["https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1519823551278-64ac92734fb1?w=600&h=400&fit=crop"])),
        ("Veterinaria Patitas Felices", "Veterinaria",
         "https://images.unsplash.com/photo-1628009368231-7bb7cfcb0def?w=600&h=400&fit=crop",
         "Consulta + vacuna 20% OFF", 20, "Coronel Bogado, Itapua, Paraguay",
         "+595971100012", "595971100012", "Lun-Sab 8am-7pm, Dom 9am-1pm",
         "Veterinaria Patitas Felices atiende a perros, gatos, aves y animales exoticos con un equipo de 3 veterinarios especializados. Servicios: consultas generales, cirugia, internacion 24hs, laboratorio propio, radiografia digital, ecografia, peluqueria canina y felina, y tienda de alimentos premium. Programa de vacunacion anual con recordatorio por WhatsApp. Convenios con aseguradoras de mascotas. Urgencias veterinarias disponibles. Mas de 1.500 pacientes activos en nuestra base de datos.",
         json.dumps(["https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1548767797-d8c844163c4a?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1601758124510-52d02ddb7cbd?w=600&h=400&fit=crop"])),
        ("Panaderia & Pasteleria La Vienesa", "Panaderia",
         "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&h=400&fit=crop",
         "Docena de medialunas 15% OFF", 15, "Maria Auxiliadora, Itapua, Paraguay",
         "+595971100013", "595971100013", "Lun-Dom 5:30am-8pm",
         "La Vienesa es la panaderia artesanal mas tradicional de Maria Auxiliadora, con 35 anos de historia familiar. Horneamos mas de 40 variedades de pan cada dia desde las 4am: pan de campo, baguettes, pan integral, medialunas de manteca y grasa, facturas, tortas y pasteles. Tortas personalizadas para cumpleanos, casamientos y eventos con 48hs de anticipacion. Ingredientes 100% naturales sin conservantes. Delivery disponible para pedidos mayores a 50.000 Gs. Pedidos por WhatsApp.",
         json.dumps(["https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1568254183919-78a4f43a2877?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=600&h=400&fit=crop"])),
        ("Optica Vision Clara", "Salud",
         "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=600&h=400&fit=crop",
         "Armazon + lentes 25% OFF", 25, "Encarnacion, Itapua, Paraguay",
         "+595971100014", "595971100014", "Lun-Sab 8am-6pm",
         "Optica Vision Clara ofrece atencion visual completa con optometristas certificados y la tecnologia mas avanzada de la region. Examen visual computarizado gratuito con cada compra. Mas de 500 modelos de armazones de marcas como Ray-Ban, Oakley, Vogue y marcas nacionales. Lentes oftalmicos, de contacto diarios, mensuales y de colores. Servicio express: lentes listos en 1 hora para graduaciones simples. Garantia de 1 ano en todos los productos. Convenios con obras sociales y seguros medicos.",
         json.dumps(["https://images.unsplash.com/photo-1508296695146-257a814070b4?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1591076482161-42ce6da69f67?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1577401239170-897942555fb3?w=600&h=400&fit=crop"])),
        ("Academia de Ingles Global", "Educacion",
         "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=600&h=400&fit=crop",
         "Primer mes de clases 40% OFF", 40, "Encarnacion, Itapua, Paraguay",
         "+595971100015", "595971100015", "Lun-Vie 7am-9pm, Sab 8am-1pm",
         "Academia de Ingles Global es el instituto de idiomas mas reconocido de Encarnacion con 12 anos de trayectoria y mas de 800 alumnos activos. Ofrecemos ingles, portugues y aleman en niveles desde principiante hasta avanzado. Metodologia comunicativa 100% practica. Grupos reducidos de maximo 8 alumnos. Horarios flexibles: manana 7am-12pm, tarde 2pm-6pm, noche 6pm-9pm y sabados 8am-1pm. Duracion por nivel: 3 meses (48 horas). Certificacion Cambridge disponible. Clases de conversacion con nativos 2 veces por semana.",
         json.dumps(["https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&h=400&fit=crop"])),
        ("Ferreteria El Constructor", "Ferreteria",
         "https://images.unsplash.com/photo-1504148455328-c376907d081c?w=600&h=400&fit=crop",
         "10% OFF en herramientas electricas", 10, "Coronel Bogado, Itapua, Paraguay",
         "+595971100016", "595971100016", "Lun-Sab 7am-6pm",
         "Ferreteria El Constructor es el proveedor de confianza de constructores, electricistas y plomeros de Coronel Bogado desde 1998. Mas de 8.000 productos en stock: herramientas manuales y electricas, materiales de construccion, pinturas, plomeria, electricidad, jardineria y seguridad industrial. Marcas lideres: Bosch, Stanley, Makita, DeWalt. Asesoramiento tecnico gratuito en obra. Credito a 12 cuotas sin interes para compras mayores a 500.000 Gs. Delivery en camioneta para pedidos grandes. Presupuestos para obras.",
         json.dumps(["https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop"])),
        ("Barberia Vintage Cuts", "Peluqueria",
         "https://images.unsplash.com/photo-1599458438325-93854b8f5c4f?w=600&h=400&fit=crop",
         "Corte + barba 20% OFF", 20, "Maria Auxiliadora, Itapua, Paraguay",
         "+595971100017", "595971100017", "Mar-Dom 9am-7pm",
         "Barberia Vintage Cuts es el espacio de grooming masculino mas exclusivo de Maria Auxiliadora. Nuestros 3 barberos certificados dominan cortes clasicos, fade, undercut, pompadour y estilos modernos. El servicio de barba incluye afeitado con navaja, toalla caliente, aceites y balsamos premium. Usamos productos de las marcas American Crew, Layrite y Uppercut. Ambiente retro con musica de los 60s y 70s. Reservas por WhatsApp con hasta 7 dias de anticipacion. Tarjeta de fidelidad: 10 cortes y el 11 es gratis.",
         json.dumps(["https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1622286342621-4bd786c2447c?w=600&h=400&fit=crop"])),
        ("Tienda de Bicicletas CyclePy", "Deportes",
         "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=600&h=400&fit=crop",
         "Servicio de mantenimiento 30% OFF", 30, "Encarnacion, Itapua, Paraguay",
         "+595971100018", "595971100018", "Lun-Sab 8am-6pm",
         "CyclePy es la tienda especializada en ciclismo mas completa del sur de Paraguay. Vendemos bicicletas de ruta, MTB, urbanas y electricas de marcas como Trek, Giant, Specialized y Caloi. Nuestro taller cuenta con mecanicos certificados que realizan mantenimiento preventivo, reparaciones, cambio de componentes y personalizacion. Accesorios: cascos, luces, candados, ropa tecnica y GPS. Clases de ciclismo para principiantes los sabados. Grupo de rodada semanal los domingos a las 7am. Financiacion disponible.",
         json.dumps(["https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?w=600&h=400&fit=crop"])),
        ("Consultorio Dental Sonrisa", "Salud",
         "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=600&h=400&fit=crop",
         "Limpieza dental gratis con consulta", 100, "Encarnacion, Itapua, Paraguay",
         "+595971100019", "595971100019", "Lun-Vie 8am-6pm, Sab 8am-12pm",
         "Consultorio Dental Sonrisa es una clinica odontologica integral con 15 anos de experiencia y 4 especialistas. Servicios: odontologia general, ortodoncia con brackets metalicos y esteticos, implantes dentales, blanqueamiento laser, cirugia oral, endodoncia y periodoncia. Equipamiento de ultima generacion: radiografia digital, escaner 3D y laser dental. Atencion para toda la familia desde los 3 anos. Presupuesto sin cargo. Financiacion en hasta 24 cuotas. Convenios con las principales obras sociales del pais.",
         json.dumps(["https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1609840114035-3c981b782dfe?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=600&h=400&fit=crop"])),
        ("Heladeria Dulce Frio", "Cafeteria",
         "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=600&h=400&fit=crop",
         "2 helados al precio de 1 los fines de semana", 50, "Maria Auxiliadora, Itapua, Paraguay",
         "+595971100020", "595971100020", "Lun-Dom 10am-11pm",
         "Heladeria Dulce Frio elabora sus helados artesanalmente cada dia con leche fresca de tambo local y frutas de estacion. Mas de 30 sabores rotativos: cremas, frutales, veganos y sin azucar. Especialidades: sundaes, batidos, waffles con helado, crepes y postres frios. Tortas heladas personalizadas para eventos con 48hs de anticipacion. Ambiente familiar con zona de juegos para ninos. Los fines de semana hay musica en vivo. Servicio de catering para fiestas y eventos corporativos.",
         json.dumps(["https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=600&h=400&fit=crop","https://images.unsplash.com/photo-1576506295286-5cda18df43e7?w=600&h=400&fit=crop"])),
    ]

    ofertas_map = {
        "Pizzeria Don Giuseppe":    ("Pizza Margherita", "Masa fermentada 48h, tomate San Marzano, mozzarella fresca y albahaca. Horneada en horno de lena a 400 grados. Diametro 35cm. Tiempo de preparacion: 15 minutos.", "47.000 Gs", "40.000 Gs", "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop"),
        "Cafe Aroma":               ("Cafe + Medialunas", "Cafe americano de origen unico de Misiones + 2 medialunas de manteca recien horneadas. Disponible de lunes a viernes hasta agotar stock. Incluye azucar y leche aparte.", "25.000 Gs", "20.000 Gs", "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop"),
        "Gym Fitness Pro":          ("Membresia Mensual", "Acceso ilimitado a todas las instalaciones: pesas, cardio, spinning, crossfit y clases grupales. Incluye evaluacion fisica inicial y plan de entrenamiento personalizado. Valido 30 dias corridos.", "250.000 Gs", "200.000 Gs", "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=300&fit=crop"),
        "Peluqueria Estilo & Arte": ("Corte + Lavado", "Corte personalizado segun morfologia de rostro + lavado con shampoo y acondicionador profesional + secado y peinado. Duracion: 45 minutos. Incluye diagnostico capilar gratuito.", "80.000 Gs", "60.000 Gs", "https://images.unsplash.com/photo-1560066984-138daaa4e4e1?w=400&h=300&fit=crop"),
        "Instituto EduTech Paraguay":("Curso Python Basico", "Aprende Python desde cero hasta nivel intermedio. 120 horas totales en 3 meses. Horarios: manana 8-12h, tarde 14-18h o noche 18-21h. Incluye material digital, acceso a plataforma online y certificado internacional. Grupos de max 10 alumnos.", "350.000 Gs", "245.000 Gs", "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=300&fit=crop"),
        "Boutique Moda Femenina":   ("Vestido de Verano", "Coleccion nueva temporada, disponible en 8 colores y tallas XS a XXL. Tela liviana 100% algodon. Lavable a maquina. Incluye bolsa de regalo. Cambios y devoluciones en 15 dias.", "180.000 Gs", "120.000 Gs", "https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=400&h=300&fit=crop"),
        "Farmacia San Rafael":      ("Pack Vitaminas C+D", "Vitamina C 1000mg (60 comprimidos efervescentes) + Vitamina D3 2000UI (60 capsulas blandas). Refuerza el sistema inmune y la salud osea. Laboratorio certificado ANMAT. Apto para mayores de 12 anos.", "95.000 Gs", "80.000 Gs", "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=400&h=300&fit=crop"),
        "Club Deportivo Itapua":    ("Inscripcion Anual", "Acceso ilimitado a todas las instalaciones y disciplinas durante 12 meses. Incluye 2 clases grupales semanales, uso de vestuarios y estacionamiento. Valido para 1 persona. Transferible con aviso previo.", "800.000 Gs", "600.000 Gs", "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=300&fit=crop"),
        "Sushi Nikkei Encarnacion": ("Roll Especial Nikkei", "8 piezas de roll con salmon fresco, palta, queso crema y salsa nikkei de la casa. Acompanado de jengibre encurtido, wasabi y salsa de soja. Pescado fresco llegado cada manana. Sin TACC disponible.", "65.000 Gs", "32.500 Gs", "https://images.unsplash.com/photo-1617196034183-421b4040ed20?w=400&h=300&fit=crop"),
        "Libreria Cultural del Sur": ("Pack Escolar Completo", "Kit para el ano escolar: 5 cuadernos universitarios, 1 carpeta 3 anillos, 10 lapiceras bic, 2 resaltadores, regla y compas. Ideal para primaria y secundaria. Stock limitado.", "120.000 Gs", "96.000 Gs", "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop"),
        "Spa & Bienestar Lotus":    ("Masaje Relajante 60min", "Masaje de cuerpo completo con aceites esenciales de lavanda y eucalipto. Tecnica sueca de relajacion profunda. Incluye musica ambiental, aromaterapia y te de hierbas post-sesion. Duracion: 60 minutos en cabina privada.", "200.000 Gs", "140.000 Gs", "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400&h=300&fit=crop"),
        "Veterinaria Patitas Felices":("Consulta + Vacuna", "Consulta clinica general con veterinario + vacuna antirrábica o polivalente segun necesidad. Incluye revision completa, pesaje y recomendaciones nutricionales. Valido para perros y gatos. Turno previo recomendado.", "120.000 Gs", "96.000 Gs", "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop"),
        "Panaderia & Pasteleria La Vienesa":("Torta Personalizada 1kg", "Torta artesanal de 1kg decorada a pedido para cumpleanos o eventos. Sabores: chocolate, vainilla, limon o frutilla. Relleno a eleccion: dulce de leche, crema o mermelada. Pedido con 48hs de anticipacion.", "150.000 Gs", "127.500 Gs", "https://images.unsplash.com/photo-1568254183919-78a4f43a2877?w=400&h=300&fit=crop"),
        "Optica Vision Clara":      ("Armazon + Lentes Antirreflejo", "Armazon de diseno a eleccion (mas de 500 modelos) + lentes oftalmicos con tratamiento antirreflejo y antirayones. Incluye examen visual gratuito. Lentes listos en 24-48 horas. Garantia de 1 ano.", "600.000 Gs", "450.000 Gs", "https://images.unsplash.com/photo-1508296695146-257a814070b4?w=400&h=300&fit=crop"),
        "Academia de Ingles Global":("Mes de Ingles Intensivo", "20 horas de clases grupales (max 8 alumnos) en 1 mes. Horarios a eleccion: manana, tarde o noche. Incluye material digital, acceso a app de practica y 2 sesiones de conversacion con hablante nativo. Nivel a confirmar con prueba de ubicacion.", "250.000 Gs", "150.000 Gs", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400&h=300&fit=crop"),
        "Ferreteria El Constructor":("Taladro Inalambrico Bosch", "Taladro percutor inalambrico Bosch 18V con 2 baterias de litio, cargador rapido y maletín de transporte. Velocidad variable, 2 marchas, mandril 13mm. Garantia oficial 2 anos.", "450.000 Gs", "405.000 Gs", "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&h=300&fit=crop"),
        "Barberia Vintage Cuts":    ("Corte + Barba Completo", "Corte de cabello a eleccion + arreglo y perfilado de barba con navaja + toalla caliente + aceite de barba premium. Duracion: 50 minutos. Incluye lavado y peinado final. Reserva tu turno por WhatsApp.", "70.000 Gs", "56.000 Gs", "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=400&h=300&fit=crop"),
        "Tienda de Bicicletas CyclePy":("Mantenimiento Completo", "Revision integral de la bicicleta: limpieza profunda, lubricacion de cadena, ajuste de frenos y cambios, centrado de ruedas, revision de rodamientos y ajuste general. Tiempo estimado: 2-3 horas. Aplica a cualquier tipo de bicicleta.", "100.000 Gs", "70.000 Gs", "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=400&h=300&fit=crop"),
        "Consultorio Dental Sonrisa":("Limpieza Dental Profesional", "Limpieza dental profunda con ultrasonido + pulido + fluorizacion + revision clinica completa + radiografia panoramica digital incluida. Sin cargo adicional con esta promocion. Turno previo obligatorio.", "180.000 Gs", "0 Gs", "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=400&h=300&fit=crop"),
        "Heladeria Dulce Frio":     ("2x1 Helado Artesanal", "Dos helados de 2 bochas cada uno al precio de uno. Mas de 30 sabores disponibles: cremas, frutales, veganos y sin azucar. Valido sabados y domingos todo el dia. No acumulable con otras promociones.", "20.000 Gs", "10.000 Gs", "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=300&fit=crop"),
    }

    for n in negocios:
        nombre, categoria, imagen, promocion, descuento, direccion, telefono, whatsapp, horario, descripcion, fotos = n
        c.execute("""
            INSERT INTO negocios (nombre, categoria, rating, reviews, imagen, promocion, descuento,
                                  direccion, mapsLink, telefono, whatsapp, horario, descripcion, servicios, fotos)
            VALUES (?, ?, 0, 0, ?, ?, ?, ?, '', ?, ?, ?, ?, '', ?)
        """, (nombre, categoria, imagen, promocion, descuento, direccion, telefono, whatsapp, horario, descripcion, fotos))
        negocio_id = c.lastrowid
        if nombre in ofertas_map:
            on, od, opo, oof, oimg = ofertas_map[nombre]
            c.execute("INSERT INTO ofertas (negocio_id, nombre, descripcion, precio_original, precio_oferta, imagen, orden) VALUES (?, ?, ?, ?, ?, ?, 0)", (negocio_id, on, od, opo, oof, oimg))
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_password_stored):
    return hash_password(password) == hash_password_stored

def generate_credentials(nombre):
    usuario = nombre.lower().replace(' ', '_')[:20]
    usuario = usuario + '_' + ''.join(secrets.choice(string.digits) for _ in range(4))
    characters = string.ascii_letters + string.digits
    contrasena = ''.join(secrets.choice(characters) for _ in range(8))
    return usuario, contrasena

if __name__ == '__main__':
    init_db()
    insertar_negocios_ejemplo()
    print("Base de datos inicializada correctamente")
