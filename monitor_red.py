import subprocess
import platform
import datetime
import time
import os

# ── CONFIGURACIÓN ──────────────────────────────────────
HOSTS = [
    {"nombre": "Google DNS",      "ip": "8.8.8.8"},
    {"nombre": "Cloudflare DNS",  "ip": "1.1.1.1"},
    {"nombre": "Router local",    "ip": "192.168.1.1"},
    {"nombre": "Servidor web lab","ip": "192.168.1.100"},
]

INTERVALO_SEGUNDOS = 10   # cada cuánto revisa
LOG_FILE = "monitor_red.log"
# ───────────────────────────────────────────────────────


def ping(ip):
    """Devuelve True si el host responde, False si no."""
    sistema = platform.system().lower()
    if sistema == "windows":
        cmd = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]
    
    resultado = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return resultado.returncode == 0


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def escribir_log(mensaje):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(mensaje + "\n")


def revisar_hosts():
    print(f"\n[{timestamp()}] Revisando {len(HOSTS)} hosts...")
    print("-" * 50)

    for host in HOSTS:
        nombre = host["nombre"]
        ip     = host["ip"]
        estado = ping(ip)

        if estado:
            estado_txt = "✅ UP"
            color      = "\033[92m"  # verde
        else:
            estado_txt = "❌ DOWN"
            color      = "\033[91m"  # rojo

        reset = "\033[0m"
        linea = f"[{timestamp()}] {estado_txt}  {nombre} ({ip})"

        print(f"{color}{linea}{reset}")
        escribir_log(linea)

        if not estado:
            alerta = f"[{timestamp()}] ⚠️  ALERTA: {nombre} ({ip}) no responde"
            print(f"\033[93m{alerta}{reset}")
            escribir_log(alerta)

    print("-" * 50)


# ── MAIN ───────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("   Monitor de Red — Bryan Carreño")
    print(f"   Revisando cada {INTERVALO_SEGUNDOS} segundos")
    print(f"   Log: {LOG_FILE}")
    print("   Ctrl+C para detener")
    print("=" * 50)

    escribir_log(f"\n{'='*50}")
    escribir_log(f"Sesión iniciada: {timestamp()}")
    escribir_log(f"{'='*50}")

    try:
        while True:
            revisar_hosts()
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        mensaje = f"[{timestamp()}] Monitor detenido por el usuario."
        print(f"\n{mensaje}")
        escribir_log(mensaje)