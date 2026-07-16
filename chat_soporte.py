"""
Módulo: chat_soporte.py
Descripción: Ventana de chat con soporte técnico integrada a la aplicación
             de biblioteca. Implementa la comunicación cliente-servidor
             síncrona mediante sockets TCP en una interfaz gráfica tkinter.

             El usuario ingresa su NickName y puede intercambiar mensajes
             en tiempo real con el operador de soporte (servidor.py).
             Si el servidor no está disponible, se muestra un mensaje
             de error sin interrumpir la aplicación principal.
"""

import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# ── Configuración (debe coincidir con servidor.py) ─────────────────────────────
HOST = "127.0.0.1"
PORT = 65432
BUFFER = 4096


class VentanaChat(tk.Toplevel):
    """
    Ventana de chat de soporte técnico sincrónico.

    Hereda de Toplevel para abrirse sobre la ventana principal
    de la aplicación de biblioteca sin bloquearla.
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.title("🎧 Soporte Técnico en Línea")
        self.geometry("500x550")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")

        self.cliente: socket.socket | None = None
        self.nickname: str = ""
        self.conectado: bool = False

        self._construir_ui()
        # Impedir cierre accidental sin desconectar
        self.protocol("WM_DELETE_WINDOW", self._cerrar)

    # ── Construcción de la interfaz ────────────────────────────────────────────

    def _construir_ui(self) -> None:
        """Construye todos los elementos de la interfaz."""
        # Encabezado
        frame_header = tk.Frame(self, bg="#2c3e50", height=60)
        frame_header.pack(fill=tk.X)
        tk.Label(
            frame_header,
            text="🎧  Soporte Técnico Sincrónico",
            bg="#2c3e50", fg="white",
            font=("Helvetica", 13, "bold")
        ).pack(pady=15)

        # Panel de NickName y conexión
        frame_nick = ttk.LabelFrame(self, text="Conexión", padding=10)
        frame_nick.pack(fill=tk.X, padx=10, pady=8)

        ttk.Label(frame_nick, text="Tu NickName:").grid(
            row=0, column=0, sticky=tk.W, padx=5)
        self.entry_nick = ttk.Entry(frame_nick, width=22)
        self.entry_nick.grid(row=0, column=1, padx=5)

        self.btn_conectar = ttk.Button(
            frame_nick, text="Conectar", command=self._conectar)
        self.btn_conectar.grid(row=0, column=2, padx=5)

        self.btn_desconectar = ttk.Button(
            frame_nick, text="Desconectar",
            command=self._desconectar, state=tk.DISABLED)
        self.btn_desconectar.grid(row=0, column=3, padx=5)

        # Indicador de estado
        self.lbl_estado = ttk.Label(frame_nick, text="⚪ Sin conexión",
                                    foreground="gray")
        self.lbl_estado.grid(row=1, column=0, columnspan=4, pady=5)

        # Área de mensajes
        frame_chat = ttk.LabelFrame(self, text="Chat", padding=5)
        frame_chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.area_chat = scrolledtext.ScrolledText(
            frame_chat, state=tk.DISABLED, wrap=tk.WORD,
            font=("Helvetica", 10), bg="#ffffff", height=18
        )
        self.area_chat.pack(fill=tk.BOTH, expand=True)

        # Colores por tipo de mensaje
        self.area_chat.tag_configure("usuario", foreground="#2980b9",
                                     font=("Helvetica", 10, "bold"))
        self.area_chat.tag_configure("soporte", foreground="#27ae60",
                                     font=("Helvetica", 10, "bold"))
        self.area_chat.tag_configure("sistema", foreground="#7f8c8d",
                                     font=("Helvetica", 9, "italic"))

        # Barra de entrada de mensaje
        frame_entrada = ttk.Frame(self)
        frame_entrada.pack(fill=tk.X, padx=10, pady=8)

        self.entry_msg = ttk.Entry(frame_entrada, font=("Helvetica", 10))
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry_msg.bind("<Return>", lambda e: self._enviar())
        self.entry_msg.configure(state=tk.DISABLED)

        self.btn_enviar = ttk.Button(
            frame_entrada, text="Enviar ➤", command=self._enviar,
            state=tk.DISABLED)
        self.btn_enviar.pack(side=tk.RIGHT)

    # ── Lógica de conexión ─────────────────────────────────────────────────────

    def _conectar(self) -> None:
        """Intenta conectarse al servidor de soporte."""
        nick = self.entry_nick.get().strip()
        if not nick:
            messagebox.showwarning("Aviso", "Ingresa un NickName.")
            return

        self.nickname = nick
        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((HOST, PORT))
            self.cliente.sendall(self.nickname.encode("utf-8"))
            self.conectado = True
        except ConnectionRefusedError:
            messagebox.showerror(
                "Sin conexión",
                "⚠  El soporte no se encuentra activo en este momento.\n"
                "Por favor, intente más tarde."
            )
            self.cliente = None
            return
        except OSError as error:
            messagebox.showerror("Error", f"No se pudo conectar: {error}")
            self.cliente = None
            return

        # Actualizar UI
        self.lbl_estado.config(text="🟢 Conectado al soporte", foreground="#27ae60")
        self.btn_conectar.config(state=tk.DISABLED)
        self.btn_desconectar.config(state=tk.NORMAL)
        self.entry_nick.config(state=tk.DISABLED)
        self.entry_msg.config(state=tk.NORMAL)
        self.btn_enviar.config(state=tk.NORMAL)
        self.entry_msg.focus()

        self._agregar_mensaje(
            f"Conectado al soporte. Bienvenido, {self.nickname}.", "sistema")

        # Hilo para recibir mensajes
        hilo = threading.Thread(target=self._recibir, daemon=True)
        hilo.start()

    def _desconectar(self) -> None:
        """Cierra la conexión con el servidor."""
        self.conectado = False
        if self.cliente:
            try:
                self.cliente.close()
            except OSError:
                pass
            self.cliente = None

        self.lbl_estado.config(text="⚪ Sin conexión", foreground="gray")
        self.btn_conectar.config(state=tk.NORMAL)
        self.btn_desconectar.config(state=tk.DISABLED)
        self.entry_nick.config(state=tk.NORMAL)
        self.entry_msg.config(state=tk.DISABLED)
        self.btn_enviar.config(state=tk.DISABLED)
        self._agregar_mensaje("Sesión cerrada.", "sistema")

    def _cerrar(self) -> None:
        """Cierra la ventana asegurando desconexión previa."""
        if self.conectado:
            self._desconectar()
        self.destroy()

    # ── Comunicación ───────────────────────────────────────────────────────────

    def _recibir(self) -> None:
        """
        Bucle de recepción de mensajes (corre en hilo secundario).
        Actualiza la UI de forma segura con after().
        """
        while self.conectado:
            try:
                datos = self.cliente.recv(BUFFER)
                if not datos:
                    self.after(0, self._servidor_desconectado)
                    break
                mensaje = datos.decode("utf-8")
                if mensaje == "SERVIDOR_DESCONECTADO":
                    self.after(0, self._servidor_desconectado)
                    break
                self.after(0, self._agregar_mensaje,
                           f"[Soporte]: {mensaje}", "soporte")
            except OSError:
                if self.conectado:
                    self.after(0, self._servidor_desconectado)
                break

    def _enviar(self) -> None:
        """Envía el mensaje escrito por el usuario al servidor."""
        if not self.conectado or not self.cliente:
            return
        mensaje = self.entry_msg.get().strip()
        if not mensaje:
            return
        try:
            self.cliente.sendall(mensaje.encode("utf-8"))
            self._agregar_mensaje(f"[{self.nickname}]: {mensaje}", "usuario")
            self.entry_msg.delete(0, tk.END)
        except OSError:
            self._agregar_mensaje("Error al enviar mensaje.", "sistema")

    def _servidor_desconectado(self) -> None:
        """Maneja la desconexión inesperada del servidor."""
        self._agregar_mensaje(
            "El soporte ha cerrado la sesión.", "sistema")
        self._desconectar()

    # ── Utilidades ─────────────────────────────────────────────────────────────

    def _agregar_mensaje(self, texto: str, etiqueta: str = "") -> None:
        """
        Inserta un mensaje en el área de chat con la etiqueta de color.

        Args:
            texto:   Texto a mostrar.
            etiqueta: 'usuario', 'soporte' o 'sistema'.
        """
        self.area_chat.config(state=tk.NORMAL)
        self.area_chat.insert(tk.END, texto + "\n", etiqueta)
        self.area_chat.see(tk.END)
        self.area_chat.config(state=tk.DISABLED)


def abrir_chat(parent: tk.Tk) -> None:
    """
    Función de acceso rápido para abrir la ventana de chat
    desde la aplicación principal.

    Args:
        parent: Ventana raíz de la aplicación (tk.Tk).
    """
    VentanaChat(parent)


# ──────────────────────────────────────────────────────────────────────────────
# PRUEBAS
# ──────────────────────────────────────────────────────────────────────────────

# PRUEBA 1: Ventana se crea sin errores (requiere display gráfico)
# root = tk.Tk()
# root.withdraw()
# ventana = VentanaChat(root)
# assert ventana.winfo_exists(), "La ventana no se creó."
# print("[PRUEBA 1] PASÓ: Ventana de chat instanciada correctamente.")
# root.destroy()

# PRUEBA 2: Conexión rechazada muestra error sin crashear app
# (Ver comportamiento con servidor apagado en _conectar)
# Se valida visualmente al ejecutar con servidor inactivo.

# PRUEBA 3: _agregar_mensaje no lanza excepción con etiqueta válida
# root = tk.Tk(); root.withdraw()
# v = VentanaChat(root)
# v._agregar_mensaje("Hola mundo", "sistema")
# v._agregar_mensaje("Mensaje usuario", "usuario")
# v._agregar_mensaje("Respuesta soporte", "soporte")
# print("[PRUEBA 3] PASÓ: _agregar_mensaje sin errores.")
# root.destroy()
