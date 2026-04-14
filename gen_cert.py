"""Genera certificado SSL autofirmado para HTTPS local"""
from OpenSSL import crypto
import socket

# Obtener IP WiFi
def get_wifi_ip():
    try:
        hostname = socket.gethostname()
        ips = socket.getaddrinfo(hostname, None, socket.AF_INET)
        all_ips = list(set(r[4][0] for r in ips))
        for prefix in ('192.168.', '10.', '172.'):
            match = next((ip for ip in all_ips if ip.startswith(prefix)), None)
            if match:
                return match
    except:
        pass
    return '127.0.0.1'

ip = get_wifi_ip()

k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 2048)

cert = crypto.X509()
cert.get_subject().CN = ip
cert.set_serial_number(1)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # 1 año
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)

# SAN para que funcione en móviles
san = f"IP:{ip},IP:127.0.0.1".encode()
cert.add_extensions([
    crypto.X509Extension(b"subjectAltName", False, san),
    crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE"),
])
cert.sign(k, 'sha256')

with open('cert.pem', 'wb') as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
with open('key.pem', 'wb') as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

print(f"Certificado generado para IP: {ip}")
print("Archivos: cert.pem, key.pem")
