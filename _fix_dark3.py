NEW_DARK = """/* DARK MODE */
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

c = open('templates/mis_cupones.html', encoding='utf-8').read()

start = c.find('/* DARK MODE */')
end_marker = '.dark-btn:hover{'
end = c.rfind(end_marker)
end = c.find('}', end) + 1

c = c[:start] + NEW_DARK + c[end:]
open('templates/mis_cupones.html', 'w', encoding='utf-8').write(c)
print('OK')
