let negociosData = [];
let editingId = null;
let modal = null;
let ofertasModal = null;
let ofertaModal = null;
let currentNegocioId = null;
let currentOfertaId = null;
let ofertasData = [];
let credencialesTemporales = {}; // Guardar contraseñas temporales para mostrar

document.addEventListener('DOMContentLoaded', function() {
    modal = new bootstrap.Modal(document.getElementById('negocioModal'));
    ofertasModal = new bootstrap.Modal(document.getElementById('ofertasModal'));
    ofertaModal = new bootstrap.Modal(document.getElementById('ofertaModal'));
    cargarNegocios();
});

async function cargarNegocios() {
    try {
        const response = await fetch('/admin/negocios');
        const data = await response.json();
        if (!Array.isArray(data)) {
            console.error('Respuesta inesperada:', data);
            return;
        }
        negociosData = data;
        console.log('Negocios cargados:', negociosData.length);
        mostrarNegocios();
    } catch (error) {
        console.error('Error al cargar negocios:', error);
        document.getElementById('negociosList').innerHTML = '<div class="alert alert-danger">Error al cargar negocios. Revisa la consola.</div>';
    }
}

function mostrarNegocios() {
    const container = document.getElementById('negociosList');
    container.innerHTML = '';

    negociosData.forEach(negocio => {
        const item = document.createElement('div');
        item.className = 'negocio-item';

        // Imagen
        const imgCol = document.createElement('div');
        imgCol.className = 'col-md-2';
        if (negocio.imagen) {
            const img = document.createElement('img');
            img.src = negocio.imagen;
            img.onerror = () => img.style.display = 'none';
            img.style.cssText = 'width:100px;height:100px;object-fit:cover;border-radius:10px;';
            imgCol.appendChild(img);
        }

        // Info
        const infoCol = document.createElement('div');
        infoCol.className = 'col-md-6';

        const nombre = document.createElement('h5');
        nombre.textContent = negocio.nombre;
        infoCol.appendChild(nombre);

        const cat = document.createElement('p');
        cat.className = 'mb-1 text-muted';
        cat.textContent = negocio.categoria;
        infoCol.appendChild(cat);

        const rating = document.createElement('p');
        rating.className = 'mb-1';
        rating.innerHTML = `<i class="fas fa-star text-warning"></i> ${negocio.rating} (${negocio.reviews} reseñas)`;
        infoCol.appendChild(rating);

        const promo = document.createElement('p');
        promo.className = 'mb-0';
        promo.innerHTML = '<strong>Promoción:</strong> ';
        promo.appendChild(document.createTextNode(negocio.promocion || '-'));
        infoCol.appendChild(promo);

        // Contador de ofertas
        const activas = negocio.ofertas_activas || 0;
        const total = negocio.total_ofertas || 0;
        const ofertasInfo = document.createElement('p');
        ofertasInfo.className = 'mb-1 mt-1';
        ofertasInfo.innerHTML = `
            <span class="badge ${activas > 0 ? 'bg-success' : 'bg-secondary'} me-1">
                <i class="fas fa-circle me-1" style="font-size:0.6rem;"></i>${activas > 0 ? 'Activo' : 'Inactivo'}
            </span>
            <span class="badge bg-light text-dark border">
                <i class="fas fa-tags me-1"></i>${activas} activa${activas !== 1 ? 's' : ''} / ${total} total
            </span>
        `;
        infoCol.appendChild(ofertasInfo);

        if (negocio.usuario) {
            const credBox = document.createElement('div');
            credBox.className = 'credenciales-box mt-3';

            // Fila usuario
            const userItem = document.createElement('div');
            userItem.className = 'credencial-item';
            const userLabel = document.createElement('span');
            userLabel.className = 'credencial-label';
            userLabel.textContent = ' Usuario:';
            const userIcon = document.createElement('i');
            userIcon.className = 'fas fa-user';
            userLabel.prepend(userIcon);
            const userVal = document.createElement('span');
            userVal.className = 'credencial-value';
            userVal.textContent = negocio.usuario;
            userItem.appendChild(userLabel);
            userItem.appendChild(userVal);

            // Fila contraseña
            const passItem = document.createElement('div');
            passItem.className = 'credencial-item';
            const passLabel = document.createElement('span');
            passLabel.className = 'credencial-label';
            passLabel.textContent = ' Contraseña:';
            const lockIcon = document.createElement('i');
            lockIcon.className = 'fas fa-lock';
            passLabel.prepend(lockIcon);
            const passVal = document.createElement('span');
            passVal.className = 'credencial-value';
            passVal.id = 'password_' + negocio.id;
            passVal.textContent = credencialesTemporales[negocio.id] || '••••••••';
            passItem.appendChild(passLabel);
            passItem.appendChild(passVal);

            credBox.appendChild(userItem);
            credBox.appendChild(passItem);
            infoCol.appendChild(credBox);

            const loginLink = document.createElement('small');
            loginLink.className = 'd-block mt-2';
            loginLink.innerHTML = `<a href="/login" target="_blank" class="btn btn-outline-primary btn-sm w-100"><i class="fas fa-sign-in-alt me-1"></i>Entrar como negocio</a>`;
            infoCol.appendChild(loginLink);
        } else {
            const sinCred = document.createElement('div');
            sinCred.className = 'mt-2';
            sinCred.innerHTML = `<span class="badge bg-warning text-dark me-2"><i class="fas fa-exclamation-triangle me-1"></i>Sin credenciales</span>
                <button class="btn btn-sm btn-outline-warning" onclick="editarNegocio(${negocio.id})"><i class="fas fa-key me-1"></i>Asignar acceso</button>`;
            infoCol.appendChild(sinCred);
        }

        // Botones
        const btnCol = document.createElement('div');
        btnCol.className = 'col-md-4 text-end';

        const btnEditar = document.createElement('button');
        btnEditar.className = 'btn btn-primary btn-sm mb-1 me-1';
        btnEditar.innerHTML = '<i class="fas fa-edit"></i> Editar';
        btnEditar.onclick = () => editarNegocio(negocio.id);

        const btnOfertas = document.createElement('button');
        btnOfertas.className = 'btn btn-warning btn-sm mb-1 me-1';
        btnOfertas.innerHTML = '<i class="fas fa-tags"></i> Ofertas';
        btnOfertas.onclick = () => gestionarOfertas(negocio.id);

        const btnEliminar = document.createElement('button');
        btnEliminar.className = 'btn btn-danger btn-sm mb-1';
        btnEliminar.innerHTML = '<i class="fas fa-trash"></i> Eliminar';
        btnEliminar.onclick = () => eliminarNegocio(negocio.id);

        btnCol.appendChild(btnEditar);
        btnCol.appendChild(btnOfertas);
        btnCol.appendChild(btnEliminar);

        // Armar fila
        const row = document.createElement('div');
        row.className = 'row align-items-center';
        row.appendChild(imgCol);
        row.appendChild(infoCol);
        row.appendChild(btnCol);
        item.appendChild(row);
        container.appendChild(item);
    });
}

function mostrarFormulario() {
    editingId = null;
    document.getElementById('modalTitle').textContent = 'Agregar Negocio';
    document.getElementById('negocioForm').reset();
    document.getElementById('negocioId').value = '';
    document.getElementById('imagePreview').innerHTML = '';
    document.getElementById('imagenFile').value = '';
    for (let i = 0; i < 3; i++) {
        document.getElementById(`foto_${i}`).value = '';
        document.getElementById(`fotoUrl_${i}`).value = '';
        document.getElementById(`fotoPreview_${i}`).innerHTML = '';
    }
    document.getElementById('usuario').value = '';
    document.getElementById('contrasena').value = '';
    // Resetear el tipo de input - SIEMPRE mostrar como texto
    document.getElementById('contrasena').type = 'text';
    const eyeIcon = document.getElementById('eyeIcon');
    if (eyeIcon) {
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
    modal.show();
}

function editarNegocio(id) {
    const negocio = negociosData.find(n => n.id === id);
    if (!negocio) return;
    
    editingId = id;
    document.getElementById('modalTitle').textContent = 'Editar Negocio';
    document.getElementById('negocioId').value = negocio.id;
    document.getElementById('nombre').value = negocio.nombre;
    document.getElementById('categoria').value = negocio.categoria;
    // ciudad se setea después de que cargarCiudadesSelect termine (ver evento show.bs.modal)
    window._ciudadPendiente = negocio.ciudad || '';
    document.getElementById('imagen').value = negocio.imagen;
    document.getElementById('promocion').value = negocio.promocion;
    document.getElementById('descuento').value = negocio.descuento;
    document.getElementById('direccion').value = negocio.direccion;
    document.getElementById('mapsLink').value = negocio.mapsLink || '';
    document.getElementById('horario').value = negocio.horario;
    document.getElementById('telefono').value = negocio.telefono;
    document.getElementById('whatsapp').value = negocio.whatsapp;
    document.getElementById('descripcion').value = negocio.descripcion || '';
    
    // Cargar credenciales
    document.getElementById('usuario').value = negocio.usuario || '';
    document.getElementById('contrasena').value = '';
    
    // Mostrar contraseña como texto SIEMPRE
    document.getElementById('contrasena').type = 'text';
    const eyeIcon = document.getElementById('eyeIconForm');
    if (eyeIcon) {
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    }
    
    // Servicios - convertir array a texto con saltos de línea
    if (negocio.servicios) {
        try {
            const serviciosArray = typeof negocio.servicios === 'string' 
                ? JSON.parse(negocio.servicios) 
                : negocio.servicios;
            document.getElementById('servicios').value = serviciosArray.join('\n');
        } catch (e) {
            document.getElementById('servicios').value = '';
        }
    } else {
        document.getElementById('servicios').value = '';
    }
    
    // Limpiar archivo de imagen
    document.getElementById('imagenFile').value = '';
    
    // Limpiar fotos adicionales
    for (let i = 0; i < 3; i++) {
        document.getElementById(`foto_${i}`).value = '';
        document.getElementById(`fotoUrl_${i}`).value = '';
        document.getElementById(`fotoPreview_${i}`).innerHTML = '';
    }
    
    // Preview de imagen existente
    if (negocio.imagen) {
        document.getElementById('imagePreview').innerHTML = `
            <img src="${negocio.imagen}" style="max-width: 200px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <p class="text-muted mt-2"><small>Imagen actual</small></p>
        `;
    }
    
    // Cargar fotos adicionales existentes
    const fotos = negocio.fotos || [];
    for (let i = 0; i < 3; i++) {
        if (fotos[i]) {
            document.getElementById(`fotoUrl_${i}`).value = fotos[i];
            document.getElementById(`foto_${i}`).value = fotos[i];
            document.getElementById(`fotoPreview_${i}`).innerHTML = `<img src="${fotos[i]}" style="max-width:100%; height:60px; object-fit:cover; border-radius:5px;">`;
        }
    }
    
    modal.show();
}

async function eliminarNegocio(id) {
    if (!confirm('¿Estás seguro de eliminar este negocio?')) return;
    
    try {
        const response = await fetch(`/admin/negocio/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Negocio eliminado exitosamente');
            cargarNegocios();
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar negocio');
    }
}

document.getElementById('negocioForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Obtener imagen (archivo o URL)
    let imagenUrl = document.getElementById('imagen').value;
    const imagenFile = document.getElementById('imagenFile').files[0];
    
    if (imagenFile) {
        const reader = new FileReader();
        imagenUrl = await new Promise((resolve) => {
            reader.onload = (e) => resolve(e.target.result);
            reader.readAsDataURL(imagenFile);
        });
    }
    
    // Recoger fotos adicionales
    const fotos = [];
    for (let i = 0; i < 3; i++) {
        const val = document.getElementById(`foto_${i}`).value;
        if (val) fotos.push(val);
    }
    
    const data = {
        nombre: document.getElementById('nombre').value,
        categoria: document.getElementById('categoria').value,
        imagen: imagenUrl || 'https://images.unsplash.com/photo-1556740749-887f6717d7e4?w=400&h=300&fit=crop',
        promocion: document.getElementById('promocion').value,
        descuento: document.getElementById('descuento').value,
        direccion: document.getElementById('direccion').value,
        mapsLink: document.getElementById('mapsLink').value,
        horario: document.getElementById('horario').value,
        telefono: document.getElementById('telefono').value,
        whatsapp: document.getElementById('whatsapp').value,
        descripcion: document.getElementById('descripcion').value,
        servicios: document.getElementById('servicios').value.split('\n').filter(s => s.trim() !== '').slice(0, 4),
        usuario: document.getElementById('usuario').value,
        contrasena: document.getElementById('contrasena').value,
        fotos: fotos,
        ciudad: document.getElementById('ciudad').value
    };
    
    try {
        let response;
        if (editingId) {
            response = await fetch(`/admin/negocio/${editingId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch('/admin/negocio', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
        }
        
        if (response.ok) {
            const result = await response.json();

            const passPlain = result.contrasena_plain || (data.contrasena ? data.contrasena : null);
            const usuarioFinal = result.usuario || data.usuario;
            const negocioId = result.negocio && result.negocio.id;
            if (passPlain && negocioId) {
                credencialesTemporales[negocioId] = passPlain;
            }

            if (!editingId && result.contrasena_plain) {
                alert(`✅ Negocio creado exitosamente\n\n👤 Usuario: ${usuarioFinal}\n🔑 Contraseña: ${result.contrasena_plain}\n\n⚠️ Guarda estas credenciales, el negocio las necesita para iniciar sesión.`);
            } else if (editingId && data.contrasena) {
                alert(`✅ Negocio actualizado\n\n👤 Usuario: ${data.usuario}\n🔑 Contraseña: ${data.contrasena}`);
            } else {
                alert(editingId ? 'Negocio actualizado' : 'Negocio agregado');
            }
            modal.hide();
            cargarNegocios();
        } else {
            const err = await response.json().catch(() => ({}));
            alert('Error al guardar: ' + (err.error || err.message || response.status));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al guardar negocio');
    }
});

// Función para mostrar/ocultar contraseña en la lista de negocios
function togglePasswordVisibility(negocioId, elementId) {
    const element = document.getElementById(elementId);
    const eyeIcon = document.getElementById(`eye_${negocioId}`);
    const password = element.getAttribute('data-password');
    
    if (!password) {
        alert('⚠️ Para ver la contraseña, necesitas generarla primero.\n\nHaz clic en "Editar" y luego "Generar" en la sección de Credenciales.');
        return;
    }
    
    if (element.textContent === '••••••••') {
        element.textContent = password;
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    } else {
        element.textContent = '••••••••';
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
}

// Función para copiar contraseña al portapapeles
function copiarContraseña(password) {
    if (!password) {
        alert('⚠️ Para copiar la contraseña, necesitas generarla primero.\n\nHaz clic en "Editar" y luego "Generar" en la sección de Credenciales.');
        return;
    }
    
    navigator.clipboard.writeText(password).then(() => {
        alert('✓ Contraseña copiada al portapapeles');
    }).catch(err => {
        console.error('Error al copiar:', err);
        alert('❌ Error al copiar. Intenta de nuevo.');
    });
}

// Guardar contraseña temporal cuando se genera
function guardarContraseñaTemporal(negocioId, password) {
    credencialesTemporales[negocioId] = password;
    // Actualizar la vista
    setTimeout(() => {
        mostrarNegocios();
    }, 100);
}

// ====== FUNCIONES PARA OFERTAS ======
let negocioOfertasActual = null;
let ofertaEnEdicion = null;

function gestionarOfertas(negocioId) {
    negocioOfertasActual = negocioId;
    ofertaEnEdicion = null;
    
    const negocio = negociosData.find(n => n.id === negocioId);
    document.getElementById('ofertasModalTitle').textContent = `Ofertas - ${negocio.nombre}`;
    
    // Guardar negocio_id en el botón agregar como respaldo
    const btnAgregar = document.getElementById('btnAgregarOferta');
    if (btnAgregar) btnAgregar.dataset.negocioId = negocioId;
    
    cargarOfertasAdmin(negocioId);
    ofertasModal.show();
}

async function cargarOfertasAdmin(negocioId) {
    try {
        // Usar endpoint público de ofertas (no requiere sesión)
        const response = await fetch(`/api/ofertas/${negocioId}`);
        const ofertas = await response.json();
        
        const container = document.getElementById('ofertasListAdmin');
        
        if (ofertas.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay ofertas para este negocio</p>';
        } else {
            let html = '';
            ofertas.forEach(oferta => {
                // Calcular tiempo restante
                const vencimiento = new Date(oferta.fecha_vencimiento);
                const ahora = new Date();
                const diferencia = vencimiento - ahora;
                
                let duracionTexto = '';
                if (diferencia > 0) {
                    const horas = Math.floor(diferencia / (1000 * 60 * 60));
                    const dias = Math.floor(horas / 24);
                    if (dias > 0) {
                        duracionTexto = `${dias}d ${horas % 24}h restante`;
                    } else {
                        duracionTexto = `${horas}h restante`;
                    }
                } else {
                    duracionTexto = 'Expirada';
                }
                
                html += `
                    <div class="oferta-item-admin">
                        <div class="row align-items-center">
                            <div class="col-md-8">
                                <h6>${oferta.nombre}</h6>
                                <p class="mb-1 small text-muted">${oferta.descripcion || '-'}</p>
                                <p class="mb-0 small">
                                    <span class="badge bg-primary">${oferta.precio_original}</span>
                                    <span class="badge bg-success">${oferta.precio_oferta}</span>
                                    <span class="badge bg-info">⏱️ ${duracionTexto}</span>
                                </p>
                            </div>
                            <div class="col-md-4 text-end">
                                <button class="btn btn-sm btn-warning" onclick="editarOfertaAdmin(${oferta.id}, '${oferta.nombre}', '${oferta.descripcion || ''}', '${oferta.precio_original}', '${oferta.precio_oferta}', '${oferta.imagen || ''}', ${oferta.duracion_horas})">
                                    <i class="fas fa-edit"></i> Editar
                                </button>
                                <button class="btn btn-sm btn-danger" onclick="eliminarOfertaAdmin(${oferta.id})">
                                    <i class="fas fa-trash"></i> Eliminar
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        }
    } catch (error) {
        console.error('Error al cargar ofertas:', error);
    }
}

function mostrarFormularioOferta() {
    ofertaEnEdicion = null;
    document.getElementById('ofertaForm').reset();
    document.getElementById('ofertaDuracion').value = '24';
    document.getElementById('ofertaImagePreview').innerHTML = '';
    document.getElementById('ofertaModalTitle').textContent = 'Agregar Oferta';
    ofertaModal.show();
}

function editarOfertaAdmin(id, nombre, descripcion, precioOriginal, precioOferta, imagen, duracion) {
    ofertaEnEdicion = id;
    document.getElementById('ofertaNombre').value = nombre;
    document.getElementById('ofertaDescripcion').value = descripcion;
    document.getElementById('ofertaPrecioOriginal').value = precioOriginal;
    document.getElementById('ofertaPrecioOferta').value = precioOferta;
    document.getElementById('ofertaImagen').value = imagen;
    document.getElementById('ofertaDuracion').value = duracion || '24';
    document.getElementById('ofertaModalTitle').textContent = 'Editar Oferta';
    ofertaModal.show();
}

async function guardarOferta() {
    const nombre = document.getElementById('ofertaNombre').value.trim();
    const descripcion = document.getElementById('ofertaDescripcion').value;
    const precioOriginal = document.getElementById('ofertaPrecioOriginal').value.trim();
    const precioOferta = document.getElementById('ofertaPrecioOferta').value.trim();
    const duracion = document.getElementById('ofertaDuracion')?.value || '24';

    // Procesar imagen: archivo o URL
    let imagen = document.getElementById('ofertaImagen').value;
    const imagenFile = document.getElementById('ofertaImagenFile')?.files[0];
    if (imagenFile) {
        imagen = await new Promise(resolve => {
            const r = new FileReader();
            r.onload = e => resolve(e.target.result);
            r.readAsDataURL(imagenFile);
        });
    }

    // Recuperar negocio_id
    if (!negocioOfertasActual) {
        const btn = document.getElementById('btnAgregarOferta');
        if (btn && btn.dataset.negocioId) negocioOfertasActual = parseInt(btn.dataset.negocioId);
    }

    if (!negocioOfertasActual) { alert('Error: negocio no seleccionado'); return; }
    if (!nombre || !precioOriginal || !precioOferta) { alert('Completá los campos obligatorios'); return; }

    const url = ofertaEnEdicion ? `/admin/oferta/${ofertaEnEdicion}` : '/admin/oferta';
    const metodo = ofertaEnEdicion ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: metodo,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre, descripcion,
                precio_original: precioOriginal,
                precio_oferta: precioOferta,
                imagen,
                duracion_horas: parseInt(duracion),
                negocio_id: negocioOfertasActual
            })
        });
        const data = await response.json();
        if (response.ok && data.success) {
            ofertaModal.hide();
            cargarOfertasAdmin(negocioOfertasActual);
        } else {
            alert('Error: ' + (data.error || JSON.stringify(data)));
        }
    } catch (error) {
        console.error(error);
        alert('Error de conexión: ' + error.message);
    }
}

async function eliminarOfertaAdmin(id) {
    if (!confirm('¿Eliminar esta oferta?')) return;
    try {
        const response = await fetch(`/admin/oferta/${id}`, { method: 'DELETE' });
        if (response.ok) {
            cargarOfertasAdmin(negocioOfertasActual);
        } else {
            alert('Error al eliminar');
        }
    } catch (error) {
        alert('Error de conexión');
    }
}

function previewOfertaImage(input) {
    const preview = document.getElementById('ofertaImagePreview');
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" style="max-width: 200px; margin-top: 10px; border-radius: 5px;">`;
        };
        reader.readAsDataURL(input.files[0]);
    }
}
