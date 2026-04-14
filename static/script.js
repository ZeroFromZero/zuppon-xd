document.addEventListener('DOMContentLoaded', async () => {
    await cargarCiudadesFiltro();
    cargarOfertas();
});

async function cargarCiudadesFiltro() {
    try {
        const res = await fetch('/api/ciudades');
        const ciudades = await res.json();
        const sel = document.getElementById('ciudadFilter');
        ciudades.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.nombre;
            opt.textContent = '📍 ' + c.nombre;
            sel.appendChild(opt);
        });
    } catch (e) { console.error('Error al cargar ciudades:', e); }
}

async function cargarOfertas() {
    // Leer chip activo en lugar del select de categoría
    const chipActivo = document.querySelector('#chipsCategoria .chip.active');
    const categoria = chipActivo ? chipActivo.dataset.value : 'todos';
    const orden = document.getElementById('ordenFilter').value;
    const ciudad = document.getElementById('ciudadFilter').value;
    try {
        const res = await fetch(`/api/ofertas_home?categoria=${categoria}&orden=${orden}&ciudad=${ciudad}`);
        const ofertas = await res.json();
        mostrarOfertas(ofertas);
    } catch (error) {
        console.error('Error al cargar:', error);
    }
}

function calcularPctModal(original, oferta) {
    if (!original || !oferta) return '';
    const orig = parseFloat(original.replace(/[^0-9]/g, ''));
    const ofer = parseFloat(oferta.replace(/[^0-9]/g, ''));
    if (!orig || !ofer || orig <= ofer) return '';
    const pct = Math.round(((orig - ofer) / orig) * 100);
    return `<span style="background:#ff4757;color:white;border-radius:20px;padding:2px 10px;font-size:0.85rem;font-weight:800;">-${pct}% OFF</span>`;
}

function calcularPorcentaje(original, oferta) {
    const orig = parseFloat(original.replace(/[^0-9.]/g, ''));
    const ofer = parseFloat(oferta.replace(/[^0-9.]/g, ''));
    if (!orig || !ofer) return null;
    return Math.round(((orig - ofer) / orig) * 100);
}

// Colores por categoría (para el dot y el thumb bg)
const CAT_COLORS = {
    'Restaurante':'#EF4444','Cafetería':'#F59E0B','Gimnasio':'#10B981',
    'Deportes':'#3B82F6','Educación':'#8B5CF6','Moda':'#EC4899',
    'Peluquería':'#F97316','Salud':'#06B6D4','Spa':'#A855F7',
    'Panadería':'#F59E0B','Farmacia':'#22C55E','Veterinaria':'#A16207',
    'Ferretería':'#64748B','Otro':'#7C3AED'
};

// Emojis por categoría
const CAT_EMOJIS = {
    'Restaurante':'🍽️','Cafetería':'☕','Gimnasio':'💪','Deportes':'⚽',
    'Educación':'📚','Moda':'👗','Peluquería':'✂️','Salud':'🏥',
    'Spa':'🧖','Panadería':'🥐','Farmacia':'💊','Veterinaria':'🐾',
    'Ferretería':'🔧','Otro':'🏪'
};

function mostrarOfertas(ofertas) {
    const container = document.getElementById('ofertasContainer');
    if (window._cdIntervals) window._cdIntervals.forEach(clearInterval);
    window._cdIntervals = [];
    container.innerHTML = '';

    // Si hay filtro de categoría activo, usar layout de columna única
    const chipActivo = document.querySelector('#chipsCategoria .chip.active');
    const categoriaActiva = chipActivo ? chipActivo.dataset.value : 'todos';
    const esFiltrado = categoriaActiva !== 'todos';
    container.classList.toggle('feed-single', esFiltrado);

    if (ofertas.length === 0) {
        container.innerHTML = `<div class="loading">
            <span style="font-size:2.5rem;display:block;margin-bottom:10px;">🔍</span>
            No hay ofertas disponibles
        </div>`;
        return;
    }

    ofertas.forEach((oferta, index) => {
        const pct       = calcularPorcentaje(oferta.precio_original, oferta.precio_oferta);
        const badgeText = pct ? `-${pct}%` : 'OFERTA';
        const imgSrc    = oferta.negocio_imagen || '';
        const cdId      = `cd-${oferta.id}`;
        const emoji     = CAT_EMOJIS[oferta.categoria] || '🏪';
        const catColor  = CAT_COLORS[oferta.categoria] || '#7C3AED';
        const thumbBg   = catColor + '22';   /* 13% opacidad */

        function fmtCountdown(ms) {
            if (ms <= 0) return 'Expirada';
            const s = Math.floor(ms / 1000);
            const d = Math.floor(s / 86400);
            const h = Math.floor((s % 86400) / 3600);
            const m = Math.floor((s % 3600) / 60);
            const sc = s % 60;
            if (d > 0) return `${d}d ${h}h`;
            return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(sc).padStart(2,'0')}`;
        }

        const vencimiento = oferta.fecha_vencimiento ? new Date(oferta.fecha_vencimiento) : null;
        const tiempoTexto = vencimiento
            ? fmtCountdown(vencimiento - new Date())
            : (oferta.duracion_horas ? `${oferta.duracion_horas}h` : '48h');

        if (vencimiento) {
            const iv = setInterval(() => {
                const el = document.getElementById(cdId);
                if (!el) { clearInterval(iv); return; }
                const rem = vencimiento - new Date();
                el.textContent = '⏱ ' + fmtCountdown(rem);
                if (rem <= 0) clearInterval(iv);
            }, 1000);
            window._cdIntervals.push(iv);
        }

        const card = document.createElement('div');
        card.style.animation = `fadeUp 0.3s ease ${Math.min(index * 0.04, 0.4)}s both`;

        const isFeatured = (index % 6 === 2);   // cada 6ta card es destacada

        if (isFeatured) {
            card.className = 'oferta-card featured';
            card.onclick = () => window.location = `/negocio/${oferta.negocio_id}`;
            card.innerHTML = `
                <div class="featured-img-wrap">
                    ${imgSrc
                        ? `<img src="${imgSrc}" alt="${oferta.nombre}">`
                        : `<div class="featured-img-placeholder">${emoji}</div>`}
                    <div class="featured-overlay"></div>
                </div>
                <div class="featured-body">
                    <div class="featured-cat-chip">
                        <span style="width:6px;height:6px;border-radius:50%;background:${catColor};display:inline-block;"></span>
                        ${oferta.categoria}
                    </div>
                    <div class="featured-title">${oferta.nombre}</div>
                    <div class="featured-desc">${oferta.descripcion || ''}</div>
                    <div class="featured-footer">
                        <span class="featured-price-original">${oferta.precio_original}</span>
                        <span class="featured-price-offer">${oferta.precio_oferta}</span>
                        <span class="featured-badge">${badgeText}</span>
                        <span class="featured-time" id="${cdId}">⏱ ${tiempoTexto}</span>
                    </div>
                </div>`;
        } else {
            card.className = 'oferta-card';
            card.onclick = () => window.location = `/negocio/${oferta.negocio_id}`;
            card.innerHTML = `
                <div class="card-thumb" style="background:${thumbBg};">
                    ${imgSrc
                        ? `<img src="${imgSrc}" alt="${oferta.negocio_nombre}">`
                        : `<div class="card-thumb-placeholder">${emoji}</div>`}
                </div>
                <div class="card-body">
                    <div class="card-meta">
                        <span class="card-cat-dot" style="background:${catColor};"></span>
                        <span class="card-business">${oferta.negocio_nombre}</span>
                    </div>
                    <div class="card-title">${oferta.nombre}</div>
                    <div class="card-desc">${oferta.descripcion || oferta.categoria}</div>
                    <div class="card-prices">
                        <span class="price-original">${oferta.precio_original}</span>
                        <span class="price-offer">${oferta.precio_oferta}</span>
                    </div>
                </div>
                <div class="card-right">
                    <span class="badge-pct">${badgeText}</span>
                    <span class="badge-time" id="${cdId}">⏱ ${tiempoTexto}</span>
                </div>`;
        }

        container.appendChild(card);
    });
}

async function reclamarOferta(ofertaId) {
    const btn = event.currentTarget;
    if (btn.disabled) return;
    btn.disabled = true;
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generando...';
    try {
        // Verificar si ya tiene un cupón para esta oferta en localStorage
        const cupones = JSON.parse(localStorage.getItem('mis_cupones') || '[]');
        const ahora = new Date();

        // Si tiene uno activo → mostrar el que ya tiene
        const yaActivo = cupones.find(c =>
            c.oferta_id == ofertaId &&
            !c.canjeado &&
            new Date(c.expira_en) > ahora
        );
        if (yaActivo) {
            mostrarModalCupon(yaActivo);
            return;
        }

        // Si tiene uno aún no expirado (canjeado) → bloquear
        const bloqueado = cupones.find(c =>
            c.oferta_id == ofertaId &&
            new Date(c.expira_en) > ahora
        );
        if (bloqueado) {
            mostrarAlertaCupon('Ya tenés un cupón activo para esta oferta. Revisá Mis Cupones.');
            return;
        }

        const res = await fetch('/api/reclamar_oferta', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({oferta_id: ofertaId})
        });
        const data = await res.json();
        if (data.success) {
            // Guardar en localStorage
            const cuponesActualizados = JSON.parse(localStorage.getItem('mis_cupones') || '[]');
            cuponesActualizados.unshift(data.cupon);
            localStorage.setItem('mis_cupones', JSON.stringify(cuponesActualizados));
            mostrarModalCupon(data.cupon);
        } else {
            mostrarAlertaCupon(data.message || 'Error al reclamar');
        }
    } catch (e) {
        console.error(e);
        alert('Error de conexión. Intentá de nuevo.');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
    }
}

function mostrarModalCupon(cupon) {
    // Crear modal dinámico
    const existing = document.getElementById('cuponModal');
    if (existing) existing.remove();

    const waMsg = encodeURIComponent(`✨ Quiero reclamar mi cupón: ${cupon.oferta_nombre}\nCódigo: ${cupon.codigo}\nPrecio: ${cupon.precio_oferta}`);
    const waUrl = `https://wa.me/${cupon.negocio_whatsapp}?text=${waMsg}`;

    const modal = document.createElement('div');
    modal.id = 'cuponModal';
    modal.innerHTML = `
        <div class="modal fade" id="cuponModalBS" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content" style="border-radius:20px;overflow:hidden;background:#1A1A1A;border:1px solid rgba(255,255,255,0.08);">
                    <div class="modal-header border-0 text-white" style="background:linear-gradient(90deg,#6C00FF,#FF006E);padding:16px 20px;">
                        <h5 class="modal-title fw-bold" style="font-size:1rem;"><i class="fas fa-ticket-alt me-2"></i>Cupón generado</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center p-4">
                        <p style="color:rgba(255,255,255,0.5);font-size:0.82rem;margin-bottom:4px;">${cupon.negocio_nombre}</p>
                        <p style="color:white;font-weight:800;font-size:1rem;margin-bottom:16px;">${cupon.oferta_nombre}</p>
                        <div style="font-family:monospace;font-size:1.6rem;font-weight:900;letter-spacing:6px;background:rgba(108,0,255,0.15);border:1px solid rgba(108,0,255,0.4);border-radius:12px;padding:10px 20px;display:inline-block;margin-bottom:16px;color:white;">
                            ${cupon.codigo}
                        </div>
                        <br>
                        <img src="data:image/png;base64,${cupon.qr_base64}" style="width:160px;height:160px;border-radius:12px;border:2px solid rgba(255,255,255,0.1);" class="mb-3">
                        <div style="margin-bottom:8px;">
                            ${cupon.precio_original ? `<span style="text-decoration:line-through;color:rgba(255,255,255,0.4);font-size:0.9rem;margin-right:8px;">${cupon.precio_original}</span>` : ''}
                            ${calcularPctModal(cupon.precio_original, cupon.precio_oferta)}
                        </div>
                        <p style="color:#00E676;font-weight:900;font-size:1.6rem;margin-bottom:4px;">${cupon.precio_oferta}</p>
                        <p style="color:rgba(255,255,255,0.4);font-size:0.78rem;"><i class="fas fa-clock me-1"></i>Válido por 24 horas</p>
                        <div style="margin-top:14px;padding:12px 16px;border-radius:12px;background:rgba(0,230,118,0.1);border:1px solid rgba(0,230,118,0.25);">
                            <p style="margin-bottom:6px;color:#00E676;font-weight:700;font-size:0.85rem;"><i class="fab fa-whatsapp me-1"></i>Redirigiendo a WhatsApp en <span id="waCountdown">3</span>s...</p>
                            <div style="height:3px;background:rgba(255,255,255,0.1);border-radius:2px;overflow:hidden;">
                                <div id="waProgress" style="height:100%;width:100%;background:#00E676;transition:width 3s linear;border-radius:2px;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer border-0 justify-content-center" style="padding:12px 20px 20px;gap:8px;">
                        <a href="/usuario/cupones" style="background:rgba(108,0,255,0.2);border:1px solid rgba(108,0,255,0.4);color:white;border-radius:12px;padding:9px 16px;text-decoration:none;font-weight:700;font-size:0.82rem;">
                            <i class="fas fa-ticket-alt me-1"></i>Mis cupones
                        </a>
                        <a href="${waUrl}" target="_blank" style="background:rgba(0,230,118,0.15);border:1px solid rgba(0,230,118,0.3);color:#00E676;border-radius:12px;padding:9px 16px;text-decoration:none;font-weight:700;font-size:0.82rem;">
                            <i class="fab fa-whatsapp me-1"></i>WhatsApp
                        </a>
                        <button data-bs-dismiss="modal" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);color:rgba(255,255,255,0.6);border-radius:12px;padding:9px 16px;font-weight:700;font-size:0.82rem;cursor:pointer;">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(document.getElementById('cuponModalBS'));
    bsModal.show();

    // Countdown 3s → WhatsApp
    let secs = 3;
    setTimeout(() => { document.getElementById('waProgress').style.width = '0%'; }, 50);
    const interval = setInterval(() => {
        secs--;
        const el = document.getElementById('waCountdown');
        if (el) el.textContent = secs;
        if (secs <= 0) {
            clearInterval(interval);
            window.open(waUrl, '_blank');
        }
    }, 1000);

    // Cancelar countdown si cierra el modal
    document.getElementById('cuponModalBS').addEventListener('hidden.bs.modal', () => clearInterval(interval));
}

function mostrarAlertaCupon(msg) {
    const existing = document.getElementById('alertaCupon');
    if (existing) existing.remove();
    const div = document.createElement('div');
    div.id = 'alertaCupon';
    div.className = 'alert alert-info alert-dismissible fade show position-fixed bottom-0 end-0 m-3';
    div.style.zIndex = 9999;
    div.innerHTML = `<i class="fas fa-info-circle me-2"></i>${msg} <a href="/usuario/cupones" class="alert-link">Ver mis cupones</a>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    document.body.appendChild(div);
    setTimeout(() => div.remove(), 5000);
}
