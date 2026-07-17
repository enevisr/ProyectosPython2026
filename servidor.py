"""
Módulo: servidor.py
Descripción: Programa servidor para el módulo de soporte sincrónico.
             Crea un socket TCP, acepta conexiones de clientes y permite
             el intercambio de mensajes en tiempo real entre el soporte
             técnico y los usuarios de la biblioteca.

Uso:
    python servidor.py

El servidor queda en espera de conexiones en HOST:PORT definidos abajo.
Escribe mensajes en la consola y presiona Enter para enviarlos al cliente.
Escribe 'salir' para cerrar la sesión actual.
"""

import socket
import threading

# ── Configuración ──────────────────────────────────────────────────────────────
HOST = "127.0.0.1"   # Dirección local (localhost)
PORT = 65433         # Puerto de escucha
BUFFER = 4096        # Tamaño del buffer de recepción


def manejar_cliente(conn: socket.socket, addr: tuple) -> None:
    """
    Gestiona la comunicación con un cliente conectado.

    Args:
        conn: Objeto socket de la conexión aceptada.
        addr: Tupla (IP, puerto) del cliente.
    """
    print(f"\n[SERVIDOR] Cliente conectado desde {addr}")

    # Recibir el NickName del cliente
    try:
        nickname = conn.recv(BUFFER).decode("utf-8").strip()
        if not nickname:
            nickname = "Usuario"
        print(f"[SERVIDOR] NickName del usuario: {nickname}")
        print("[SERVIDOR] Escribe un mensaje y presiona Enter. Escribe 'salir' para cerrar.\n")
    except OSError:
        conn.close()
        return

    # Hilo para recibir mensajes del cliente
    def recibir():
        while True:
            try:
                datos = conn.recv(BUFFER)
                if not datos:
                    print(f"\n[SERVIDOR] {nickname} ha cerrado la conexión.")
                    break
                mensaje = datos.decode("utf-8")
                print(f"\n[{nickname}]: {mensaje}")
                print("[Soporte]: ", end="", flush=True)
            except OSError:
                break

    hilo_recibir = threading.Thread(target=recibir, daemon=True)
    hilo_recibir.start()

    # Bucle de envío desde la consola del soporte
    while True:
        try:
            respuesta = input("[Soporte]: ")
            if respuesta.strip().lower() == "salir":
                conn.sendall("SERVIDOR_DESCONECTADO".encode("utf-8"))
                break
            if respuesta:
                conn.sendall(respuesta.encode("utf-8"))
        except (EOFError, KeyboardInterrupt):
            break
        except OSError:
            break

    print(f"[SERVIDOR] Cerrando sesión con {nickname}.")
    conn.close()


def iniciar_servidor() -> None:
    """
    Inicializa el socket del servidor y entra en el bucle de aceptación
    de conexiones. Gestiona las excepciones en caso de que el servidor
    no pueda iniciarse (puerto ocupado, permisos, etc.).
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((HOST, PORT))
            servidor.listen(5)
            print("=" * 60)
            print("  SOPORTE TÉCNICO SINCRÓNICO — SERVIDOR CEIPA")
            print("=" * 60)
            print(f"  Escuchando en {HOST}:{PORT}")
            print("  Esperando conexión de un usuario...")
            print("=" * 60)

            while True:
                try:
                    conn, addr = servidor.accept()
                    # Cada cliente en su propio hilo
                    hilo = threading.Thread(
                        target=manejar_cliente, args=(conn, addr), daemon=True
                    )
                    hilo.start()
                except KeyboardInterrupt:
                    print("\n[SERVIDOR] Servidor detenido por el operador.")
                    break

    except OSError as error:
        print(f"\n[ERROR] No se pudo iniciar el servidor: {error}")
        print("Posibles causas:")
        print(f"  • El puerto {PORT} ya está en uso.")
        print("  • No tiene permisos suficientes.")
        print("Solución: Cierre otras instancias del servidor e intente de nuevo.")


# ──────────────────────────────────────────────────────────────────────────────
# PRUEBAS (ejecutar con el servidor levantado en otra terminal)
# ──────────────────────────────────────────────────────────────────────────────

# PRUEBA 1: Inicio correcto del servidor
# servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
#     servidor.bind((HOST, PORT))
#     servidor.listen(1)
#     print("[PRUEBA 1] PASÓ: Servidor iniciado correctamente.")
#     servidor.close()
# except OSError as e:
#     print(f"[PRUEBA 1] FALLÓ: {e}")

# PRUEBA 2: Puerto ocupado genera excepción controlada
# servidor1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# servidor2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
#     servidor1.bind((HOST, PORT))
#     servidor1.listen(1)
#     servidor2.bind((HOST, PORT))  # Debe fallar
#     print("[PRUEBA 2] FALLÓ: No lanzó excepción")
# except OSError:
#     print("[PRUEBA 2] PASÓ: Excepción controlada al intentar puerto ocupado.")
# finally:
#     servidor1.close()
#     servidor2.close()


if __name__ == "__main__":
    iniciar_servidor()
