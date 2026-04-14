
# Paleta dark mode suave:
# bg principal:  #18191f  (gris oscuro cálido, no negro puro)
# bg card:       #22232b  
# bg card hover: #2a2b35
# bg panel:      #1e1f27
# border:        #32333e
# texto:         #c8cad4  (blanco suave, no puro)
# texto muted:   #7c7f8e
# accent:        #8b8ff8  (morado suave)

INDEX = 'templates/index.html'
CUPONES = 'templates/mis_cupones.html'

INDEX_OLD = """        /* DARK MODE */
        [data-theme="dark"] body { background: #0f0f1a !important; color: #e0e0e0; }
        [data-theme="dark"] .oferta-card { background: #1e1e2e !important; border-color: #2d2d44 !important; color: #e0e0e0; }
        [data-theme="dark"] .card-title, [data-theme="dark"] .card-text { color: #e0e0e0 !important; }
        [data-theme="dark"] .negocio-chip { color: #aaa !important; }
        [data-theme="dark"] section.py-5 { background: #0f0f1a; }
        [data-theme="dark"] footer { background: #0a0a14 !important; }
        [data-theme="dark"] .form-select { background-color: #1e1e2e; color: #e0e0e0; border-color: #3d3d5c; }
        [data-theme="dark"] .filters-container { background: rgba(255,255,255,0.05) !important; }
        [data-theme="dark"] .precio-original { color: #888 !important; }
        [data-theme="dark"] .oferta-img-placeholder { background: #2d2d44 !important; }
        .dark-btn { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: white; border-radius: 8px; padding: 6px 12px; cursor: pointer; font-size: 0.9rem; transition: all 0.2s; }
        .dark-btn:hover { background: rgba(255,255,255,0.25); }"""

INDEX_NEW = """        /* DARK MODE */
        [data-theme="dark"] body { background: #18191f !important; color: #c8cad4; }
        [data-theme="dark"] .oferta-card { background: #22232b !important; border-color: #32333e !important; color: #c8cad4; box-shadow: 0 4px 20px rgba(0,0,0,0.25) !important; }
        [data-theme="dark"] .card-title { color: #dddfe8 !important; }
        [data-theme="dark"] .card-text { color: #9a9db0 !important; }
        [data-theme="dark"] .negocio-chip { color: #8b8ff8 !important; }
        [data-theme="dark"] section.py-5 { background: #18191f; }
        [data-theme="dark"] footer { background: #13141a !important; }
        [data-theme="dark"] .form-select { background-color: #22232b; color: #c8cad4; border-color: #32333e; }
        [data-theme="dark"] .filters-container { background: rgba(255,255,255,0.06) !important; }
        [data-theme="dark"] .precio-original { color: #6b6e82 !important; }
        [data-theme="dark"] .oferta-img-placeholder { background: #2a2b35 !important; color: #4a4d60 !important; }
        [data-theme="dark"] .precio-oferta { color: #6ee7b7 !important; }
        [data-theme="dark"] .badge-tiempo { background: #2a2b35 !important; color: #9a9db0 !important; }
        .dark-btn { background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.18); color: white; border-radius: 8px; padding: 6px 12px; cursor: pointer; font-size: 0.9rem; transition: all 0.2s; }
        .dark-btn:hover { background: rgba(255,255,255,0.2); }"""

CUPONES_OLD = """
        /* DARK MODE */
        [data-theme="dark"] body{background:#0f0f1a!important;color:#e0e0e0;}
        [data-theme="dark"] .page-head{background:#1e1e2e!important;border-color:#2d2d44!important;}
        [data-theme="dark"] .page-head h2{color:#e0e0e0!important;}
        [data-theme="dark"] .cupon-card{background:#1e1e2e!important;box-shadow:0 4px 20px rgba(0,0,0,.4)!important;}
        [data-theme="dark"] .notch{background:#0f0f1a!important;}
        [data-theme="dark"] .notch-line{border-color:#2d2d44!important;}
        [data-theme="dark"] .t-body{background:#1e1e2e;}
        [data-theme="dark"] .det-panel{background:#16162a!important;border-color:#2d2d44!important;}
        [data-theme="dark"] .det-item{background:#1e1e2e!important;border-color:#2d2d44!important;}
        [data-theme="dark"] .det-val{color:#e0e0e0!important;}
        [data-theme="dark"] .det-lbl{color:#888!important;}
        [data-theme="dark"] .btn-exp{border-color:#2d2d44!important;color:#a29bfe!important;}
        [data-theme="dark"] .btn-exp:hover{background:#2d2d44!important;}
        [data-theme="dark"] .cd-box.normal{background:#2d2a1a!important;border-color:#ffd43b!important;}
        [data-theme="dark"] .cd-box.urgente{background:#2d1a1a!important;}
        [data-theme="dark"] .p-orig{color:#666!important;}
        [data-theme="dark"] .empty h5{color:#666!important;}
        [data-theme="dark"] .empty p{color:#555!important;}
        [data-theme="dark"] .modal-content{background:#1e1e2e!important;}
        [data-theme="dark"] .mq-item{background:#16162a!important;}
        [data-theme="dark"] .mq-item .val{color:#e0e0e0!important;}
        [data-theme="dark"] .usuario-banner{background:linear-gradient(135deg,#1e1e3e,#16162e)!important;border-color:#4a4a8a!important;}
        .dark-btn{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);color:white;border-radius:8px;padding:6px 12px;cursor:pointer;font-size:.9rem;transition:all .2s;}
        .dark-btn:hover{background:rgba(255,255,255,.25);}"""

CUPONES_NEW = """
        /* DARK MODE */
        [data-theme="dark"] body{background:#18191f!important;color:#c8cad4;}
        [data-theme="dark"] .page-head{background:#22232b!important;border-color:#32333e!important;}
        [data-theme="dark"] .page-head h2{color:#dddfe8!important;}
        [data-theme="dark"] .page-head p{color:#7c7f8e!important;}
        [data-theme="dark"] .cupon-card{background:#22232b!important;box-shadow:0 4px 20px rgba(0,0,0,.25)!important;}
        [data-theme="dark"] .notch{background:#18191f!important;}
        [data-theme="dark"] .notch-line{border-color:#32333e!important;}
        [data-theme="dark"] .t-body{background:#22232b;}
        [data-theme="dark"] .det-panel{background:#1e1f27!important;border-color:#32333e!important;}
        [data-theme="dark"] .det-item{background:#22232b!important;border-color:#32333e!important;}
        [data-theme="dark"] .det-val{color:#c8cad4!important;}
        [data-theme="dark"] .det-lbl{color:#7c7f8e!important;}
        [data-theme="dark"] .det-item.hl{background:linear-gradient(135deg,#22243a,#1e2038)!important;border-color:#3a3d5c!important;}
        [data-theme="dark"] .det-item.hl .det-val{color:#8b8ff8!important;}
        [data-theme="dark"] .btn-exp{border-color:#32333e!important;color:#8b8ff8!important;}
        [data-theme="dark"] .btn-exp:hover{background:#2a2b35!important;}
        [data-theme="dark"] .cd-box.normal{background:#26241a!important;border-color:#b8960c!important;}
        [data-theme="dark"] .cd-box.normal .cd-time{color:#d4a017!important;}
        [data-theme="dark"] .cd-box.urgente{background:#261a1a!important;border-color:#c0392b!important;}
        [data-theme="dark"] .p-orig{color:#5a5d70!important;}
        [data-theme="dark"] .p-new{color:#6ee7b7!important;}
        [data-theme="dark"] .p-pct{background:linear-gradient(135deg,#c0392b,#e74c3c)!important;}
        [data-theme="dark"] .qr-thumb{border-color:#32333e!important;}
        [data-theme="dark"] .qr-hint{color:#5a5d70!important;}
        [data-theme="dark"] .btn-qr{box-shadow:none!important;}
        [data-theme="dark"] .empty i{color:#32333e!important;}
        [data-theme="dark"] .empty h5{color:#5a5d70!important;}
        [data-theme="dark"] .empty p{color:#4a4d60!important;}
        [data-theme="dark"] #qrModal .modal-content{background:#22232b!important;}
        [data-theme="dark"] .mq-item{background:#1e1f27!important;}
        [data-theme="dark"] .mq-item .lbl{color:#7c7f8e!important;}
        [data-theme="dark"] .mq-item .val{color:#c8cad4!important;}
        [data-theme="dark"] .mq-codigo{background:#1e1f27!important;color:#8b8ff8!important;border-color:#3a3d5c!important;}
        [data-theme="dark"] .usuario-banner{background:linear-gradient(135deg,#22243a,#1e2038)!important;border-color:#3a3d5c!important;}
        [data-theme="dark"] .usuario-nombre{color:#8b8ff8!important;}
        [data-theme="dark"] .usuario-lbl{color:#7c7f8e!important;}
        [data-theme="dark"] .text-muted{color:#7c7f8e!important;}
        .dark-btn{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);color:white;border-radius:8px;padding:6px 12px;cursor:pointer;font-size:.9rem;transition:all .2s;}
        .dark-btn:hover{background:rgba(255,255,255,.18);}"""

# Aplicar a index.html
ci = open(INDEX, encoding='utf-8').read()
if INDEX_OLD in ci:
    ci = ci.replace(INDEX_OLD, INDEX_NEW)
    print('index.html dark CSS OK')
else:
    print('index.html: no encontrado el bloque viejo')
open(INDEX, 'w', encoding='utf-8').write(ci)

# Aplicar a mis_cupones.html
cc = open(CUPONES, encoding='utf-8').read()
if CUPONES_OLD in cc:
    cc = cc.replace(CUPONES_OLD, CUPONES_NEW)
    print('mis_cupones.html dark CSS OK')
else:
    print('mis_cupones.html: no encontrado, buscando parcial...')
    # Buscar y reemplazar solo el bloque de dark mode
    start = cc.find('/* DARK MODE */')
    end = cc.find('.dark-btn:hover{background:rgba(255,255,255,.25);}')
    if start > 0 and end > 0:
        end += len('.dark-btn:hover{background:rgba(255,255,255,.25);}')
        cc = cc[:start] + CUPONES_NEW.strip() + cc[end:]
        print('mis_cupones.html: reemplazado por posicion OK')
    else:
        print(f'start={start}, end={end}')
open(CUPONES, 'w', encoding='utf-8').write(cc)
