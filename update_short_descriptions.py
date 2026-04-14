import sqlite3

def update_short_descriptions():
    """Acortar descripciones a 2-3 párrafos máximo"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    descripciones = {
        'Pizzería Don Giuseppe': """Pizzería Don Giuseppe es un auténtico rincón italiano en el corazón de Encarnación. Con más de 20 años de experiencia, ofrecemos pizzas horneadas en nuestro horno de leña italiano con ingredientes premium: mozzarella di bufala, tomates San Marzano y aceite de oliva extra virgen. Complementamos nuestro menú con pastas frescas hechas diariamente, risottos cremosos y postres italianos. El ambiente acogedor con decoración rústica italiana es perfecto para disfrutar en familia o reuniones.""",

        'Café Aroma': """Café Aroma es el destino perfecto para los amantes del café artesanal en Encarnación. Con 15 años de experiencia, nuestros baristas certificados preparan café premium seleccionado de las mejores plantaciones. Ofrecemos espresso, cappuccino, bebidas innovadoras y pasteles artesanales en un ambiente acogedor con wifi gratis. El aroma del café recién molido y la música seleccionada hacen de Café Aroma tu lugar favorito para relajarte.""",

        'Gym Fitness Pro': """Gym Fitness Pro es tu aliado integral para alcanzar tus objetivos de salud con instalaciones modernas, equipamiento de última generación y entrenadores personales certificados. Ofrecemos clases grupales variadas (yoga, pilates, spinning, zumba), máquinas cardiovasculares, pesas libres y áreas funcionales. El ambiente motivador, las duchas modernas con amenities y la cafetería saludable complementan tu experiencia de bienestar integral.""",

        'Peluquería Estilo & Arte': """Peluquería Estilo & Arte cuenta con estilistas certificados que combinan técnicas tradicionales con tendencias modernas. Ofrecemos cortes profesionales, coloración con tintes premium, tratamientos de keratina, manicure, pedicure y extensiones de cabello natural. El ambiente sofisticado, los productos de calidad premium y nuestro equipo especializado garantizan que salgas con la imagen transformada que deseas.""",

        'Instituto EduTech Paraguay': """Instituto EduTech Paraguay es la plataforma educativa especializada en programación, desarrollo web, data science e inteligencia artificial. Con 10 años de experiencia, ofrecemos cursos modularizados, bootcamps intensivos y mentorías personalizadas con instructores certificados de grandes empresas tech. Todas nuestras certificaciones son reconocidas en la industria, con aulas modernas, acceso 24/7 a plataformas online y planes de pago flexibles.""",

        'Boutique Moda Femenina': """Boutique Moda Femenina ofrece ropa y accesorios de moda contemporánea seleccionados cuidadosamente de diseñadores reconocidos. Con prendas que combinan elegancia, comodidad y tendencia en tallas inclusivas (XS a XL), nuestras asesoras de estilo ofrecen recomendaciones personalizadas. Disponemos de probadores cómodos, ajustes gratuitos y un ambiente elegante perfecto para explorar tu estilo.""",

        'Farmacia San Rafael': """Farmacia San Rafael es tu aliada de confianza con 25 años en el cuidado de la salud familiar. Ofrecemos medicamentos con receta, productos de venta libre, suplementos vitamínicos y equipos médicos certificados, con farmacéuticos disponibles para consultas sin costo. Servicio de entrega a domicilio, programa de descuentos y horarios extendidos garantizan tu conveniencia.""",

        'Club Deportivo Itapúa': """Club Deportivo Itapúa es un espacio integral de entretenimiento y deportes con canchas de fútbol profesionales, cancha de tenis, piscina climatizada y salones de eventos. Ofrecemos escuelas de fútbol con entrenadores certificados, clases de natación, yoga, pilates y actividades para todas las edades. Las instalaciones seguras, modernas y el ambiente familiar hacen del club tu destino de bienestar.""",

        'Sushi Nikkei Encarnación': """Sushi Nikkei prepara sushi fresco diariamente con chef japonés certificado y pescado seleccionado cuidadosamente. Ofrecemos rolls variados, nigiri sashimi premium, ramen artesanal, tempura crujiente y postres japoneses. El ambiente minimalista y elegante, con bar sushi y servicio de delivery especializado, transporta la experiencia culinaria auténtica de Japón a Encarnación.""",

        'Librería Cultural del Sur': """Librería Cultural del Sur ofrece más de 10,000 títulos de ficción, no-ficción, educación y literatura en varios idiomas. Además de libros, disponemos de material escolar, revistas especializadas y regalos literarios. El ambiente acogedor con sofás, área de café, wifi gratis y personal apasionado por la lectura hacen cada visita un encuentro con nuevas historias.""",

        'Spa & Bienestar Lotus': """Spa & Bienestar Lotus es tu santuario de relajación con masajes tailandeses, faciales anti-edad con productos suizos premium, envolturas corporales y sauna infrarrojo. Las salas diseñadas con aromaterapia, música relajante y terapeutas certificados ofrecen experiencias personalizadas. Disponemos de paquetes wellness y áreas de meditación para una transformación integral de bienestar.""",

        'Veterinaria Patitas Felices': """Veterinaria Patitas Felices ofrece atención veterinaria integral con veterinarios especializados certificados. Servicios incluyen consultas clínicas, laboratorio, radiografías digitales, cirugías, odontología veterinaria, grooming profesional y peluquería. Las instalaciones modernas con quirófanos asépticos y área de internación con clima controlado garantizan el mejor cuidado para tus mascotas.""",

        'Panadería & Pastelería La Vienesa': """Panadería & Pastelería La Vienesa elabora diariamente pan artesanal fresco, medialunas crocantes, facturas variadas y productos de pastelería con recetas de 30 años. Ofrecemos pan integral saludable, opciones sin TACC, pastas de hojaldre derretibles y tortas personalizadas para eventos. Todos nuestros productos usan ingredientes de calidad premium sin aditivos innecesarios.""",

        'Óptica Visión Clara': """Óptica Visión Clara cuenta con optometristas certificados que realizan evaluaciones visuales completas. Ofrecemos amplio catálogo de armazones de marcas reconocidas (Ray-Ban, Gucci, Prada), lentes de última generación (progresivos, antirreflexo, filtro azul) y lentes de contacto. Disponemos de servicio de ajuste, reparación, limpieza ultrasónica gratis y seguimiento visual periódico.""",

        'Academia de Inglés Global': """Academia de Inglés Global con 12 años de experiencia ha preparado cientos de estudiantes para certificaciones internacionales. Ofrecemos cursos por niveles, inglés empresarial, preparación TOEFL/IELTS/Cambridge, con docentes nativos certificados. Clases en grupos reducidos, laboratorio de idiomas, biblioteca digital y plataforma online garantizan aprendizaje efectivo y certificaciones reconocidas.""",

        'Ferretería El Constructor': """Ferretería El Constructor con 20 años en el rubro ofrece materialidades de construcción, herramientas profesionales, productos eléctricos certificados, pinturas y herrajes de calidad. Personal capacitado ofrece asesoramiento técnico y presupuestos sin cargo. Disponemos de servicio de entrega a domicilio, promociones para obras grandes y amplio inventario actualizado.""",

        'Barbería Vintage Cuts': """Barbería Vintage Cuts especializada en el arte del barbering clásico ofrece cortes precisos con técnica de navaja, afeitados clásicos con espuma caliente y diseño de barba profesional. Barberos certificados, productos premium para cuidado facial, ambiente masculino acogedor y entretenimiento completan la experiencia auténtica de barbería tradicional.""",

        'Tienda de Bicicletas CyclePy': """Tienda de Bicicletas CyclePy ofrece amplio catálogo de bicicletas de todas las marcas reconocidas (ruta, montaña, urbanas, indoor). Disponemos de servicio técnico completo (reparación, ajuste, mantenimiento), accesorios esenciales, equipamiento deportivo y prendas técnicas. Personal ciclista apasionado brinda recomendaciones especializadas y talleres educativos sobre mantenimiento y seguridad.""",

        'Consultorio Dental Sonrisa': """Consultorio Dental Sonrisa cuenta con dentistas especializados en odontología general, periodoncia, ortodoncia, endodoncia y estética dental. Ofrecemos limpiezas preventivas, tratamientos de caries, implantes dentales, blanqueamiento profesional con tecnología moderna y radiografías digitales. El ambiente amigable diseñado para reducir ansiedad, presupuestos transparentes y planes de pago flexibles garantizan tu comodidad.""",
    }
    
    # Actualizar cada negocio
    for nombre, descripcion in descripciones.items():
        c.execute('''
            UPDATE negocios 
            SET descripcion = ?
            WHERE nombre = ?
        ''', (descripcion, nombre))
    
    conn.commit()
    
    print(f"✓ {len(descripciones)} descripciones acortadas correctamente")
    
    conn.close()

if __name__ == '__main__':
    update_short_descriptions()
