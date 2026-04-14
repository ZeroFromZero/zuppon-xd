#!/usr/bin/env python3
from database import get_connection
from datetime import datetime, timedelta
import random

def actualizar_duraciones():
    """Actualiza todas las ofertas con duraciones aleatorias y fechas de vencimiento"""
    conn = get_connection()
    c = conn.cursor()
    
    # Verificar si las columnas existen, si no, agregarlas
    try:
        c.execute("ALTER TABLE ofertas ADD COLUMN fecha_vencimiento TIMESTAMP")
        print("✓ Columna fecha_vencimiento agregada")
    except:
        print("✓ Columna fecha_vencimiento ya existe")
    
    try:
        c.execute("ALTER TABLE ofertas ADD COLUMN duracion_horas INTEGER DEFAULT 48")
        print("✓ Columna duracion_horas agregada")
    except:
        print("✓ Columna duracion_horas ya existe")
    
    # Obtener todas las ofertas sin fecha de vencimiento
    c.execute("SELECT id FROM ofertas WHERE fecha_vencimiento IS NULL")
    ofertas_sin_duracion = [row[0] for row in c.fetchall()]
    
    duraciones = [2, 6, 12, 24, 48, 72]  # 2 horas, 6 horas, 12 horas, 1 día, 2 días, 3 días
    
    for oferta_id in ofertas_sin_duracion:
        duracion = random.choice(duraciones)
        fecha_vencimiento = datetime.now() + timedelta(hours=duracion)
        
        c.execute('''
            UPDATE ofertas 
            SET duracion_horas = ?, fecha_vencimiento = ?
            WHERE id = ?
        ''', (duracion, fecha_vencimiento, oferta_id))
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ {len(ofertas_sin_duracion)} ofertas actualizadas con duraciones")
    print("✓ Duraciones agregadas: 2h, 6h, 12h, 24h, 48h, 72h")

if __name__ == '__main__':
    actualizar_duraciones()
