# Descubre Negocios - Plataforma de Promociones

Plataforma REAL para descubrir negocios locales con promociones exclusivas, sistema de ranking y valoraciones persistentes.

## Características Principales

### 🗺️ Descubrimiento de Negocios
- Vista de cards con información detallada
- Vista de mapa interactivo con Google Maps
- Filtros por categoría
- Ordenamiento por rating, reseñas o descuento

### 🎁 Promociones Ligeras (10-20%)
- Café gratis
- Desayuno gratis
- Descuentos del 10% al 20%
- Badges visuales destacados

### 📱 Contacto Directo
- Botón de WhatsApp con mensaje pre-cargado
- Botón de llamada directa
- Información de horarios y ubicación

### ⭐ Sistema de Ranking REAL
- Base de datos SQLite persistente
- Valoraciones reales de usuarios
- Rating promedio calculado automáticamente
- Los mejor valorados aparecen primero

### 💬 Sistema de Valoraciones
- Los usuarios pueden dejar valoraciones con nombre
- Calificación de 1 a 5 estrellas
- Comentarios de experiencia
- Las valoraciones se guardan permanentemente
- El rating del negocio se actualiza automáticamente

### � Sistema de Autenticación de Negocios
- **Login de Negocios**: Acceso seguro con usuario y contraseña
- **Panel Privado**: Cada negocio ve su información y gestiona su cuenta
- **Cambio de Contraseña**: Los negocios pueden actualizar sus credenciales
- **Credenciales Seguras**: Las contraseñas se hashean con SHA-256
- **Admin Panel**: Gestión total de usuarios y credenciales de negocios

📖 **Ver [AUTENTICACION.md](AUTENTICACION.md) para detalles completos**

### 🔧 Panel de Administración
- Agregar nuevos negocios con credenciales automáticas
- Editar negocios existentes y regenerar credenciales
- Eliminar negocios
- Ver todos los usuarios de los negocios
- Generar contraseñas seguras automáticamente

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos (opcional, se hace automáticamente)
python database.py

# Ejecutar aplicación
python app.py
```

Abre `http://localhost:5000` en tu navegador.

## Estructura de Base de Datos

### Tabla: negocios
- id, nombre, categoria, rating, reviews
- imagen, promocion, descuento
- direccion, telefono, whatsapp, horario
- lat, lng (coordenadas GPS)
- descripcion, servicios

### Tabla: valoraciones
- id, negocio_id, nombre, rating, comentario, fecha

## Tecnologías

- Flask (Backend)
- SQLite (Base de datos REAL)
- Bootstrap 5 (UI)
- Google Maps (Mapas)
- Font Awesome (Iconos)

## Uso

1. Navega por los negocios en la página principal
2. Haz clic en un negocio para ver detalles completos
3. Deja tu valoración con estrellas y comentario
4. Accede a `/admin` para gestionar negocios
5. Las valoraciones se guardan permanentemente en la base de datos

### 🚀 Acceso Rápido

- **Página Principal**: http://localhost:5000
- **Login de Negocio**: http://localhost:5000/login
- **Panel de Admin**: http://localhost:5000/admin
- **Panel del Negocio** (autenticado): http://localhost:5000/negocio/panel
- **Demo**: `python demo_auth.py` (muestra credenciales ejemplares)

## Archivo de Base de Datos

La base de datos se guarda en `negocios.db` y persiste entre reinicios.

## 🔐 Credenciales de Ejemplo (Después de ejecutar)

Todos los negocios tienen credenciales autogeneradas. Para probar:

```
Usuario: café_aroma_gourmet_9978
Contraseña: (Visible en admin panel)
```

Para ver todas las credenciales:
```bash
python demo_auth.py
```
