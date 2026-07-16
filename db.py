"""
Módulo: db.py
Descripción: Gestión de la base de datos SQLite para la aplicación de biblioteca.
"""

import sqlite3
from datetime import date, timedelta
from typing import List, Tuple, Optional


class BaseDatos:
    """
    Clase que gestiona todas las operaciones con la base de datos SQLite.
    
    Responsabilidades:
        - Crear tablas si no existen
        - Operaciones CRUD (Create, Read, Update, Delete)
        - Consultas especializadas para préstamos y reportes
    """

    def __init__(self, ruta_db: str = "biblioteca.db"):
        self.ruta_db = ruta_db
        self.crear_tablas()

    def conectar(self):
        """Abre una conexión a la base de datos."""
        return sqlite3.connect(self.ruta_db)

    def crear_tablas(self) -> None:
        """Crea las tablas si no existen."""
        conexion = self.conectar()
        cursor = conexion.cursor()

        # Tabla: libros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS libros (
                id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE NOT NULL,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                anio_publicacion INTEGER,
                genero TEXT,
                disponible BOOLEAN DEFAULT 1
            )
        """)

        # Tabla: usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono TEXT,
                activo BOOLEAN DEFAULT 1
            )
        """)

        # Tabla: prestamos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
                id_libro INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                fecha_prestamo DATE NOT NULL,
                fecha_devolucion_esperada DATE NOT NULL,
                fecha_devolucion_real DATE,
                activo BOOLEAN DEFAULT 1,
                FOREIGN KEY (id_libro) REFERENCES libros (id_libro),
                FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
            )
        """)

        conexion.commit()
        conexion.close()

    # ══ OPERACIONES LIBRO ══════════════════════════════════════════════════
    def agregar_libro(self, isbn: str, titulo: str, autor: str,
                      anio: int, genero: str) -> bool:
        """Agrega un nuevo libro a la base de datos."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO libros (isbn, titulo, autor, anio_publicacion, "
                "genero) VALUES (?, ?, ?, ?, ?)",
                (isbn, titulo, autor, anio, genero)
            )
            conexion.commit()
            conexion.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def obtener_libro(self, id_libro: int) -> Optional[Tuple]:
        """Obtiene un libro por ID."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM libros WHERE id_libro = ?", (id_libro,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado

    def obtener_todos_libros(self) -> List[Tuple]:
        """Retorna todos los libros."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM libros ORDER BY titulo")
        libros = cursor.fetchall()
        conexion.close()
        return libros

    def obtener_libros_disponibles(self) -> List[Tuple]:
        """Retorna solo los libros disponibles."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM libros WHERE disponible = 1 ORDER BY titulo")
        libros = cursor.fetchall()
        conexion.close()
        return libros

    def buscar_libro_por_isbn(self, isbn: str) -> Optional[Tuple]:
        """Busca un libro por ISBN."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM libros WHERE isbn = ?", (isbn,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado

    def actualizar_libro(self, id_libro: int, titulo: str, autor: str,
                        anio: int, genero: str) -> bool:
        """Actualiza datos de un libro."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE libros SET titulo = ?, autor = ?, "
                "anio_publicacion = ?, genero = ? WHERE id_libro = ?",
                (titulo, autor, anio, genero, id_libro)
            )
            conexion.commit()
            conexion.close()
            return True
        except Exception:
            return False

    def eliminar_libro(self, id_libro: int) -> bool:
        """Elimina un libro."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM libros WHERE id_libro = ?",
                          (id_libro,))
            conexion.commit()
            conexion.close()
            return True
        except Exception:
            return False

    def marcar_disponibilidad_libro(self, id_libro: int,
                                    disponible: bool) -> bool:
        """Cambia el estado disponibilidad de un libro."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE libros SET disponible = ? WHERE id_libro = ?",
                (disponible, id_libro)
            )
            conexion.commit()
            conexion.close()
            return True
        except Exception:
            return False

    # ══ OPERACIONES USUARIO ════════════════════════════════════════════════
    def agregar_usuario(self, nombre: str, email: str, telefono: str) -> bool:
        """Agrega un nuevo usuario."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, telefono) "
                "VALUES (?, ?, ?)",
                (nombre, email, telefono)
            )
            conexion.commit()
            conexion.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def obtener_usuario(self, id_usuario: int) -> Optional[Tuple]:
        """Obtiene un usuario por ID."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?",
                      (id_usuario,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado

    def obtener_todos_usuarios(self) -> List[Tuple]:
        """Retorna todos los usuarios."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY nombre")
        usuarios = cursor.fetchall()
        conexion.close()
        return usuarios

    def obtener_usuarios_activos(self) -> List[Tuple]:
        """Retorna solo usuarios activos."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE activo = 1 ORDER BY nombre")
        usuarios = cursor.fetchall()
        conexion.close()
        return usuarios

    def actualizar_usuario(self, id_usuario: int, nombre: str,
                          email: str, telefono: str) -> bool:
        """Actualiza datos de un usuario."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE usuarios SET nombre = ?, email = ?, telefono = ? "
                "WHERE id_usuario = ?",
                (nombre, email, telefono, id_usuario)
            )
            conexion.commit()
            conexion.close()
            return True
        except Exception:
            return False

    def eliminar_usuario(self, id_usuario: int) -> bool:
        """Desactiva un usuario (soft delete)."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE usuarios SET activo = 0 WHERE id_usuario = ?",
                (id_usuario,)
            )
            conexion.commit()
            conexion.close()
            return True
        except Exception:
            return False

    # ══ OPERACIONES PRESTAMO ═══════════════════════════════════════════════
    def crear_prestamo(self, id_libro: int, id_usuario: int) -> bool:
        """Crea un nuevo préstamo."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            fecha_prestamo = date.today()
            fecha_devolucion = fecha_prestamo + timedelta(days=15)

            cursor.execute(
                "INSERT INTO prestamos "
                "(id_libro, id_usuario, fecha_prestamo, "
                "fecha_devolucion_esperada) VALUES (?, ?, ?, ?)",
                (id_libro, id_usuario, fecha_prestamo, fecha_devolucion)
            )
            conexion.commit()

            # Marcar libro como no disponible
            self.marcar_disponibilidad_libro(id_libro, False)

            conexion.close()
            return True
        except Exception:
            return False

    def obtener_prestamo(self, id_prestamo: int) -> Optional[Tuple]:
        """Obtiene un préstamo por ID."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM prestamos WHERE id_prestamo = ?",
                      (id_prestamo,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado

    def obtener_todos_prestamos(self) -> List[Tuple]:
        """Retorna todos los préstamos."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM prestamos ORDER BY fecha_prestamo DESC")
        prestamos = cursor.fetchall()
        conexion.close()
        return prestamos

    def obtener_prestamos_activos(self) -> List[Tuple]:
        """Retorna solo los préstamos activos."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM prestamos WHERE activo = 1 "
            "ORDER BY fecha_prestamo DESC")
        prestamos = cursor.fetchall()
        conexion.close()
        return prestamos

    def obtener_prestamos_vencidos(self) -> List[Tuple]:
        """Retorna préstamos vencidos (fecha actual > fecha límite)."""
        conexion = self.conectar()
        cursor = conexion.cursor()
        hoy = date.today()
        cursor.execute(
            "SELECT * FROM prestamos WHERE activo = 1 "
            "AND fecha_devolucion_esperada < ? "
            "ORDER BY fecha_devolucion_esperada",
            (hoy,)
        )
        prestamos = cursor.fetchall()
        conexion.close()
        return prestamos

    def devolver_libro(self, id_prestamo: int) -> bool:
        """Registra la devolución de un préstamo."""
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            fecha_devolucion = date.today()

            # Obtener id_libro del préstamo
            cursor.execute("SELECT id_libro FROM prestamos WHERE id_prestamo = ?",
                          (id_prestamo,))
            resultado = cursor.fetchone()
            if not resultado:
                conexion.close()
                return False

            id_libro = resultado[0]

            # Actualizar préstamo
            cursor.execute(
                "UPDATE prestamos SET activo = 0, fecha_devolucion_real = ? "
                "WHERE id_prestamo = ?",
                (fecha_devolucion, id_prestamo)
            )

            # Marcar libro como disponible
            self.marcar_disponibilidad_libro(id_libro, True)

            conexion.commit()
            conexion.close()
            return True
        except Exception:
            return False

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas generales de la biblioteca."""
        conexion = self.conectar()
        cursor = conexion.cursor()

        # Total de libros
        cursor.execute("SELECT COUNT(*) FROM libros")
        total_libros = cursor.fetchone()[0]

        # Libros disponibles
        cursor.execute("SELECT COUNT(*) FROM libros WHERE disponible = 1")
        libros_disponibles = cursor.fetchone()[0]

        # Libros prestados
        cursor.execute(
            "SELECT COUNT(*) FROM prestamos WHERE activo = 1")
        prestamos_activos = cursor.fetchone()[0]

        # Total usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = 1")
        total_usuarios = cursor.fetchone()[0]

        # Préstamos vencidos
        hoy = date.today()
        cursor.execute(
            "SELECT COUNT(*) FROM prestamos WHERE activo = 1 "
            "AND fecha_devolucion_esperada < ?",
            (hoy,)
        )
        prestamos_vencidos = cursor.fetchone()[0]

        # Top 5 géneros más prestados
        cursor.execute("""
            SELECT l.genero, COUNT(p.id_prestamo) as cantidad
            FROM libros l
            JOIN prestamos p ON l.id_libro = p.id_libro
            GROUP BY l.genero
            ORDER BY cantidad DESC
            LIMIT 5
        """)
        generos = cursor.fetchall()

        conexion.close()

        return {
            "total_libros": total_libros,
            "libros_disponibles": libros_disponibles,
            "libros_prestados": prestamos_activos,
            "total_usuarios": total_usuarios,
            "prestamos_vencidos": prestamos_vencidos,
            "generos_top": generos
        }


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS
# ══════════════════════════════════════════════════════════════════════════════

# db = BaseDatos("test.db")
# db.crear_tablas()

# # Agregar libros
# db.agregar_libro("978-1", "El Principito", "Saint-Exupéry", 1943, "Fábula")
# db.agregar_libro("978-2", "Cien años de soledad", "García Márquez", 1967,
#                  "Realismo mágico")

# # Agregar usuarios
# db.agregar_usuario("Ana Torres", "ana@mail.com", "3001234567")
# db.agregar_usuario("Pedro Gómez", "pedro@mail.com", "3109876543")

# # Listar
# print("Libros:", db.obtener_todos_libros())
# print("Usuarios:", db.obtener_todos_usuarios())

# # Préstamo
# db.crear_prestamo(1, 1)
# print("Préstamos:", db.obtener_prestamos_activos())
# print("Libro disponible?:", db.obtener_libro(1)[6])  # disponible = True/False

# # Devolución
# db.devolver_libro(1)
# print("Libro disponible después devolución?:", db.obtener_libro(1)[6])

# # Estadísticas
# print("Estadísticas:", db.obtener_estadisticas())
