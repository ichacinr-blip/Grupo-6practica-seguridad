import socket

def escaneo_puertos_basico(host, puertos):
    print(f"\n=== MÓDULO DE ESCANEO DE RED COMPLEMENTARIO ===")
    print(f"Escaneando objetivo: {host}")
    for puerto in puertos:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        resultado = sock.connect_ex((host, puerto))
        if resultado == 0:
            print(f"[+] Puerto {puerto}: ABIERTO")
        else:
            print(f"[-] Puerto {puerto}: CERRADO / FILTRADO")
        sock.close()

def recomendaciones_hardening_bd():
    print("\n=== MÓDULO DE RECOMENDACIONES DE HARDENING EN BD RELACIONALES ===")
    hardening_steps = [
        "1. Principio de Menor Privilegio: Asegurar que el usuario de la BD solo tenga permisos SELECT/INSERT/UPDATE estrictamente necesarios.",
        "2. Consultas Parametrizadas: Prohibir la concatenación de entradas de usuario en sentencias SQL.",
        "3. Cifrado de Datos: Encriptar contraseñas utilizando algoritmos robustos como bcrypt o Argon2.",
        "4. Aislamiento de Red: Restringir el acceso a la base de datos únicamente a IPs del servidor web mediante reglas de Firewall.",
        "5. Auditoría y Logs: Habilitar el registro de eventos y monitoreo de consultas anómalas."
    ]
    for step in hardening_steps:
        print(step)

if __name__ == '__main__':
    # Escaneo local de prueba
    escaneo_puertos_basico('127.0.0.1', [80, 443, 5000, 3306, 5432])
    recomendaciones_hardening_bd()