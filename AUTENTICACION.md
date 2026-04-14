# Sistema de Autenticación para Negocios 🔐

## ¿Qué se agregó?

Se ha implementado un sistema completo de autenticación y gestión de credenciales para los negocios:

### 1. **Base de Datos**
- ✅ Se agregaron dos campos a la tabla `negocios`:
  - `usuario`: Identificador único para cada negocio
  - `contrasena`: Contraseña hasheada (SHA-256) para seguridad

### 2. **Páginas Nuevas**

#### `/login` - Página de Login
- Interfaz atractiva y responsive
- Los negocios pueden ingresar con sus credenciales
- Validación de usuario y contraseña
- Botón para mostrar/ocultar la contraseña

#### `/negocio/panel` - Panel Privado del Negocio
- Muestra información completa del negocio
- Display de credenciales de acceso (usuario)
- Formulario para cambiar contraseña
- Requiere autenticación

### 3. **Panel de Administración**
- Los administradores pueden:
  - Ver las credenciales de cada negocio
  - Generar automáticamente usuarios y contraseñas
  - Mostrar/ocultar contraseñas
  - Editar y crear negocios con sus credenciales

### 4. **Seguridad**
- ✅ Las contraseñas se hashean usando SHA-256
- ✅ Las sesiones se manejan de forma segura con Flask
- ✅ Los usuarios solo ven su propia información

## 🚀 Cómo Usar

### Para los Negocios:

1. **Acceder al Login**
   - Click en el botón "Mi Negocio" en la página principal
   - O dirígete a: `http://localhost:5000/login`

2. **Ingresar Credenciales**
   - Usuario: Se muestra en el panel de admin
   - Contraseña: Se proporciona al crear el negocio

3. **Panel del Negocio**
   - Una vez autenticado, verás tu información
   - Puedes cambiar tu contraseña en cualquier momento
   - Tu usuario se muestra para referencia

4. **Cambiar Contraseña**
   - Ve a tu panel: `/negocio/panel`
   - Sección "Cambiar Contraseña"
   - Ingresa la contraseña actual
   - Ingresa la nueva contraseña dos veces

### Para los Administradores:

1. **Acceder a Admin**
   - Click en el botón "Admin" en la página principal
   - O dirígete a: `http://localhost:5000/admin`

2. **Ver Credenciales**
   - En la lista de negocios, verás una caja con las credenciales
   - Usuario: Se muestra claramente
   - Contraseña: Se oculta por seguridad

3. **Crear Negocio con Credenciales**
   - Click en "Agregar Negocio"
   - Completa todos los campos
   - Sección "Credenciales de Acceso":
     - Click en "Generar" para crear usuario/contraseña automáticamente
     - O ingresa valores personalizados
   - Click en "Guardar"

4. **Editar Credenciales Existentes**
   - Click en "Editar" en un negocio
   - En la sección de credenciales:
     - Click en "Generar" para crear nuevas credenciales
     - Los campos se auto-generan
   - Guardar cambios

## 📊 Credenciales Ejemplo

Los negocios existentes ya tienen credenciales asignadas. Ejemplo:

```
Usuario: café_aroma_gourmet_9978
Contraseña: (se genera aleatoriamente)
```

El usuario es un identificador único basado en el nombre del negocio.

## 🔒 Medidas de Seguridad

1. **Hash de Contraseñas**: Todas las contraseñas se almacenan hasheadas
2. **Sesiones Seguras**: Flask maneja la autenticación de sesiones
3. **Validación**: Se valida usuario y contraseña antes de crear la sesión
4. **Logout**: Los negocios pueden cerrar sesión en cualquier momento

## 🛠️ Endpoints API

### Autenticación
- `POST /api/login` - Login de negocio
- `GET /logout` - Cerrar sesión

### Panel del Negocio
- `GET /negocio/panel` - Panel privado (requiere autenticación)
- `POST /api/negocio/cambiar-contrasena` - Cambiar contraseña

### Admin
- `GET /admin/negocios` - Listar todos los negocios
- `POST /admin/negocio` - Crear negocio con credenciales
- `PUT /admin/negocio/<id>` - Editar negocio y credenciales

## 📁 Archivos Modificados/Nuevos

### Nuevos:
- `templates/login.html` - Página de login
- `templates/negocio_panel.html` - Panel privado del negocio
- `setup_credentials.py` - Script para generar credenciales iniciales

### Modificados:
- `database.py` - Agregados campos y funciones de hash
- `app.py` - Agregadas rutas de autenticación
- `templates/admin.html` - Campos de credenciales en formulario
- `static/admin.js` - Lógica para generar credenciales
- `templates/index.html` - Link a página de login

## 💡 Notas Importantes

1. **Contraseña por defecto**: Las contraseñas se generan automáticamente al crear/editar negocios
2. **Reset de contraseña**: No hay función de "olvide mi contraseña" - el admin debe regenerarla
3. **Usuario único**: Cada usuario es único en el sistema
4. **Seguridad en producción**: En producción, cambiar `app.secret_key` por una clave segura y usar HTTPS

## 🎯 Próximas Mejoras Sugeridas

- Recuperación de contraseña por email
- Two-factor authentication (2FA)
- Auditoría de accesos
- Cambio de usuario/email
- Gestión de múltiples usuarios por negocio
