"""
Módulo: gui.py
Descripción: Interfaz gráfica con tkinter para la aplicación de biblioteca.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from db import BaseDatos
import reportes
import chat_soporte


class VentanaPrincipal:
    """Ventana principal de la aplicación."""

    def __init__(self, root: tk.Tk, db: BaseDatos):
        self.root = root
        self.db = db
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Estilo
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        # Header
        self.crear_header()

        # Menú principal
        self.crear_menu_principal()

        # Frame central para cambiar contenido
        self.frame_contenido = ttk.Frame(self.root)
        self.frame_contenido.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def crear_header(self) -> None:
        """Crea la barra superior con información."""
        frame_header = ttk.Frame(self.root)
        frame_header.pack(fill=tk.X, padx=10, pady=10)

        lbl_titulo = ttk.Label(
            frame_header, text="📚 Sistema de Biblioteca UNAD",
            font=("Helvetica", 16, "bold")
        )
        lbl_titulo.pack(anchor=tk.W)

        # Estadísticas rápidas
        self.actualizar_estadisticas()

    def actualizar_estadisticas(self) -> None:
        """Actualiza y muestra estadísticas."""
        stats = self.db.obtener_estadisticas()
        info = (f"Libros: {stats['total_libros']} | "
                f"Disponibles: {stats['libros_disponibles']} | "
                f"Usuarios: {stats['total_usuarios']} | "
                f"Préstamos Activos: {stats['libros_prestados']}")

        # Eliminar etiqueta anterior si existe
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Label) and "Libros:" in str(widget.cget("text")):
                widget.destroy()

        lbl_stats = ttk.Label(
            self.root, text=info, font=("Helvetica", 10)
        )
        lbl_stats.pack(fill=tk.X, padx=10)

    def crear_menu_principal(self) -> None:
        """Crea el menú de opciones."""
        frame_menu = ttk.Frame(self.root)
        frame_menu.pack(fill=tk.X, padx=10, pady=5)

        botones = [
            ("📖 Libros", self.mostrar_libros),
            ("👤 Usuarios", self.mostrar_usuarios),
            ("📤 Préstamos", self.mostrar_prestamos),
            ("📊 Reportes", self.mostrar_reportes),
            ("🎧 Soporte en Línea", self.abrir_soporte),
        ]

        for texto, comando in botones:
            btn = ttk.Button(frame_menu, text=texto, command=comando)
            btn.pack(side=tk.LEFT, padx=5)

    def limpiar_contenido(self) -> None:
        """Limpia el frame de contenido."""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def mostrar_libros(self) -> None:
        """Muestra la interfaz de gestión de libros."""
        self.limpiar_contenido()

        # Frame superior con botones
        frame_botones = ttk.Frame(self.frame_contenido)
        frame_botones.pack(fill=tk.X, pady=5)

        ttk.Button(frame_botones, text="➕ Agregar Libro",
                   command=self.agregar_libro).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="✏️ Editar",
                   command=self.editar_libro).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🗑️ Eliminar",
                   command=self.eliminar_libro).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🔄 Actualizar",
                   command=self.actualizar_tabla_libros).pack(side=tk.LEFT, padx=2)

        # Tabla de libros
        frame_tabla = ttk.Frame(self.frame_contenido)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=5)

        columnas = ("ID", "ISBN", "Título", "Autor", "Año", "Género",
                   "Disponible")
        self.tabla_libros = ttk.Treeview(frame_tabla, columns=columnas,
                                         height=15)
        self.tabla_libros.column("#0", width=0, stretch=tk.NO)

        for col in columnas:
            self.tabla_libros.column(col, anchor=tk.W, width=120)
            self.tabla_libros.heading(col, text=col, anchor=tk.W)

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL,
                                  command=self.tabla_libros.yview)
        self.tabla_libros.configure(yscroll=scrollbar.set)

        self.tabla_libros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.actualizar_tabla_libros()

    def actualizar_tabla_libros(self) -> None:
        """Actualiza la tabla de libros."""
        for item in self.tabla_libros.get_children():
            self.tabla_libros.delete(item)

        libros = self.db.obtener_todos_libros()
        for libro in libros:
            disponible = "Sí" if libro[6] else "No"
            self.tabla_libros.insert(parent="", index="end", text="",
                                     values=(libro[0], libro[1], libro[2],
                                            libro[3], libro[4], libro[5],
                                            disponible))

    def agregar_libro(self) -> None:
        """Abre ventana para agregar libro."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Libro")
        ventana.geometry("400x300")

        ttk.Label(ventana, text="ISBN:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        entry_isbn = ttk.Entry(ventana)
        entry_isbn.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Título:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        entry_titulo = ttk.Entry(ventana)
        entry_titulo.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Autor:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        entry_autor = ttk.Entry(ventana)
        entry_autor.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Año:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        entry_anio = ttk.Entry(ventana)
        entry_anio.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Género:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        entry_genero = ttk.Entry(ventana)
        entry_genero.grid(row=4, column=1, padx=10, pady=5)

        def guardar():
            try:
                if self.db.agregar_libro(entry_isbn.get(), entry_titulo.get(),
                                        entry_autor.get(), int(entry_anio.get()),
                                        entry_genero.get()):
                    messagebox.showinfo("Éxito", "Libro agregado correctamente")
                    self.actualizar_tabla_libros()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "ISBN duplicado o error en datos")
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número")

        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=5,
                                                                   column=0,
                                                                   columnspan=2,
                                                                   pady=15)

    def editar_libro(self) -> None:
        """Edita el libro seleccionado."""
        seleccion = self.tabla_libros.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un libro")
            return

        item = self.tabla_libros.item(seleccion)
        valores = item["values"]
        id_libro = valores[0]

        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Libro")
        ventana.geometry("400x300")

        ttk.Label(ventana, text="Título:").grid(row=0, column=0, sticky=tk.W,
                                               padx=10, pady=5)
        entry_titulo = ttk.Entry(ventana)
        entry_titulo.insert(0, valores[2])
        entry_titulo.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Autor:").grid(row=1, column=0, sticky=tk.W,
                                              padx=10, pady=5)
        entry_autor = ttk.Entry(ventana)
        entry_autor.insert(0, valores[3])
        entry_autor.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Año:").grid(row=2, column=0, sticky=tk.W,
                                            padx=10, pady=5)
        entry_anio = ttk.Entry(ventana)
        entry_anio.insert(0, valores[4])
        entry_anio.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Género:").grid(row=3, column=0, sticky=tk.W,
                                               padx=10, pady=5)
        entry_genero = ttk.Entry(ventana)
        entry_genero.insert(0, valores[5])
        entry_genero.grid(row=3, column=1, padx=10, pady=5)

        def guardar():
            try:
                self.db.actualizar_libro(id_libro, entry_titulo.get(),
                                        entry_autor.get(),
                                        int(entry_anio.get()),
                                        entry_genero.get())
                messagebox.showinfo("Éxito", "Libro actualizado")
                self.actualizar_tabla_libros()
                ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos")

        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=4,
                                                                   column=0,
                                                                   columnspan=2,
                                                                   pady=15)

    def eliminar_libro(self) -> None:
        """Elimina el libro seleccionado."""
        seleccion = self.tabla_libros.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un libro")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar este libro?"):
            item = self.tabla_libros.item(seleccion)
            id_libro = item["values"][0]
            self.db.eliminar_libro(id_libro)
            messagebox.showinfo("Éxito", "Libro eliminado")
            self.actualizar_tabla_libros()

    def mostrar_usuarios(self) -> None:
        """Muestra la interfaz de gestión de usuarios."""
        self.limpiar_contenido()

        frame_botones = ttk.Frame(self.frame_contenido)
        frame_botones.pack(fill=tk.X, pady=5)

        ttk.Button(frame_botones, text="➕ Agregar Usuario",
                   command=self.agregar_usuario).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="✏️ Editar",
                   command=self.editar_usuario).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🗑️ Desactivar",
                   command=self.eliminar_usuario).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🔄 Actualizar",
                   command=self.actualizar_tabla_usuarios).pack(side=tk.LEFT, padx=2)

        frame_tabla = ttk.Frame(self.frame_contenido)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=5)

        columnas = ("ID", "Nombre", "Email", "Teléfono", "Activo")
        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=columnas,
                                          height=15)
        self.tabla_usuarios.column("#0", width=0, stretch=tk.NO)

        for col in columnas:
            self.tabla_usuarios.column(col, anchor=tk.W, width=150)
            self.tabla_usuarios.heading(col, text=col, anchor=tk.W)

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL,
                                  command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscroll=scrollbar.set)
        self.tabla_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.actualizar_tabla_usuarios()

    def actualizar_tabla_usuarios(self) -> None:
        """Actualiza tabla de usuarios."""
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        usuarios = self.db.obtener_todos_usuarios()
        for usuario in usuarios:
            activo = "Sí" if usuario[4] else "No"
            self.tabla_usuarios.insert(parent="", index="end", text="",
                                      values=(usuario[0], usuario[1], usuario[2],
                                             usuario[3], activo))

    def agregar_usuario(self) -> None:
        """Abre ventana para agregar usuario."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Usuario")
        ventana.geometry("400x250")

        ttk.Label(ventana, text="Nombre:").grid(row=0, column=0, sticky=tk.W,
                                               padx=10, pady=5)
        entry_nombre = ttk.Entry(ventana)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Email:").grid(row=1, column=0, sticky=tk.W,
                                              padx=10, pady=5)
        entry_email = ttk.Entry(ventana)
        entry_email.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Teléfono:").grid(row=2, column=0, sticky=tk.W,
                                                 padx=10, pady=5)
        entry_telefono = ttk.Entry(ventana)
        entry_telefono.grid(row=2, column=1, padx=10, pady=5)

        def guardar():
            if self.db.agregar_usuario(entry_nombre.get(), entry_email.get(),
                                      entry_telefono.get()):
                messagebox.showinfo("Éxito", "Usuario agregado")
                self.actualizar_tabla_usuarios()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Email duplicado o error")

        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=3,
                                                                   column=0,
                                                                   columnspan=2,
                                                                   pady=15)

    def editar_usuario(self) -> None:
        """Edita el usuario seleccionado."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return

        item = self.tabla_usuarios.item(seleccion)
        valores = item["values"]
        id_usuario = valores[0]

        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Usuario")
        ventana.geometry("400x250")

        ttk.Label(ventana, text="Nombre:").grid(row=0, column=0, sticky=tk.W,
                                               padx=10, pady=5)
        entry_nombre = ttk.Entry(ventana)
        entry_nombre.insert(0, valores[1])
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Email:").grid(row=1, column=0, sticky=tk.W,
                                              padx=10, pady=5)
        entry_email = ttk.Entry(ventana)
        entry_email.insert(0, valores[2])
        entry_email.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Teléfono:").grid(row=2, column=0, sticky=tk.W,
                                                 padx=10, pady=5)
        entry_telefono = ttk.Entry(ventana)
        entry_telefono.insert(0, valores[3])
        entry_telefono.grid(row=2, column=1, padx=10, pady=5)

        def guardar():
            self.db.actualizar_usuario(id_usuario, entry_nombre.get(),
                                      entry_email.get(), entry_telefono.get())
            messagebox.showinfo("Éxito", "Usuario actualizado")
            self.actualizar_tabla_usuarios()
            ventana.destroy()

        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=3,
                                                                   column=0,
                                                                   columnspan=2,
                                                                   pady=15)

    def eliminar_usuario(self) -> None:
        """Desactiva el usuario seleccionado."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return

        if messagebox.askyesno("Confirmar", "¿Desactivar este usuario?"):
            item = self.tabla_usuarios.item(seleccion)
            id_usuario = item["values"][0]
            self.db.eliminar_usuario(id_usuario)
            messagebox.showinfo("Éxito", "Usuario desactivado")
            self.actualizar_tabla_usuarios()

    def mostrar_prestamos(self) -> None:
        """Muestra la interfaz de préstamos."""
        self.limpiar_contenido()

        frame_botones = ttk.Frame(self.frame_contenido)
        frame_botones.pack(fill=tk.X, pady=5)

        ttk.Button(frame_botones, text="➕ Nuevo Préstamo",
                   command=self.crear_prestamo).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="↩️ Devolver Libro",
                   command=self.devolver_prestamo).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="⚠️ Ver Vencidos",
                   command=self.mostrar_vencidos).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🔄 Actualizar",
                   command=self.actualizar_tabla_prestamos).pack(side=tk.LEFT, padx=2)

        frame_tabla = ttk.Frame(self.frame_contenido)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=5)

        columnas = ("ID", "Libro", "Usuario", "Inicio", "Límite",
                   "Devuelto", "Activo")
        self.tabla_prestamos = ttk.Treeview(frame_tabla, columns=columnas,
                                           height=15)
        self.tabla_prestamos.column("#0", width=0, stretch=tk.NO)

        for col in columnas:
            self.tabla_prestamos.column(col, anchor=tk.W, width=120)
            self.tabla_prestamos.heading(col, text=col, anchor=tk.W)

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL,
                                  command=self.tabla_prestamos.yview)
        self.tabla_prestamos.configure(yscroll=scrollbar.set)
        self.tabla_prestamos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.actualizar_tabla_prestamos()

    def actualizar_tabla_prestamos(self) -> None:
        """Actualiza la tabla de préstamos."""
        for item in self.tabla_prestamos.get_children():
            self.tabla_prestamos.delete(item)

        prestamos = self.db.obtener_todos_prestamos()
        for p in prestamos:
            libro = self.db.obtener_libro(p[1])
            usuario = self.db.obtener_usuario(p[2])
            titulo_libro = libro[2] if libro else "Desconocido"
            nombre_usuario = usuario[1] if usuario else "Desconocido"
            activo = "Activo" if p[6] else "Cerrado"
            dev = p[5] if p[5] else "Pendiente"

            self.tabla_prestamos.insert(parent="", index="end", text="",
                                       values=(p[0], titulo_libro,
                                              nombre_usuario, p[3], p[4],
                                              dev, activo))

    def crear_prestamo(self) -> None:
        """Abre ventana para crear préstamo."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Préstamo")
        ventana.geometry("350x200")

        ttk.Label(ventana, text="Libro ID:").grid(row=0, column=0, sticky=tk.W,
                                                 padx=10, pady=5)
        entry_libro = ttk.Entry(ventana)
        entry_libro.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(ventana, text="Usuario ID:").grid(row=1, column=0, sticky=tk.W,
                                                   padx=10, pady=5)
        entry_usuario = ttk.Entry(ventana)
        entry_usuario.grid(row=1, column=1, padx=10, pady=5)

        def guardar():
            try:
                id_libro = int(entry_libro.get())
                id_usuario = int(entry_usuario.get())
                if self.db.crear_prestamo(id_libro, id_usuario):
                    messagebox.showinfo("Éxito", "Préstamo creado")
                    self.actualizar_tabla_prestamos()
                    self.actualizar_tabla_libros()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo crear préstamo")
            except ValueError:
                messagebox.showerror("Error", "IDs deben ser números")

        ttk.Button(ventana, text="Crear", command=guardar).grid(row=2, column=0,
                                                                columnspan=2,
                                                                pady=15)

    def devolver_prestamo(self) -> None:
        """Devuelve un préstamo seleccionado."""
        seleccion = self.tabla_prestamos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un préstamo")
            return

        item = self.tabla_prestamos.item(seleccion)
        id_prestamo = item["values"][0]

        if self.db.devolver_libro(id_prestamo):
            messagebox.showinfo("Éxito", "Libro devuelto")
            self.actualizar_tabla_prestamos()
            self.actualizar_tabla_libros()
        else:
            messagebox.showerror("Error", "No se pudo devolver el libro")

    def mostrar_vencidos(self) -> None:
        """Muestra préstamos vencidos."""
        vencidos = self.db.obtener_prestamos_vencidos()
        if not vencidos:
            messagebox.showinfo("Info", "No hay préstamos vencidos")
            return

        mensaje = "Préstamos vencidos:\n\n"
        for p in vencidos:
            libro = self.db.obtener_libro(p[1])
            usuario = self.db.obtener_usuario(p[2])
            titulo = libro[2] if libro else "Desconocido"
            nombre = usuario[1] if usuario else "Desconocido"
            dias_retraso = (date.today() - p[4]).days
            mensaje += (f"ID: {p[0]} | {titulo} | {nombre} | "
                       f"{dias_retraso} días de retraso\n")

        messagebox.showinfo("Préstamos Vencidos", mensaje)

    def mostrar_reportes(self) -> None:
        """Muestra opciones de reportes."""
        self.limpiar_contenido()

        frame = ttk.Frame(self.frame_contenido)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(frame, text="📊 Reportes y Estadísticas",
                 font=("Helvetica", 14, "bold")).pack(pady=10)

        botones_reportes = [
            ("📈 Resumen General", self.reporte_general),
            ("📊 Géneros Más Prestados", self.reporte_generos),
            ("⚠️ Préstamos Vencidos", self.reporte_vencidos),
        ]

        for texto, comando in botones_reportes:
            ttk.Button(frame, text=texto, command=comando,
                      width=30).pack(pady=10)

    def reporte_general(self) -> None:
        """Genera reporte general."""
        reportes.generar_reporte_general(self.db)
        messagebox.showinfo("Éxito", "Reporte generado: reporte_general.png")

    def reporte_generos(self) -> None:
        """Genera reporte de géneros."""
        reportes.generar_reporte_generos(self.db)
        messagebox.showinfo("Éxito", "Reporte generado: reporte_generos.png")

    def reporte_vencidos(self) -> None:
        """Genera reporte de vencidos."""
        vencidos = self.db.obtener_prestamos_vencidos()
        if not vencidos:
            messagebox.showinfo("Info", "No hay préstamos vencidos")
            return
        reportes.generar_reporte_vencidos(self.db, vencidos)
        messagebox.showinfo("Éxito", "Reporte generado: reporte_vencidos.png")

    def abrir_soporte(self) -> None:
        """Abre la ventana de chat de soporte técnico sincrónico."""
        chat_soporte.abrir_chat(self.root)
