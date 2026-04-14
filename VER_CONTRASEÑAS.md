# 🔐 Sistema de Visualización de Contraseñas - Actualización

## ¿Qué se agregó?

Se mejoró la visualización y gestión de contraseñas en el panel de administración:

### ✅ **En la Lista de Negocios**
- ✨ Las contraseñas ahora se mostran (generadas recientemente) o están ocultas (como ••••••••)
- 👁️ **Botón de Mostrar/Ocultar**: Alterna entre vista oculta y visible
- 📋 **Botón de Copiar**: Copia la contraseña directamente al portapapeles
- 🔄 Cuando se regeneran credenciales, la contraseña se muestra automáticamente

### ✅ **En el Formulario de Edición**
- 👁️ **Botón de Mostrar/Ocultar**: Toggle para ver la contraseña mientras editas
- 📋 **Botón de Copiar**: Copia rápidamente la contraseña generada
- 🔄 **Botón Generar**: Crea automáticamente usuario y contraseña

## 🎯 Cómo Usar - Admin

### Ver Contraseñas de Negocios:
1. Ve a `/admin`
2. En la caja de credenciales de cada negocio:
   - Las contraseñas recién generadas aparecen ocultas (••••••••)
   - Click en el icono 👁️ para mostrar la contraseña
   - Click en el icono 📋 para copiar al portapapeles

### Regenerar Credenciales:
1. Click en "Editar" en un negocio
2. En la sección "Credenciales de Acceso":
   - Click en "Generar" para crear nuevas credenciales
   - Se muestra la nueva contraseña automáticamente
   - Puedes copiarla con el botón 📋
3. Click en "Guardar"

### Ver Contraseña mientras Editas:
1. En el formulario de edición:
   - Click en 👁️ para mostrar/ocultar
   - Click en 📋 para copiar la contraseña actual

## 💡 Cómo Funciona

### En el Cliente (JavaScript):
```javascript
// Se guardan las contraseñas temporales en memoria
credencialesTemporales[negocioId] = "ContraseñaDeLlegada";

// Al mostrar negocios, se verifica si existe contraseña temporal
// Si existe: muestra con toggle show/hide
// Si no existe: muestra ••••••••
```

### En el Backend:
- Las contraseñas se almacenan hasheadas (SHA-256) por seguridad
- **NUNCA** se devuelven en el API
- Solo se muestran en el cliente la contraseña "temporal" que subió el admin

## ⚠️ Notas Importantes

1. **Reinicio de Página**: Si recargas la página, se pierden las contraseñas temporales mostradas
   - Solución: Regenerar credenciales si necesitas verlas de nuevo
   
2. **Seguridad**: Las contraseñas hasheadas nunca se envían al cliente
   - Solo la contraseña que escribió el admin se almacena temporalmente

3. **Contraseña Original**: Una vez guardado un negocio, no se puede recuperar su contraseña original
   - Solución: Regenerar (generar una nueva) si se olvida

## 🎨 Interfaz Mejorada

- **Estilo gradiente** en la caja de credenciales (azul degradado)
- **Sombra suave** para mejor visual
- **Botones coloreados**: Eye (gris), Copy (azul)
- **Monospace font** para credenciales
- **Responsive design** - Funciona en mobile también

## 📝 Ejemplo de Flujo

```
Admin -> Click "Agregar Negocio"
    ↓
Admin -> Completa formulario
    ↓
Admin -> Click "Generar" en Credenciales
    ↓
Sistema genera: usuario_12345, ContrGHJ2
    ↓
Admin ve contraseña en el formulario
    ↓
Admin -> Click 👁️ para ocultar/mostrar
    ↓
Admin -> Click 📋 para copiar
    ↓
Admin -> Click "Guardar"
    ↓
Contraseña se hashea y guarda en BD
    ↓
En la lista, se muestra con credencial temporal
```

## 🔗 Cambios de Código

### Archivos Modificados:
- `static/admin.js` - Lógica de mostrar/ocultar contraseñas
- `templates/admin.html` - UI mejorada y funciones
- Estilos CSS para credenciales

### Variables Globales:
- `credencialesTemporales` - Almacena contraseñas en sesión

### Funciones Nuevas:
- `togglePasswordVisibility()` - Mostrar/ocultar en la lista
- `copiarContraseña()` - Copiar a portapapeles
- `mostrarContraseñaForm()` - Mostrar/ocultar en formulario
- `copiarContraseñaForm()` - Copiar desde formulario
