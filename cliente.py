"""
Módulo: cliente.py
Descripción: Programa cliente para el módulo de soporte sincrónico.
             Solicita un NickName al usuario, se conecta al servidor y
             permite el intercambio de mensajes en tiempo real.
             En caso de que el servidor no esté disponible, controla la
             excepción y notifica al usuario.

Uso:
    python cliente.py

Asegúrese de que el servidor (servidor.py) esté corriendo antes de iniciar.
"""

import socket
import threading

# ── Configuración (debe coincidir con servidor.py) ─────────────────────────────
HOST = "127.0.0.1"
PORT = 65432
BUFFER = 4096


def iniciar_cliente() -> None:
    """
    Solicita el NickName al usuario, conecta con el servidor y gestiona
    el intercambio de mensajes. Controla la excepción cuando el servidor
    no está disponible.
    """
    print("=" * 60)
    print("  SOPORTE TÉCNICO SINCRÓNICO — CLIENTE")
    print("=" * 60)

    nickname = input("Ingresa tu NickName: ").strip()
    if not nickname:
        nickname = "Usuario"

    # Intentar conectar al servidor
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("\n⚠  El soporte no se encuentra activo en este momento.")
        print("   Por favor, intente más tarde o contacte al administrador.")
        return
    except OSError as error:
        print(f"\n⚠  No se pudo conectar al servidor: {error}")
        return

    # Enviar el NickName al servidor
    cliente.sendall(nickname.encode("utf-8"))

    print(f"\n✓  Conectado al soporte. Bienvenido, {nickname}.")
    print("   Escribe tu mensaje y presiona Enter.")
    print("   Escribe 'salir' para cerrar la sesión.\n")

    # Hilo para recibir mensajes del servidor
    def recibir():
        while True:
            try:
                datos = cliente.recv(BUFFER)
                if not datos:
                    print("\n[SISTEMA] El soporte ha cerrado la sesión.")
                    break
                mensaje = datos.decode("utf-8")
                if mensaje == "SERVIDOR_DESCONECTADO":
                    print("\n[SISTEMA] El soporte ha cerrado la sesión. Hasta luego.")
                    break
                print(f"\n[Soporte]: {mensaje}")
                print(f"[{nickname}]: ", end="", flush=True)
            except OSError:
                break

    hilo_recibir = threading.Thread(target=recibir, daemon=True)
    hilo_recibir.start()

    # Bucle de envío desde el teclado del usuario
    while True:
        try:
            mensaje = input(f"[{nickname}]: ")
            if mensaje.strip().lower() == "salir":
                print("[SISTEMA] Cerrando sesión...")
                break
            if mensaje:
                cliente.sendall(mensaje.encode("utf-8"))
        except (EOFError, KeyboardInterrupt):
            break
        except OSError:
            break

    cliente.close()
    print("[SISTEMA] Desconectado.")


# ──────────────────────────────────────────────────────────────────────────────
# PRUEBAS
# ──────────────────────────────────────────────────────────────────────────────

# PRUEBA 1: Servidor no disponible → excepción controlada
# try:
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(("127.0.0.1", 9999))   # Puerto que nadie escucha
#     print("[PRUEBA 1] FALLÓ: Se esperaba ConnectionRefusedError")
# except ConnectionRefusedError:
#     print("[PRUEBA 1] PASÓ: Excepción controlada correctamente.")
# finally:
#     s.close()

# PRUEBA 2: Envío y recepción de cadena de texto
# (requiere servidor activo)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
#     s.connect((HOST, PORT))
#     s.sendall("TestNick".encode("utf-8"))
#     s.sendall("Mensaje de prueba".encode("utf-8"))
#     respuesta = s.recv(BUFFER)
#     assert len(respuesta) >= 0, "Sin respuesta del servidor"
#     print("[PRUEBA 2] PASÓ: Comunicación establecida.")
# except Exception as e:
#     print(f"[PRUEBA 2] FALLÓ: {e}")
# finally:
#     s.close()


if __name__ == "__main__":
    iniciar_cliente()
