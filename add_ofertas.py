import sqlite3
import random
from datetime import datetime, timedelta

def add_ofertas():
    """Agregar ofertas y productos con imágenes a todos los negocios"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    def convertir_precio(precio_str):
        """Convierte precio de dólares a guaraníes: $X.XX -> X.000 Gs (aprox)"""
        try:
            # Extrae el número del string ($3.50 -> 3.50)
            valor = float(precio_str.replace('$', '').strip())
            # Convierte a guaraníes (aprox 1 USD = 7000 Gs)
            valor_gs = int(valor * 7000)
            # Formatea con separador de miles: 24500 -> 24.500
            return f"{valor_gs:,}".replace(",", ".") + " Gs"
        except:
            return precio_str
    
    # Obtener todos los negocios
    c.execute('SELECT id, nombre, categoria FROM negocios ORDER BY id')
    negocios = c.fetchall()
    
    ofertas_por_negocio = {
        1: [  # Café Aroma Gourmet
            ('Café Espresso Premium', 'Espresso preparado con granos seleccionados de las mejores plantaciones de América Latina, extraído con máquina profesional italiana a presión perfecta. Intenso, aromático y con cuerpo robusto. Servido inmediatamente para preservar toda su esencia y aroma. Ideal para comenzar el día con energía.',
             '$3.50', '$1.50', 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop'),
            ('Cappuccino Artesanal', 'Combinación perfecta de espresso doble con leche vaporizada sedosa y espuma decorada con arte latte. Preparado por baristas certificados con técnica italiana tradicional. El equilibrio perfecto entre café y leche, con aroma inconfundible y textura aterciopelada.',
             '$4.50', '$2.50', 'https://images.unsplash.com/photo-1517668808822-9ebb02ae2a0e?w=400&h=300&fit=crop'),
            ('Pastel de Chocolate', 'Torta casera elaborada diariamente con chocolate belga 70% de cacao, mantequilla europea y huevos frescos. Cubierta con ganache de chocolate oscuro y decoración artesanal. Esponjosa por dentro, cremosa y con intenso sabor a chocolate puro. Acompaña perfectamente con café.',
             '$6.00', '$3.00', 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop'),
        ],
        2: [  # Cappuccino Express
            ('Americano Double Shot', 'Café americano potente preparado con dos shots de espresso de grano premium, diluido en agua caliente filtrada para mantener el aroma y cuerpo. Intenso, robusto y perfecto para quienes aman el café fuerte. Bebida clásica que nunca falla.',
             '$3.00', '$1.50', 'https://images.unsplash.com/photo-1447933608880-8c8fe0f4c25c?w=400&h=300&fit=crop'),
            ('Latte Macchiato', 'Leche vaporizada suave con espresso marcado en forma diferenciada. Tres capas de sabor: espuma sedosa, leche cremosa y café intenso. Textura aterciopelada gracias a la técnica profesional de vaporización. Bebida elegante para disfrutar cada sorbo.',
             '$4.00', '$2.00', 'https://images.unsplash.com/photo-1459023058943-07fcbe16d735?w=400&h=300&fit=crop'),
            ('Croissant Francés', 'Croissant auténtico francés elaborado con masa folclórica tradicional y mantequilla pura importada de Francia. Horneado diariamente hasta lograr capas crocantes por fuera y suave por dentro. Aroma de mantequilla que invade cada bocado. Acompaña perfectamente con café.',
             '$2.50', '$1.25', 'https://images.unsplash.com/photo-1585080876519-c21cc028cb0d?w=400&h=300&fit=crop'),
        ],
        3: [  # Restaurante El Sabor Mexicano
            ('Enchiladas Verdes', 'Enchiladas preparadas con tortillas de maíz suave rellenas de pollo desmenuzado tierno, cubiertas con salsa verde casera elaborada diariamente con tomatillos frescos, cilantro y chiles. Gratinadas con queso Oaxaca fundido. Servidas con crema agria y arroz de acompañamiento.',
             '$12.00', '$6.00', 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&h=300&fit=crop'),
            ('Ceviche Mixto', 'Ceviche fresco del día con camarones jumbo naturales y filete de pez blanco, marinado en limón fresco ácido perfecto. Complementado con cebolla morada, cilantro, tomate y aguacate. Afinador con toque de ají rojo. Servido con tortilla tostada casera. Explosión de sabores marinos.',
             '$14.00', '$7.00', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop'),
            ('Molcajete Especial', 'Molcajete volcánico tradicional con carnitas de cerdo tiernas, chorizo especiado, queso Oaxaca, y rajas poblanas. Servido caliente y humeante directamente del comal. Acompañado con arepa casera y salsa pico de gallo. Experiencia gastronómica auténtica mexicana.',
             '$18.00', '$9.00', 'https://images.unsplash.com/photo-1571407970349-bc81e7834525?w=400&h=300&fit=crop'),
            ('Quesadillas de Flor de Calabaza', 'Quesadillas rellenas generosamente de flor de calabaza tierna, queso Oaxaca derretido, rajas poblanas y epazote. Cocinadas en comal tradicional hasta que se tuesten levemente. Servidas con crema agria, salsa verde y cebolla morada. Delicia vegetariana tradicional.',
             '$10.00', '$5.00', 'https://images.unsplash.com/photo-1565055895-c2bea5e601b6?w=400&h=300&fit=crop'),
        ],
        4: [  # Pizzería Napoli Auténtica
            ('Pizza Margherita', 'Pizza italiana tradicional con masa fermentada 48 horas, cubierta con salsa de tomate San Marzano, mozzarella di bufala fresca, albahaca fresca y aceite de oliva extra virgen. Horneada en horno de leña a 300°C. Crujiente, ligera y auténtica desde Nápoles.',
             '$16.00', '$8.00', 'https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=400&h=300&fit=crop'),
            ('Pizza Quattro Formaggi', 'Pizza premium con cuatro quesos italianos: mozzarella, gorgonzola, provolone y parmesano. Masa artesanal crujiente en los bordes, suave en el centro. Horneada en horno de leña que resalta los sabores únicos de cada queso. Mezcla armoniosa de sabores cremosos y intensos.',
             '$18.00', '$9.00', 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&h=300&fit=crop'),
            ('Pasta Carbonara', 'Pasta italiana fresca hecha diariamente con salsa carbonara auténtica romana: yemas de huevo, guanciale italiano, pecorino romano y pimienta negra. Sin crema, sin nata. Técnica tradicional que crea salsa sedosa. Manjar italiano clásico que requiere precisión en su preparación.',
             '$14.00', '$7.00', 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400&h=300&fit=crop'),
            ('Tiramisú', 'Postre italiano clásico elaborado con bizcochos savoiardi mojados en café espresso fuerte, capas de mascarpone cremoso azucarado, y capas de cacao en polvo. Refrigerado 4 horas para que los sabores se unifiquen. Postre elegante, cremoso y con sabor a café intenso.',
             '$6.00', '$3.00', 'https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=400&h=300&fit=crop'),
        ],
        5: [  # Steakhouse Prime Cuts
            ('Carne Wagyu 300g', 'Corte prime de carne Wagyu auténtica con marmolado excepcional, importada directamente de Japón. 300 gramos de carne de la máxima calidad, selecta por su infiltración de grasa y ternura incomparable. Cocinada a punto perfecto. Experiencia gastronómica de lujo.',
             '$65.00', '$32.50', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop'),
            ('Filete Mignon', 'Corte premium de 400 gramos de lomo de carne certificada, seleccionado por su ternura extrema. Cocinado a punto perfecto y cubierto con salsa béarnaise casera elaborada con mantequilla, vino blanco y yema de huevo. Acompañado con papa gratinada y vegetales de estación.',
             '$55.00', '$27.50', 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop'),
            ('Costillas BBQ', 'Costillas ahumadas lentamente durante 6 horas en ahumador de madera de nogal. Carne tierna que se despega del hueso, cubierta con salsa BBQ casera de receta secreta con toque de miel y especias. Acompañadas con papas rusticas y ensalada coleslaw fresca.',
             '$48.00', '$24.00', 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop'),
            ('Botella Vino Reserva', 'Vino tinto premium Cabernet Sauvignon cosecha reserva de bodega reconocida mundialmente. Envejeci en barril de roble francés por 18 meses. Cuerpo robusto con notas de ciruela y especias. Ideal para acompañar carnes de calidad superior.',
             '$120.00', '$60.00', 'https://images.unsplash.com/photo-1510812431401-41d2cab2707d?w=400&h=300&fit=crop'),
        ],
        6: [  # Sushi Paradise
            ('Rolls Surtido', 'Combinación variada de 12 piezas de distintos rolls: California, Filadelfia, Tempura, Dragón y Arcoíris. Cada rol preparado con arroz sushi de grano corto sazonado perfectamente, pescado fresco de primera calidad y ingredientes premium. Acompañado con salsa de soja, wasabi y jengibre encurtido.',
             '$24.00', '$12.00', 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop'),
            ('Nigiri Sashimi Premium', '15 piezas de sashimi fresco premium cortadas con precisión de cuchillo profesional. Selección de salmón Atlántico, atún rojo, pulpo, camarones y pez blanco. Preparadas por chef sushi certificado. Ensalada de alga wakame, salsa ponzu y jengibre. Experiencia de sabor puro.',
             '$32.00', '$16.00', 'https://images.unsplash.com/photo-1553881081-0ac4dd95895e?w=400&h=300&fit=crop'),
            ('Maki Tempura', 'Rolls crujientes con camarón tempura rebozado en masa ligera y crujiente, acompañado de aguacate, pepino y mayonesa casera. Rollos cubiertos con semilla de sésamo tostado. Contraste perfecto entre lo crujiente y lo suave. Combinación de sabores y texturas irresistible.',
             '$18.00', '$9.00', 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop'),
            ('Edamame', 'Edamame (porotos de soja) cocidos al vapor con perfección, sazonados con sal marina gourmet. Acompañado con salsa de soja suave. Aperitivo saludable, proteico y refrescante. Ideal para comenzar la experiencia culinaria o mientras espera su orden principal.',
             '$8.00', '$4.00', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop'),
        ],
        7: [  # Gym Fitness Pro Elite
            ('Membresía Gold 1 mes', 'Acceso ilimitado a todas las clases: aeróbica, yoga, pilates, zumba y spinning. Uso de todas las máquinas de última generación, pesas libres y área de funcional. Entrenador disponible para orientación. Duchas con amenities, estacionamiento incluido. Plan de iniciación personalizado.',
             '$120.00', '$60.00', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=300&fit=crop'),
            ('Sesión Personal Trainer', 'Sesión de entrenamiento personalizado de una hora completa con entrenador certificado. Plan adaptado a tus objetivos específicos: pérdida de peso, ganancia muscular o acondicionamiento. Evaluación postural, programa individualizado y seguimiento continuo. Transformación corporalguarantizada.',
             '$80.00', '$40.00', 'https://images.unsplash.com/photo-1552961519-fbf46af7925d?w=400&h=300&fit=crop'),
            ('Clase Yoga Premium', 'Clase de yoga avanzada con instructor certificado en filosofía y técnicas tradicionales. Sesión de 60 minutos de relajación, flexibilidad y fortalecimiento. Incluye meditación inicial, asanas progresivas y savasana final. Apto para niveles intermedios y avanzados. Equilibrio cuerpo y mente.',
             '$30.00', '$15.00', 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400&h=300&fit=crop'),
            ('Pack Proteína Whey', 'Proteína whey 2kg de marca premium importada directamente de Estados Unidos. Sabor vainilla o chocolate, origen de concentrado de suero de leche puro, 25g de proteína por porción. Mezcla rápida, sin grumos. Complemento ideal post-entrenamiento para recuperación muscular.',
             '$75.00', '$37.50', 'https://images.unsplash.com/photo-1587014638746-410236b93c43?w=400&h=300&fit=crop'),
        ],
        8: [  # CrossFit Max
            ('Membresía CrossFit 1 mes', 'Acceso ilimitado a todos los WODs (Workout of the Day) programados diariamente. Clases grupales de CrossFit con coaching directo de atletas certificados. Programación varied, escalable para todos los niveles. Comunidad motivadora y desafiante. Acceso a salas de peso, cardio y funcional moderno.',
             '$150.00', '$75.00', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=300&fit=crop'),
            ('Coaching personalizado', 'Plan de entrenamiento personalizado diseñado por coach certificado en CrossFit. Evaluación funcional completa, objetivos claros y programa de 4-6 semanas. Sesiones de video coaching, retroalimentación sobre técnica y progresión. Seguimiento mensual de avances. Garantía de resultados.',
             '$100.00', '$50.00', 'https://images.unsplash.com/photo-1552961519-fbf46af7925d?w=400&h=300&fit=crop'),
            ('Botella de Agua Deportiva', 'Botella reutilizable de 1 litro de alta resistencia, aislamiento térmico manteniendo bebidas frías o calientes. Diseño ergonómico con logo del gym estampado. Material BPA-free, amigable al ambiente. Ideal para entrenamientos intensos. El acceorio perfecto del atleta.',
             '$35.00', '$17.50', 'https://images.unsplash.com/photo-1608270861620-7a0be6a1fb53?w=400&h=300&fit=crop'),
            ('Clase Nutrición', 'Taller educativo de nutrición deportiva con especialista certificado en nutricionismo clínico. Duración 90 minutos, en profundidad sobre macro/micronutrientes, timing de comidas, suplementación segura. Incluye planes alimentarios personalizados y resolución de dudas. Fundamental para optimizar resultados.',
             '$50.00', '$25.00', 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&h=300&fit=crop'),
        ],
        9: [  # Spa Relax Luxury
            ('Masaje Tailandés 60min', 'Masaje tradicional tailandés completo de 60 minutos que combina presión, estiramiento y acupresión en puntos energéticos. Terapeuta certificado con 10+ años de experiencia. Técnica milenaria que libera tensiones, mejora circulación y aporta relajación profunda. Acompañado con bebida de hierbas aromática.',
             '$180.00', '$90.00', 'https://images.unsplash.com/photo-1544161515-81205f8abedf?w=400&h=300&fit=crop'),
            ('Facial Anti-Edad', 'Facial premium de 60 minutos con productos suizos de lujo de la marca reconocida mundialmente. Incluye limpieza profunda, exfoliación, masaje facial rejuvenecedor, aplicación de sérum anti-edad y crema hidratante intensiva. Resultados visibles: piel más radiante, firme y revitalizada.',
             '$150.00', '$75.00', 'https://images.unsplash.com/photo-1576091160550-112173f7f869?w=400&h=300&fit=crop'),
            ('Sauna Infrarrojo 30min', 'Sesión de sauna infrarrojo relajante de 30 minutos en cabina privada. Temperatura controlada que penetra hasta 1.5 pulgadas en la piel, mejorando circulación sin estrés cardiac. Desintoxicación profunda, alivio del estrés y relajación muscular. Incluye bebida purificadora.',
             '$60.00', '$30.00', 'https://images.unsplash.com/photo-1544161515-81205f8abedf?w=400&h=300&fit=crop'),
            ('Paquete Spa Completo', 'Paquete integral de bienestar de 3 horas: masaje tailandés profesional (60min) + facial anti-edad premium (60min) + sauna infrarrojo (30min) + té aromático final. Experiencia completa que rejuvenece cuerpo y mente. Relajación absoluta y transformación integral.',
             '$320.00', '$160.00', 'https://images.unsplash.com/photo-1587884294521-a3e7e7b2b93b?w=400&h=300&fit=crop'),
        ],
        10: [  # Salón de Belleza "La Corona"
            ('Corte + Coloración', 'Corte profesional con técnica moderna ejecutado por estilista experimentado + coloración con tinte premium de marca internacional. Incluye consultoría de color, protección del cabello, secado y styling final. Transformación garantizada que realza tu belleza natural.',
             '$120.00', '$60.00', 'https://images.unsplash.com/photo-1562322506-f9a60b3b4f25?w=400&h=300&fit=crop'),
            ('Manicure + Pedicure', 'Manicure y pedicure completo con diseño de uñas de gel semi-permanente de durabilidad 3 semanas. Limpieza profunda, modelado de uña, aplicación de base y gel de color, decoraciones opcionales. Resultados profesionales con acabado impecable que luce radiante.',
             '$80.00', '$40.00', 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=300&fit=crop'),
            ('Tratamiento de Keratina', 'Tratamiento de keratina lisadora avanzado para cabello dañado, encrespado o rebelde. Aplicación profesional de productos premium brasileños, reposo de 72 horas recomendado. Resultados: cabello liso, brilloso y sedoso por 3 meses. Recuperaba la salud del cabello radicalmente.',
             '$150.00', '$75.00', 'https://images.unsplash.com/photo-1552961519-fbf46af7925d?w=400&h=300&fit=crop'),
            ('Extensiones de Cabello', 'Extensiones de cabello natural 100% humano de 60cm aplicadas mediante técnica de uniones seguras y duraderas. Disponible en múltiples tonos para combinar con tu cabello. Resultado: cabello voluminoso, largo y natural. Durabilidad 3-4 meses con cuidados adecuados.',
             '$200.00', '$100.00', 'https://images.unsplash.com/photo-1562322506-f9a60b3b4f25?w=400&h=300&fit=crop'),
        ],
        11: [  # Cine VIP Premium
            ('2 Boletos + Popcorn + Drink', 'Entrada para dos personas en sala de cine + popcorn mediano + bebida grande con hielo. Disfrutar del cine en comodidad con entrada prioritaria a las salas mejor acondicionadas. Snacks de calidad con opciones de sabores especiales. Experiencia cinematográfica completa.',
             '$45.00', '$22.50', 'https://images.unsplash.com/photo-1489599849228-8d85f17ea8e8?w=400&h=300&fit=crop'),
            ('Pack Película Premium', '4 boletos en sala IMAX con pantalla gigante y sonido Dolby Atmos envolvente + snacks gourmet: popcorn gourmet, nachos premium y bebidas. Experiencia visualy sonora superior. Acceso prioritario a funciones, ideal para familias o grupos de amigos.',
             '$200.00', '$100.00', 'https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=400&h=300&fit=crop'),
            ('Popcorn Gourmet', 'Popcorn casero con opciones de sabores gourmet: queso cheddar intenso, caramelo dulce o mezcla sabrosa. Elaborado con maicena premium, mantequilla real y condimentos importados. Fresco, crocante y adictivo. El acompañamiento perfecto para ver películas.',
             '$15.00', '$7.50', 'https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=400&h=300&fit=crop'),
            ('Café Premium + Snack', 'Café gourmet recién preparado acompañado de brownie artesanal  casero hecho con chocolate belga 70%. Combinación perfecta de bebida y postre. Café intenso y aromático se complementa con chocolate profundo y textura fudgy. Experiencia de sabor en cada momento del cine.',
             '$20.00', '$10.00', 'https://images.unsplash.com/photo-1495474472287-4d71bcdd-2085?w=400&h=300&fit=crop'),
        ],
        12: [  # Parque Temático "Aventura Total"
            ('Entrada Familiar 4 personas', 'Entrada para 4 personas a parque temático completo con acceso a todas las atracciones + almuerzo incluido (buffet de comida internacional). Disfrutar juegos mecánicos, shows en vivo y entretenimiento para todas las edades. Diversión integral garantizada. Recuerdos inolvidables en familia.',
             '$280.00', '$140.00', 'https://images.unsplash.com/photo-1464207687429-7505649dae38?w=400&h=300&fit=crop'),
            ('Programa VIP + Fast Pass', 'Entrada VIP para familia con Fast Pass que permite acceso prioritario a todas las atracciones, évitando colas. Comidas ilimitadas en restaurantes del parque, bebidas gratuitas durante el día. Acceso a áreas exclusivas y atenciones especiales VIP. Lujo y comodidad garantizada.',
             '$450.00', '$225.00', 'https://images.unsplash.com/photo-1552961519-fbf46af7925d?w=400&h=300&fit=crop'),
            ('Camiseta Oficial del Parque', 'Camiseta 100% algodón pre-encogido con logo y diseño oficial del parque impreso. Disponible en múltiples tallas desde niño hasta adulto. Prenda coleccionable que recuerda la visita y experiencias vividas. Calidad de impresión duradera que resiste lavados constantes.',
             '$35.00', '$17.50', 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop'),
            ('Fotos Profesionales Digitales', 'Pack de 20 fotos profesionales del parque', '$85.00', '$42.50', 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=300&fit=crop'),
        ],
        13: [  # Boutique Fashion "Elegancia"
            ('Vestido de Diseñador', 'Vestido exclusivo de diseñador italiano', '$350.00', '$175.00', 'https://images.unsplash.com/photo-1595777707802-521654d531a2?w=400&h=300&fit=crop'),
            ('Bolsa de Cuero Premium', 'Bolsa de cuero italiano genuino', '$280.00', '$140.00', 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=300&fit=crop'),
            ('Jeans Premium', 'Jeans de marca internacional premium', '$120.00', '$60.00', 'https://images.unsplash.com/photo-1542272604-787c62d465d1?w=400&h=300&fit=crop'),
            ('Blazer Ejecutivo', 'Blazer 100% lana para look profesional', '$180.00', '$90.00', 'https://images.unsplash.com/photo-1508762590798-1aa33fc19f41?w=400&h=300&fit=crop'),
        ],
        14: [  # Librería Cultural Plus
            ('Novela Bestseller', 'Última novela de autor reconocido + café', '$20.00', '$10.00', 'https://images.unsplash.com/photo-1507842217343-583f20270319?w=400&h=300&fit=crop'),
            ('Libro Academic', 'Libro de ficción o técnico premium', '$65.00', '$32.50', 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=400&h=300&fit=crop'),
            ('Comic Limitado', 'Comic edición limitada numerada', '$45.00', '$22.50', 'https://images.unsplash.com/photo-1478720568477-152d9e3fb27d?w=400&h=300&fit=crop'),
            ('Suscripción 3 meses', 'Acceso a biblioteca digital + cafetería', '$90.00', '$45.00', 'https://images.unsplash.com/photo-1507842217343-583f20270319?w=400&h=300&fit=crop'),
        ],
        15: [  # Hotel Boutique "Casa Magica"
            ('Noche Habitación Suite', 'Suite deluxe con vista + desayuno premium', '$280.00', '$140.00', 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&h=300&fit=crop'),
            ('Pack 3 Noches', 'Habitación suite + desayuno + spa gratis', '$720.00', '$360.00', 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&h=300&fit=crop'),
            ('Experiencia Meditación', 'Meditación guiada + yoga + té aromático', '$85.00', '$42.50', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop'),
            ('Tour Gastronómico', 'Tour a mercados locales + clase de cocina', '$120.00', '$60.00', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop'),
        ],
        16: [  # Hostal Viajero Amiga
            ('Cama Privada 1 Noche', 'Habitación privada con baño compartido', '$60.00', '$30.00', 'https://images.unsplash.com/photo-1598584886122-86ba7ffb84fe?w=400&h=300&fit=crop'),
            ('Pack 7 Noches', 'Habitación privada + desayunos + tours', '$350.00', '$175.00', 'https://images.unsplash.com/photo-1598584886122-86ba7ffb84fe?w=400&h=300&fit=crop'),
            ('Tour Completo Ciudad', 'Tour guiado a principales monumentos', '$45.00', '$22.50', 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400&h=300&fit=crop'),
            ('Cena Comida Casera', 'Cena preparada por chef con otros huéspedes', '$25.00', '$12.50', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop'),
        ],
        17: [  # Consultorio Dental Smile Plus
            ('Limpieza Dental Profesional', 'Limpieza con ultrasonido + fluorización', '$150.00', '$75.00', 'https://images.unsplash.com/photo-1574925120552-6d3d3b10f69f?w=400&h=300&fit=crop'),
            ('Blanqueamiento Dental', 'Blanqueamiento profesional LED avanzado', '$300.00', '$150.00', 'https://images.unsplash.com/photo-1576091160550-2173997f2b11?w=400&h=300&fit=crop'),
            ('Implante Dental', 'Implante dental con corona de porcelana', '$1200.00', '$600.00', 'https://images.unsplash.com/photo-1606811841689-23db76ff14ca?w=400&h=300&fit=crop'),
            ('Ortodoncia - Consulta', 'Evaluación + radiografías ortopédicas', '$200.00', '$100.00', 'https://images.unsplash.com/photo-1516575334481-f410a11be214?w=400&h=300&fit=crop'),
        ],
        18: [  # Peluquería Barbería Vintage
            ('Corte Clásico + Barba', 'Corte de navaja tradicional + peinado', '$50.00', '$25.00', 'https://images.unsplash.com/photo-1599458438325-93854b8f5c4f?w=400&h=300&fit=crop'),
            ('Afeitado Premium', 'Afeitado clásico de navaja con steam', '$40.00', '$20.00', 'https://images.unsplash.com/photo-1599458438325-93854b8f5c4f?w=400&h=300&fit=crop'),
            ('Masaje Facial', 'Masaje facial con productos premium', '$60.00', '$30.00', 'https://images.unsplash.com/photo-1576091160550-2173997f2b11?w=400&h=300&fit=crop'),
            ('Caballería Completa', 'Corte + barba + masaje + productos', '$120.00', '$60.00', 'https://images.unsplash.com/photo-1599458438325-93854b8f5c4f?w=400&h=300&fit=crop'),
        ],
        19: [  # Galería de Arte "Contempo"
            ('Entrada Galería', 'Entrada general + catálogo + vino', '$15.00', '$7.50', 'https://images.unsplash.com/photo-1577720643272-265b434e2a1e?w=400&h=300&fit=crop'),
            ('Obra de Arte Original', 'Pieza de artista emergente mexicano', '$800.00', '$400.00', 'https://images.unsplash.com/photo-1578314802414-269248b658f3?w=400&h=300&fit=crop'),
            ('Tour Privado + Vino', 'Tour guiado por curador + vino importado', '$100.00', '$50.00', 'https://images.unsplash.com/photo-1577720643272-265b434e2a1e?w=400&h=300&fit=crop'),
            ('Taller de Pintura', 'Clase introductoria de pintura acrílica', '$75.00', '$37.50', 'https://images.unsplash.com/photo-1549887534-7e9baab3db52?w=400&h=300&fit=crop'),
        ],
        20: [  # Academia de Danza Ritmo Vida
            ('Clase Privada 1 Hora', 'Clase particular de danza con instructor', '$80.00', '$40.00', 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=400&h=300&fit=crop'),
            ('Pack 10 Clases', 'Acceso a 10 clases de danza a elegir', '$350.00', '$175.00', 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=400&h=300&fit=crop'),
            ('Show de Danza', 'Entrada a show de fin de año de alumnos', '$40.00', '$20.00', 'https://images.unsplash.com/photo-1503205814626-35a92136e72c?w=400&h=300&fit=crop'),
            ('Vestuario de Presentación', 'Traje completo de danza para presentación', '$250.00', '$125.00', 'https://images.unsplash.com/photo-1516228732101-59c5f1721f4a?w=400&h=300&fit=crop'),
        ],
        21: [  # EdutechPy - Cursos Online
            ('Curso Python Básico', 'Curso completo Python desde cero + certificado', '$199.00', '$59.70', 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&h=300&fit=crop'),
            ('Curso Data Science', 'Data Science completo con Python + proyectos', '$349.00', '$104.70', 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop'),
            ('Curso Web Development', 'Web completo: HTML, CSS, JavaScript, React', '$299.00', '$89.70', 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&h=300&fit=crop'),
            ('Mentoría Personalizada', 'Sesiones 1-a-1 con mentor experto en tech', '$150.00', '$45.00', 'https://images.unsplash.com/photo-1522202176988-696f6929c113?w=400&h=300&fit=crop'),
            ('Pack Bootcamp Intensivo', 'Bootcamp 12 semanas Python + IA + Certificado', '$1500.00', '$450.00', 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&h=300&fit=crop'),
        ],
    }
    
    # Agregar ofertas
    duraciones = [2, 6, 12, 24, 48, 72]  # horas
    for negocio_id, ofertas in ofertas_por_negocio.items():
        for orden, (nombre, descripcion, precio_original, precio_oferta, imagen) in enumerate(ofertas, 1):
            duracion = random.choice(duraciones)
            fecha_vencimiento = datetime.now() + timedelta(hours=duracion)
            # Convertir precios de dólares a guaraníes
            precio_orig_gs = convertir_precio(precio_original)
            precio_ofer_gs = convertir_precio(precio_oferta)
            c.execute('''
                INSERT INTO ofertas (negocio_id, nombre, descripcion, precio_original, precio_oferta, imagen, orden, duracion_horas, fecha_vencimiento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (negocio_id, nombre, descripcion, precio_orig_gs, precio_ofer_gs, imagen, orden, duracion, fecha_vencimiento))
    
    conn.commit()
    
    # Mostrar resumen
    c.execute('SELECT COUNT(*) FROM ofertas')
    total_ofertas = c.fetchone()[0]
    
    print(f"✓ {total_ofertas} ofertas/productos agregados exitosamente")
    print("\nResumen por negocio:")
    
    for negocio in negocios:
        negocio_id, nombre, categoria = negocio
        c.execute('SELECT COUNT(*) FROM ofertas WHERE negocio_id = ?', (negocio_id,))
        count = c.fetchone()[0]
        print(f"  • {nombre}: {count} productos")
    
    conn.close()

if __name__ == '__main__':
    add_ofertas()
