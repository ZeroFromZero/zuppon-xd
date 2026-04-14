import sqlite3

def update_curso_python():
    """Actualizar descripción del Curso Python Básico"""
    conn = sqlite3.connect('negocios.db')
    c = conn.cursor()
    
    # Actualizar la oferta
    c.execute('''
        UPDATE ofertas 
        SET descripcion = ?
        WHERE nombre = ?
    ''', ('Introducción a la programación con Python', 'Curso Python Básico'))
    
    conn.commit()
    
    # Verificar
    c.execute('SELECT id, nombre, descripcion FROM ofertas WHERE nombre = ?', ('Curso Python Básico',))
    resultado = c.fetchone()
    
    if resultado:
        print(f"✓ Actualizado:")
        print(f"  Nombre: {resultado[1]}")
        print(f"  Descripción: {resultado[2]}")
    
    conn.close()

if __name__ == '__main__':
    update_curso_python()
