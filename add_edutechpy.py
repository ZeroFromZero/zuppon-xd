import sqlite3

def add_edutechpy():
    """Agregar negocio educativo EdutechPy"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    edutechpy = (
        'EdutechPy - Cursos Online', 
        'Educación', 
        4.9, 
        421, 
        'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&h=300&fit=crop',
        'Primer mes 70% descuento + acceso a 50+ cursos. Certificados gratis',
        70,
        'Plataforma 100% Online, Disponible Mundialmente',
        '',
        '+525588887777',
        '5525588887777',
        'Acceso 24/7 desde cualquier dispositivo',
        'EdutechPy es una plataforma revolucionaria de educación online especializada en tecnología moderna. Ofrecemos más de 50 cursos certificados en Python, Data Science, Web Development, Inteligencia Artificial y Machine Learning. Nuestros instructores son profesionales certificados con experiencia en empresas Tech de renombre internacional. Cada curso incluye proyectos prácticos reales, ejercicios interactivos, dudas resueltas por mentores, y acceso a una comunidad de más de 10,000 estudiantes activos. Contamos con certificados reconocidos en la industria que potencian tu CV laboral. Aprende a tu propio ritmo con contenido actualizado continuamente. Acceso 24/7 desde cualquier dispositivo: computadora, tablet o teléfono. Ofertas especiales para principiantes y paquetes empresariales para equipos.',
        'Python,DataScience,WebDev,IA,Certificados,Mentoria,Comunidad'
    )
    
    c.execute('''
        INSERT INTO negocios (nombre, categoria, rating, reviews, imagen, promocion, descuento, 
                            direccion, mapsLink, telefono, whatsapp, horario, descripcion, servicios)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', edutechpy)
    
    conn.commit()
    conn.close()
    print("✓ EdutechPy agregado exitosamente")

if __name__ == '__main__':
    add_edutechpy()
