import sqlite3

def update_todas_descripciones():
    """Actualizar descripciones para todos los negocios"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    descripciones = {
        'Pizzería Don Giuseppe': """Pizzería Don Giuseppe es un auténtico rincón italiano en el corazón de Encarnación, donde cada pizza es una obra maestra elaborada con técnicas tradicionales napoletanas. Con más de 20 años de experiencia, nos enorgullece ofrecer pizzas horneadas en nuestro horno de leña italiano que alcanza temperaturas perfectas para obtener ese punto crujiente por fuera y suave por dentro. Cada ingrediente es seleccionado cuidadosamente: mozzarella di bufala importada, tomates San Marzano, aceite de oliva extra virgen y otros insumos premium que garantizan autenticidad en cada bocado.

Nuestro menú va más allá de pizzas tradicionales, incluyendo pastas frescas hechas diariamente, risottos cremosos, ensaladas italianas y postres como tiramisú y panna cotta elaborados según recetas familiares transmitidas por generaciones. El ambiente acogedor, con decoración rústica italiana, música ambiente y mesas estratégicamente distribuidas, crea una atmósfera perfecta para disfrutar en familia, parejas o grupos de amigos.

Nuestro equipo de pizzaiolos certificados y personal capacitado se dedica a ofrecerte la mejor experiencia culinaria italiana. Contamos con servicio de delivery, estacionamiento amplio y opciones de vinos importados que complementan perfectamente nuestros platos. Ven a Don Giuseppe y viajaremos juntos a Italia sin salir de Encarnación.""",

        'Café Aroma': """Café Aroma es el destino perfecto para los amantes del café artesanal en Encarnación. Con más de 15 años de experiencia, somos especialistas en la preparación de bebidas de café premium, seleccionando granos de las mejores plantaciones de América Latina y el mundo. Cada taza es preparada por nuestros baristas certificados internacionalmente, siguiendo métodos de extracción perfecta que destacan los sabores únicos y el aroma incomparable de cada variedad de café.

Nuestro ambiente acogedor y elegante, decorado con detalles rústicos que combinan calidez y sofisticación, es ideal para disfrutar en pareja, con amigos o para trabajar en un espacio tranquilo con wifi de alta velocidad. Ofrecemos un menú variado que incluye desde clásicos espresso, cappuccino y americano, hasta bebidas innovadoras creadas exclusivamente por nuestro equipo. Acompañamos cada café con pasteles artesanales, sándwiches gourmet y opciones vegetarianas preparadas con ingredientes frescos.

La música seleccionada cuidadosamente, el aroma inconfundible del café recién molido, y la comodidad de nuestros espacios hacen de Café Aroma tu lugar favorito para relajarte. Nuestro equipo es atento y capacitado, siempre dispuesto a recomendarte la mejor opción según tus preferencias y presupuesto. Abierto todos los días para que disfrutes de un verdadero café de calidad, hecho con pasión y dedicación.""",

        'Gym Fitness Pro': """Gym Fitness Pro es tu aliado integral para lograr tus objetivos de salud y bienestar en Encarnación. Con instalaciones modernas y equipamiento de última generación, ofrecemos un ambiente motivador donde puedes trabajar en tu transformación física. Nuestras máquinas cardiovasculares, pesas libres, equipos de musculación y área funcional están diseñados para satisfacer todos los niveles de entrenamiento, desde principiantes hasta atletas avanzados.

Contamos con un equipo de entrenadores personales certificados internacionalmente, dispuestos a diseñar programas personalizados adaptados a tus objetivos específicos: pérdida de peso, ganancia muscular, acondicionamiento cardiovascular o entrenamiento deportivo. Nuestras clases grupales incluyen yoga, pilates, spinning, zumba y aeróbica coreografiada, todas dirigidas por instructores especialistas que crean un ambiente energético y motivador.

Las instalaciones incluyen duchas modernas con amenities premium, lockers seguros, áreas de descanso cómodo y cafetería saludable con batidos y bebidas proteicas. Ofrecemos membresías flexibles, evaluaciones físicas gratuitas, asesoramiento nutricional y un programa de seguimiento continuo que garantiza resultados reales. Gym Fitness Pro es más que un gimnasio, es una comunidad de personas comprometidas con su bienestar.""",

        'Peluquería Estilo & Arte': """Peluquería Estilo & Arte es tu salón de belleza de confianza en Encarnación, donde la experiencia, el talento y la innovación se unen para transformar tu imagen y aumentar tu autoestima. Nuestro equipo de estilistas certificados combina técnicas tradicionales con tendencias contemporáneas mundiales, personalizando cada servicio según tu tipo de cabello, tono de piel y estilo de vida.

Ofrecemos un amplio catálogo de servicios: cortes modernos y clásicos con técnica profesional, coloración con tintes premium de marcas internacionales reconocidas, tratamientos de keratina lisadora, hidratación profunda, peinados para eventos especiales y tratamientos reparadores para cabellos dañados. También disponemos de servicios de manicure y pedicure con diseños personalizados, uñas de gel, extensiones de cabello natural 100% humano y cuidado integral de la imagen.

El ambiente es tranquilo, acogedor y sofisticado, diseñado para que te sientas cómodo y valorado durante cada visita. Utilizamos productos de calidad premium que respetan la salud del cabello y la piel. Nuestro personal es amable, atento y especializado en escuchar tus necesidades para ofrecerte soluciones personalizadas. En Estilo & Arte, no solo cambias tu cabello, transformas tu confianza.""",

        'Instituto EduTech Paraguay': """Instituto EduTech Paraguay es la plataforma de educación tecnológica más completa en Encarnación, especializada en formar profesionales competentes en programación, desarrollo web, análisis de datos e inteligencia artificial. Con más de 10 años de experiencia educativa, hemos formado miles de estudiantes que hoy trabajan en empresas tecnológicas reconocidas a nivel nacional e internacional.

Nuestros cursos combinan teoría sólida con práctica intensiva mediante proyectos reales que puedes incluir en tu portafolio profesional. Contamos con instructores con experiencia laboral en grandes empresas tech, certificados internacionalmente y apasionados por enseñar. Ofrecemos programas flexibles: cursos modularizados, bootcamps intensivos, mentorías personalizadas y diplomados especializados en Python, JavaScript, React, Data Science y Cloud Computing.

Todas nuestras certificaciones son reconocidas por la industria y aumentan significativamente tus oportunidades laborales. Disponemos de aulas modernas equipadas con computadoras de alto rendimiento, acceso 24/7 a plataformas de aprendizaje online, biblioteca digital con recursos educativos y comunidad activa de estudiantes. Ofrecemos becas parciales, planes de pago flexibles y garantía de satisfacción. En EduTech, invertimos en tu futuro profesional.""",

        'Boutique Moda Femenina': """Boutique Moda Femenina es tu destino exclusivo para ropa y accesorios de moda contemporánea en Encarnación. Especializados en propuestas femeninas que combinan elegancia, comodidad y tendencia, ofrecemos prendas cuidadosamente seleccionadas de diseñadores reconocidos y marcas premium de calidad garantizada. Cada prenda en nuestro boutique es elegida considerando estilo, durabilidad y el confort que mereces.

Nuestro catálogo incluye vestidos sofisticados para eventos especiales, blusas versátiles para la oficina, jeans de calidad, prendas casuales cómodas, abrigos elegantes y accesorios que complementan cualquier look. Contamos con tallas inclusivas que van desde XS hasta XL, asegurando que todas las mujeres encuentren opciones que las hagan sentir hermosas y seguras.

Las asesoras de estilo de nuestro boutique están capacitadas para ofrecerte recomendaciones personalizadas basadas en tu tipo de cuerpo, gustos y presupuesto. Ofrecemos servicio de probador cómodo, ajustes gratuitos, devoluciones sin inconvenientes y programa de fidelización con descuentos exclusivos. El ambiente es elegante y acogedor, perfecto para explorar nuevas propuestas de moda. En nuestra boutique, encontrarás ropa que refleja tu personalidad.""",

        'Farmacia San Rafael': """Farmacia San Rafael es tu aliada de confianza para el cuidado de la salud de tu familia en Encarnación. Con más de 25 años de trayectoria, somos una farmacia integral que ofrece medicamentos con receta, productos de venta libre, suplementos vitamínicos, productos de higiene personal, cosméticos y equipos médicos certificados.

Contamos con farmacéuticos especializados disponibles para ofrecerte consultas sin costo, recomendaciones sobre medicamentos, información sobre efectos secundarios y posibles interacciones farmacológicas. Además, disponemos de servicio de entrega a domicilio, un programa de descuentos para clientes frecuentes, y refrigeración especial para medicamentos que lo requieren. Ofrecemos marcas reconocidas y productos genéricos de igual calidad a precios accesibles.

Nuestro local es moderno, bien iluminado y organizado para facilitar tu búsqueda de productos. Contamos con estacionamiento seguro, atención amable y eficiente, y horarios extendidos para tu conveniencia. En Farmacia San Rafael, nos importa tu bienestar y el de tu familia con atención profesional y responsable.""",

        'Club Deportivo Itapúa': """Club Deportivo Itapúa es mucho más que un club, es un espacio integral de entretenimiento, deportes y convivencia familiar en Encarnación. Con instalaciones modernas y amplias, ofrecemos canchas de fútbol profesionales, cancha de tennis, áreas de swimming pool climatizada, salón de eventos y amplios espacios verdes para diversas actividades deportivas y recreativas.

Disponemos de programas para todas las edades: escuelas de fútbol con entrenadores certificados, clases de natación desde bebés hasta adultos, entrenamientos de tennis, yoga, pilates y actividades para niños como actividades acuáticas divertidas. Contamos con equipamiento deportivo de calidad, vestuarios modernos, cafetería, áreas de descanso y personal de seguridad capacitado disponible durante todo el funcionamiento del club.

El ambiente es seguro, familiar y motivador, ideal para disfrutar del deporte, mejorar tu condición física y compartir momentos valiosos con la familia. Ofrecemos membresías flexibles con diferentes opciones según tus necesidades e intereses. En Itapúa, practicar deporte es más que entrenamiento, es un estilo de vida saludable.""",

        'Sushi Nikkei Encarnación': """Sushi Nikkei Encarnación es un restaurante japonés especializado que combina la autenticidad de la cocina japonesa tradicional con toques contemporáneos en Encarnación. Nuestro chef japonés certificado y su equipo ofrecen una experiencia culinaria excepcional preparando sushi fresco diariamente con pescado seleccionado cuidadosamente, asegurando máxima frescura y calidad.

Nuestro menú incluye rolls variados con materias primas premium, nigiri sashimi de diferentes tipos de pescado, sopas miso auténticas, fideos udon, ramen artesanal, tempura crujiente y postres japoneses tradicionales. Disponemos de sake premium importado de Japón y bebidas complementarias que elevan la experiencia culinaria. Cada plato es preparado con técnica precisa y presentado de forma artística, respetando la filosofía estética japonesa.

El ambiente es minimalista y elegante, con decoración auténtica que transporta al cliente a Japón. Contamos con bar sushi, mesas comodonas, salones privados para eventos especiales y personal bilingüe capacitado. Ofrecemos servicio de delivery con empaquetamiento especial que mantiene la frescura. En Sushi Nikkei, disfrutas de un viaje gastronómico a Japón sin salir de Encarnación.""",

        'Librería Cultural del Sur': """Librería Cultural del Sur es un espacio dedicado al conocimiento, la imaginación y la cultura en Encarnación. Con una amplia selección de más de 10,000 títulos, somos el destino favorito de lectores, estudiantes, intelectuales y amantes de los libros que buscan desde bestsellers internacionales hasta obras clásicas y literatura independiente.

Nuestro inventario incluye libros de ficción, no-ficción, educación, autoayuda, infantiles, arte, historia, filosofía y títulos en varios idiomas (español, inglés, portugués). Contamos con seción de libros usados a precios accesibles, revistas especializadas, material escolar de calidad y regalos literarios únicos. Organizamos presentaciones de autores, clubes de lectura mensuales, talleres de escritura creativa y eventos culturales que enriquecen la comunidad.

El espacio es acogedor con sofás cómodos, área de café donde puedes disfrutar mientras lees, wifi gratis y servicio de atención personalizada. Nuestro personal son lectores apasionados dispuestos a recomendarte títulos según tus intereses. En Librería Cultural del Sur, cada visita es un encuentro con nuevas historias y conocimiento.""",

        'Spa & Bienestar Lotus': """Spa & Bienestar Lotus es un santuario de relajación y rejuvenecimiento en Encarnación, diseñado para ofrecerte la máxima experiencia de bienestar integral. Con instalaciones lujosas y personal especializado, nos dedicamos a restaurar tu balance físico y emocional mediante terapias holísticas, masajes relajantes y tratamientos de belleza premium.

Ofrecemos masajes tailandeses tradicionales, masajes sueco de relajación, masajes terapéuticos para dolor y tensión muscular, reflexología, y tratamientos especializados con piedras calientes y aceites aromáticos. Además, disponemos de faciales anti-edad con productos suizos de lujo, envolturas corporales reparadoras, peeling profesionales, tratamientos corporales reafirmantes y servicios de belleza integral. Las salas de sauna infrarrojo, jacuzzi y areas de meditación complementan la experiencia completa de bienestar.

Todo se realiza en un ambiente sereno con aromaterapia, música relajante y atención personalizada de terapeutas certificados. Ofrecemos paquetes wellness personalizados, tratamientos para parejas, y una filosofía que considera el cuerpo y la mente como un sistema integral. En Lotus, el bienestar es un viaje de transformación y paz.""",

        'Veterinaria Patitas Felices': """Veterinaria Patitas Felices es el centro integral de cuidado para la salud y el bienestar de tus mascotas en Encarnación. Contamos con veterinarios especializados certificados y equipamiento médico moderno para ofrecerte servicios profesionales de atención veterinaria completa.

Ofrecemos consultas clínicas, diagnóstico por laboratorio, radiografías digitales, cirugías menores y mayores, servicios reproductivos, odontología veterinaria, peluquería y grooming profesional. Disponemos de servicios de internación con monitoreo continuo, farmacoterapia especializada, y asesoramiento en nutrición animal. Nuestro personal ama a los animales y se dedica a proporcionar atención compasiva y de calidad.

Las instalaciones incluyen sala de espera cómoda, quirófanos asépticos, laboratorio equipado, y area de internación con clima controlado. Realizamos chequeos preventivos, inmunizaciones, desparasitaciones y promocionamos la medicina preventiva para una vida larga y saludable de tus mascotas. En Patitas Felices, tu mascota es familia.""",

        'Panadería & Pastelería La Vienesa': """Panadería & Pastelería La Vienesa es la mejor opción para pan artesanal y productos de pastelería en Encarnación. Con recetas transmitidas por más de 30 años, elaboramos diariamente pan fresco, medialunas crocantes, facturas variadas y productos de pastelería utilizando ingredientes de calidad premium.

Ofrecemos pan integral saludable, pan francés crujiente, pan de molde suave, pan sin TACC para celíacos, y variedades especiales como pan con semillas y pan de cereales. Nuestras pastas de hojaldre son crujientes y derretibles en boca, disponibles en variedades dulces y saladas. Elaboramos tortas personalizadas para eventos especiales, cupcakes decorados, tartas innovadoras y postres de pastelería fina.

Todos nuestros productos usan conservantes naturales y elaboración artesanal, sin aditivos innecesarios. El local es limpio, moderno y cuenta con vitrina expositor atractiva. Ofrecemos servicio de pedidos por encargo, entregas a domicilio y programa de catering para eventos. En La Vienesa, cada producto es hecho con amor y dedicación.""",

        'Óptica Visión Clara': """Óptica Visión Clara es tu centro especializado en cuidado de la visión y óptica en Encarnación. Contamos con optometristas certificados que realizan evaluaciones visuales completas, determinación de graduación exacta y recomendaciones personalizadas de soluciones visuales.

Ofrecemos un amplio catálogo de armazones de marcas reconocidas internacionalmente (Ray-Ban, Gucci, Prada, Oakley), lentes de última generación con tecnologías avanzadas (progresivos, antirreflexo, filtro azul, fotocromáticos), lentes de contacto de diferentes tipos y soluciones de cuidado. Disponemos de servicios de ajuste y reparación, limpieza ultrasónica gratis, y seguimiento visual periódico.

Nuestro local cuenta con ambiente moderno, iluminación profesional para pruebas visuales, y personal capacitado en asesor técnico. Realizamos pruebas visuales detalladas, test de daltonismo y evaluación de presión ocular. Ofrecemos financiamiento flexible para tus gafas. En Visión Clara, cuidamos tus ojos con profesionalismo.""",

        'Academia de Inglés Global': """Academia de Inglés Global es la institución educativa especializada en enseñanza de inglés de calidad en Encarnación. Con más de 12 años de experiencia, hemos preparado a cientos de estudiantes para certificaciones internacionales y para comunicarse fluídamente en inglés.

Ofrecemos programas estructurados según niveles (desde principiantes absolutos hasta advanced), cursos especializados (inglés empresarial, técnico, conversacional) y preparación para exámenes internacionales (TOEFL, IELTS, Cambridge). Nuestros profesores son nativos o certificados en enseñanza del idioma, utilizando metodologías modernas y materiales actualizados que hacen el aprendizaje dinámico y efectivo.

Las clases son en grupos reducidos o personalizadas asegurando atención individualizada. Disponemos de laboratorio de idiomas, biblioteca con recursos audiovisuales, y plataforma online complementaria para refuerzo en casa. Realizamos evaluaciones periódicas, simulacros de exámenes y seguimiento del progreso. En Global, el inglés es tu puerta al mundo.""",

        'Ferretería El Constructor': """Ferretería El Constructor es tu aliado confiable para todos tus proyectos de construcción, reparación y mantenimiento en Encarnación. Con más de 20 años en el rubro, ofrecemos una amplia gama de productos de ferretería, materialidades de construcción y herramientas para profesionales, constructores y aficionados.

Disponemos de materiales básicos (ladrillos, cemento, arena), productos eléctricos certificados, tuberías PVC y cobre, herrajes de calidad, pinturas y barnices de marcas reconocidas, herramientas manuales y eléctricas profesionales, y equipamiento de seguridad. Nuestro inventario es amplio y actualizado con las últimas innovaciones del mercado. Contamos con personal capacitado que puede asesorarte en selección de materiales y presupuestos.

El local es amplio, bien organizado y cuenta con estacionamiento conveniente. Ofrecemos servicio de entrega a domicilio, cotizaciones sin cargo, y asesoramiento técnico profesional. Disponemos de promociones y descuentos especiales para obras grandes. En El Constructor, tus proyectos salen adelante con confianza.""",

        'Barbería Vintage Cuts': """Barbería Vintage Cuts es un espacio dedicado al arte del barbering clásico con un toque contemporáneo en Encarnación. Especializados en cortes de caballero realizados con técnica de navaja, ofrecemos la experiencia auténtica de la barbería tradicional combinada con conocimiento de tendencias modernas.

Nuestros barberos certificados ofrecen cortes precisos, afeitados clásicos de navaja con espuma caliente, diseños de barba profesionales, perfilado de líneas nítidas y tratamientos capilares especializados para hombre. Disponemos de productos premium para el cuidado facial y capilar, incluyendo aceites corporales, bálsamos y lociones aftershave de calidad superior. El ambiente es masculino, acogedor y relajante, con sillones cómodos y entretenimiento.

Nuestro espacio une la tradición barbera con tecnología moderna. Ofrecemos servicios de barba, cortes de niños y servicios de grooming integral. En Vintage Cuts, el barbering es un arte en cada corte.""",

        'Tienda de Bicicletas CyclePy': """Tienda de Bicicletas CyclePy es el referente en bicicletas, accesorios y equipamiento para el ciclismo en Encarnación. Contamos con amplio catálogo de bicicletas de todas las marcas reconocidas: bicicletas de ruta, montaña, urbanas, indoor y especializadas para competencia.

Ofrecemos asistencia profesional en selección de la bicicleta adecuada según tu nivel y necesidades. Disponemos de servicio técnico completo: reparación, ajuste, mantenimiento preventivo y cambio de piezas. Contamos con accesorios esenciales: cascos de seguridad, luces, candados, mochilas, equipamiento deportivo técnico y prendas ciclísticas de calidad. Realizamos talleres educativos sobre mantenimiento básico y seguridad en ruta.

Nuestro personal son ciclistas apasionados dispuestos a compartir experiencia y recomendaciones. El local es moderno con display atractivo de bicicletas. Ofrecemos financiamiento flexible y programas de cambio de bicicletas viejas. En CyclePy, encontrarás todo para disfrutar el ciclismo seguro.""",

        'Consultorio Dental Sonrisa': """Consultorio Dental Sonrisa es tu centro odontológico integral en Encarnación, dedicado a la salud y estética dental con enfoque en atención de calidad y comodidad del paciente. Contamos con dentistas especializados en diferentes disciplinas: odontología general, periodoncia, ortodoncia, endodoncia y odontología estética.

Ofrecemos tratamientos desde limpiezas preventivas profesionales, tratamientos de caries, hasta procedimientos complejos como implantes dentales, puentes, coronas de cerámica y blanqueamiento dental profesional. Disponemos de tecnología moderna: radiografías digitales (menor radiación), cámara intraoral, sistemas de anestesia avanzada para mayor comodidad, y equipamiento de desinfección de alta estandar.

El ambiente es amigable, moderno y acogedor, diseñado para reducir ansiedad. Los dentistas explican cada procedimiento, ofrecen opciones de tratamiento y realizan seguimiento periódico. Contamos con programa de educación en higiene oral, presupuestos transparentes y planes de pago flexibles. En Sonrisa, tu salud dental es nuestra prioridad.""",
    }
    
    # Actualizar cada negocio con su descripción
    for nombre, descripcion in descripciones.items():
        c.execute('''
            UPDATE negocios 
            SET descripcion = ?
            WHERE nombre = ?
        ''', (descripcion, nombre))
    
    conn.commit()
    
    # Resumen
    c.execute('SELECT COUNT(*) FROM negocios')
    total = c.fetchone()[0]
    
    print(f"✓ {len(descripciones)} descripciones actualizadas")
    print(f"Total de negocios en BD: {total}")
    print("\nNegocios actualizados:")
    for nombre in descripciones.keys():
        print(f"  • {nombre}")
    
    conn.close()

if __name__ == '__main__':
    update_todas_descripciones()
