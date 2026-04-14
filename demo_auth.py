#!/usr/bin/env python
"""
Script de demostración del sistema de autenticación
Muestra cómo funcionan las credenciales de los negocios
"""

from database import get_connection, verify_password

def mostrar_credenciales():
    """Muestra algunos negocios con sus credenciales"""
    conn = get_connection()
    c = conn.cursor()
    
    # Obtener algunos negocios
    c.execute('SELECT id, nombre, usuario FROM negocios LIMIT 5')
    negocios = c.fetchall()
    
    print("\n" + "="*70)
    print("🔐 SISTEMA DE AUTENTICACIÓN DE NEGOCIOS")
    print("="*70)
    print("\n📋 Primeros 5 Negocios Registrados:\n")
    
    for i, negocio in enumerate(negocios, 1):
        print(f"{i}. {negocio['nombre']}")
        print(f"   Usuario: {negocio['usuario']}")
        print(f"   Link de acceso: http://localhost:5000/login")
        print()
    
    conn.close()

def verificar_autenticacion():
    """Verifica que el sistema de hash funcione correctamente"""
    from database import hash_password
    
    print("\n" + "="*70)
    print("✅ VERIFICACIÓN DEL SISTEMA DE HASHING")
    print("="*70)
    
    # Test de contraseña
    password = "TestPassword123"
    hash_result = hash_password(password)
    
    print(f"\nContraseña original: {password}")
    print(f"Hash generado: {hash_result[:20]}...")
    print(f"Verificación: {'✓ CORRECTO' if verify_password(password, hash_result) else '✗ ERROR'}")
    
    # Test de contraseña incorrecta
    print(f"\nVerificación con contraseña incorrecta: ", end="")
    print(f"{'✓ CORRECTO (rechazada)' if not verify_password('WrongPassword', hash_result) else '✗ ERROR'}")

def mostrar_instrucciones():
    """Muestra instrucciones de uso"""
    print("\n" + "="*70)
    print("🚀 CÓMO COMENZAR")
    print("="*70)
    print("""
1. INICIA LA APLICACIÓN:
   python app.py

2. ACCEDE AL PANEL DE ADMIN:
   http://localhost:5000/admin
   - Aquí verás todos los negocios con sus credenciales
   - Puedes generar nuevas credenciales
   - Puedes editar y crear negocios

3. PRUEBA EL LOGIN DE NEGOCIO:
   http://localhost:5000/login
   - Ingresa un usuario de la lista anterior
   - La contraseña se genera aleatoriamente (pídele al admin)

4. ACCEDE AL PANEL DEL NEGOCIO:
   http://localhost:5000/negocio/panel
   - Solo si estás autenticado
   - Puedes cambiar tu contraseña aquí

5. CÓMO OBTENER CREDENCIALES:
   - En el panel de admin, puedes ver todos los usuarios
   - Para la contraseña, el admin debe mostrarla generando nuevas credenciales
   - O resetear la contraseña del negocio
    """)

if __name__ == "__main__":
    mostrar_credenciales()
    verificar_autenticacion()
    mostrar_instrucciones()
    
    print("\n" + "="*70)
    print("📚 Para más información, consulta AUTENTICACION.md")
    print("="*70 + "\n")
