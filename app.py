"""
Módulo: app.py
Descripción: Punto de entrada para la aplicación de gestión de biblioteca.
             Inicia la interfaz gráfica con tkinter.
"""

import tkinter as tk
from db import BaseDatos
from gui import VentanaPrincipal


def main():
    """Punto de entrada principal de la aplicación. Con los detalles"""
    # Crear instancia de base de datos
    db = BaseDatos("biblioteca.db")

    # Crear ventana principal
    root = tk.Tk()
    app = VentanaPrincipal(root, db)

    # Ejecutar loop de eventos
    root.mainloop()


if __name__ == "__main__":
    main()


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS DE CARGA INICIAL
# ══════════════════════════════════════════════════════════════════════════════

# Esta sección carga datos de demostración si la base de datos está vacía.
# Descomenta si necesitas datos iniciales.

# def cargar_datos_demo():
#     """Carga datos de demostración en la base de datos."""
#     db = BaseDatos("biblioteca.db")
#
#     # Verificar si hay datos
#     if len(db.obtener_todos_libros()) == 0:
#         print("Cargando datos de demostración...")
#
#         # Libros
#         libros_demo = [
#             ("978-958-704-466-8", "Cien años de soledad",
#              "Gabriel García Márquez", 1967, "Realismo mágico"),
#             ("978-84-204-4804-4", "El Principito",
#              "Antoine de Saint-Exupéry", 1943, "Fábula"),
#             ("978-84-376-0494-7", "La casa de los espíritus",
#              "Isabel Allende", 1982, "Realismo mágico"),
#             ("978-0-7432-7356-5", "El código Da Vinci",
#              "Dan Brown", 2003, "Thriller"),
#             ("978-84-339-6833-2", "Ficciones",
#              "Jorge Luis Borges", 1944, "Cuento fantástico"),
#         ]
#
#         for isbn, titulo, autor, anio, genero in libros_demo:
#             db.agregar_libro(isbn, titulo, autor, anio, genero)
#
#         # Usuarios
#         usuarios_demo = [
#             ("Ana Torres", "ana.torres@email.com", "3001234567"),
#             ("Pedro Gómez", "pedro.gomez@email.com", "3109876543"),
#             ("Laura Martínez", "laura.m@email.com", "3205551234"),
#         ]
#
#         for nombre, email, telefono in usuarios_demo:
#             db.agregar_usuario(nombre, email, telefono)
#
#         # Crear un préstamo de demostración
#         db.crear_prestamo(1, 1)
#
#         print("Datos de demostración cargados exitosamente")
#     else:
#         print("Base de datos ya contiene datos")
#
# cargar_datos_demo()
