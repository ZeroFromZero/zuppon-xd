// Gestión de ofertas
async function cargarOfertasNegocio(negocioId) {
    try {
        const response = await fetch(`/api/ofertas/${negocioId}`);
        ofertasData = await response.json();
        
        const container = document.getElementById('ofertasListAdmin');
        container.innerHTML = '';
        
        if (ofertasData.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay ofertas aún. Agrega hasta 3 ofertas.</p>';
        } else {
            ofertasData.forEach((oferta, index) => {
                const item = document.createElement('div');
                item.className = 'oferta-item-admin mb-3';
                item.innerHTML = `
                    <div class="row align-items-center">
                        <div class="col-md-1">
                            <div class="btn-group-vertical">
                                <button class="btn btn-sm btn-outline-secondary" onclick="cambiarOrden(${oferta.id}, 'arriba')" ${index === 0 ? 'disabled' : ''}>
                                    <i class="fas fa-chevron-up"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-secondary" onclick="cambiarOrden(${oferta.id}, 'abajo')" ${index === ofertasData.length - 1 ? 'disabled' : ''}>
                                    <i class="fas fa-chevron-down"></i>
                                </button>
                            </div>
                        </div>
                        <div class="col-md-2">
                            ${oferta.imagen ? `<img src="${oferta.imagen}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px;">` : '<div style="width: 80px; height: 80px; background: #ddd; border-radius: 8px;"></div>'}
                        </div>
                        <div class="col-md-5">
                            <h6>${oferta.nombre}</h6>
                            <p class="mb-0 text-muted small">${oferta.descripcion || 'Sin descripción'}</p>
                            <span class="text-muted text-decoration-line-through small">${oferta.precio_original}</span>
                            <strong class="text-success ms-2">${oferta.precio_oferta}</strong>
                        <div class="col-md-4 text-end">
                            <button class="btn btn-sm btn-primary" onclick="editarOferta(${oferta.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="eliminarOferta(${oferta.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                `;
                container.appendChild(item);
            });
        }
        
        // Habilitar/deshabilitar botón agregar
        const btnAgregar = document.getElementById('btnAgregarOferta');
        if (ofertasData.length >= 3) {
            btnAgregar.disabled = true;
            btnAgregar.innerHTML = '<i class="fas fa-ban"></i> Máximo 3 ofertas';
        } else {
            btnAgregar.disabled = false;
            btnAgregar.innerHTML = '<i class="fas fa-plus"></i> Agregar Oferta';
        }
        
    } catch (error) {
        console.error('Error al cargar ofertas:', error);
    }
}

async function cambiarOrden(ofertaId, direccion) {
    try {
        const response = await fetch(`/api/oferta/${ofertaId}/orden`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({direccion})
        });
        
        if (response.ok) {
            await cargarOfertasNegocio(currentNegocioId);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function editarOferta(ofertaId) {
    const oferta = ofertasData.find(o => o.id === ofertaId);
    if (!oferta) return;
    
    currentOfertaId = ofertaId;
    document.getElementById('ofertaModalTitle').textContent = 'Editar Oferta';
    document.getElementById('ofertaNombre').value = oferta.nombre;
    document.getElementById('ofertaDescripcion').value = oferta.descripcion || '';
    document.getElementById('ofertaPrecioOriginal').value = oferta.precio_original;
    document.getElementById('ofertaPrecioOferta').value = oferta.precio_oferta;
    document.getElementById('ofertaImagen').value = oferta.imagen || '';
    
    if (oferta.imagen) {
        document.getElementById('ofertaImagePreview').innerHTML = `
            <img src="${oferta.imagen}" style="max-width: 150px; border-radius: 8px; margin-top: 10px;">
        `;
    }
    
    ofertaModal.show();
}

async function eliminarOferta(ofertaId) {
    if (!confirm('¿Eliminar esta oferta?')) return;
    
    try {
        const response = await fetch(`/api/oferta/${ofertaId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            await cargarOfertasNegocio(currentNegocioId);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar oferta');
    }
}

function previewOfertaImage(input) {
    const preview = document.getElementById('ofertaImagePreview');
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" style="max-width: 150px; border-radius: 8px; margin-top: 10px;">`;
        };
        reader.readAsDataURL(input.files[0]);
    }
}
