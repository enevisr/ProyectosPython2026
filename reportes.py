"""
Módulo: reportes.py
Descripción: Generación de reportes y gráficos con matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
from db import BaseDatos
from datetime import date


# Configurar estilo
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica']


def generar_reporte_general(db: BaseDatos) -> None:
    """
    Genera un reporte general con estadísticas principales.
    
    Crea una figura con múltiples subgráficos mostrando:
    - Libros disponibles vs prestados
    - Usuarios activos
    - Préstamos en regla vs vencidos
    """
    stats = db.obtener_estadisticas()

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("📊 Reporte General de Biblioteca", fontsize=16, fontweight="bold")

    # Gráfico 1: Libros disponibles vs prestados
    libros_data = [stats['libros_disponibles'], stats['libros_prestados']]
    colores1 = ['#2ecc71', '#e74c3c']
    ax1.pie(libros_data, labels=['Disponibles', 'Prestados'],
            autopct='%1.1f%%', colors=colores1, startangle=90)
    ax1.set_title("Estado de Libros")

    # Gráfico 2: Total de libros
    ax2.barh(['Total'], [stats['total_libros']], color='#3498db')
    ax2.set_title("Total de Libros en Catálogo")
    ax2.set_xlim(0, max(stats['total_libros'] * 1.2, 10))
    for i, v in enumerate([stats['total_libros']]):
        ax2.text(v + 0.5, i, str(v), va='center')

    # Gráfico 3: Usuarios
    ax3.barh(['Activos'], [stats['total_usuarios']], color='#9b59b6')
    ax3.set_title("Usuarios Activos")
    ax3.set_xlim(0, max(stats['total_usuarios'] * 1.2, 10))
    for i, v in enumerate([stats['total_usuarios']]):
        ax3.text(v + 0.5, i, str(v), va='center')

    # Gráfico 4: Préstamos vencidos
    prestamos_activos = stats['libros_prestados']
    prestamos_vencidos = stats['prestamos_vencidos']
    datos_vencidos = [prestamos_activos - prestamos_vencidos, prestamos_vencidos]
    colores4 = ['#27ae60', '#c0392b']
    ax4.pie(datos_vencidos,
            labels=['En Regla', 'Vencidos'],
            autopct='%1.1f%%',
            colors=colores4,
            startangle=90)
    ax4.set_title("Estado de Préstamos Activos")

    plt.tight_layout()
    plt.savefig("reporte_general.png", dpi=150, bbox_inches='tight')
    plt.close()


def generar_reporte_generos(db: BaseDatos) -> None:
    """
    Genera reporte de géneros más prestados.
    
    Muestra un gráfico de barras con los top 5 géneros
    ordenados por cantidad de préstamos.
    """
    stats = db.obtener_estadisticas()
    generos_data = stats['generos_top']

    if not generos_data:
        # Crear gráfico vacío
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Sin datos de préstamos por género',
               ha='center', va='center', fontsize=14)
        fig.suptitle("📚 Géneros Más Prestados", fontsize=16, fontweight="bold")
        plt.savefig("reporte_generos.png", dpi=150, bbox_inches='tight')
        plt.close()
        return

    generos = [g[0] for g in generos_data]
    cantidades = [g[1] for g in generos_data]

    fig, ax = plt.subplots(figsize=(10, 6))
    colores = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#9b59b6']
    barras = ax.barh(generos, cantidades, color=colores[:len(generos)])

    ax.set_xlabel('Cantidad de Préstamos')
    ax.set_title('Géneros Más Prestados', fontsize=14, fontweight='bold')
    ax.set_xlim(0, max(cantidades) * 1.2 if cantidades else 10)

    # Agregar valores en las barras
    for i, (barra, cantidad) in enumerate(zip(barras, cantidades)):
        ax.text(cantidad + 0.1, i, str(cantidad), va='center')

    fig.suptitle("📚 Géneros Más Prestados", fontsize=16, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig("reporte_generos.png", dpi=150, bbox_inches='tight')
    plt.close()


def generar_reporte_vencidos(db: BaseDatos, vencidos: list) -> None:
    """
    Genera reporte de préstamos vencidos.
    
    Muestra tabla con préstamos vencidos y sus días de retraso.
    """
    if not vencidos:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No hay préstamos vencidos',
               ha='center', va='center', fontsize=14)
        fig.suptitle("⚠️ Préstamos Vencidos", fontsize=16, fontweight="bold")
        plt.savefig("reporte_vencidos.png", dpi=150, bbox_inches='tight')
        plt.close()
        return

    datos_tabla = []
    for p in vencidos:
        libro = db.obtener_libro(p[1])
        usuario = db.obtener_usuario(p[2])
        titulo = libro[2] if libro else "Desconocido"
        nombre = usuario[1] if usuario else "Desconocido"
        dias_retraso = (date.today() - p[4]).days

        # Limitar longitud de texto
        titulo = titulo[:25]
        nombre = nombre[:25]

        datos_tabla.append([titulo, nombre, p[4], dias_retraso])

    # Crear tabla
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')

    tabla = ax.table(
        cellText=[[str(d[0]), str(d[1]), str(d[2]), str(d[3])]
                  for d in datos_tabla],
        colLabels=['Libro', 'Usuario', 'Fecha Límite', 'Días Retraso'],
        cellLoc='left',
        loc='center',
        bbox=[0, 0, 1, 1]
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 1.8)

    # Colorear header
    for i in range(4):
        tabla[(0, i)].set_facecolor('#e74c3c')
        tabla[(0, i)].set_text_props(weight='bold', color='white')

    # Colorear filas
    for i in range(1, len(datos_tabla) + 1):
        for j in range(4):
            if i % 2 == 0:
                tabla[(i, j)].set_facecolor('#ecf0f1')
            else:
                tabla[(i, j)].set_facecolor('#ffffff')

    fig.suptitle("⚠️ Préstamos Vencidos", fontsize=16, fontweight="bold")
    plt.savefig("reporte_vencidos.png", dpi=150, bbox_inches='tight')
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS
# ══════════════════════════════════════════════════════════════════════════════

# from db import BaseDatos
# db = BaseDatos("test_reportes.db")
# generar_reporte_general(db)
# print("Reporte general generado: reporte_general.png")
#
# generar_reporte_generos(db)
# print("Reporte de géneros generado: reporte_generos.png")
#
# vencidos = db.obtener_prestamos_vencidos()
# if vencidos:
#     generar_reporte_vencidos(db, vencidos)
#     print("Reporte de vencidos generado: reporte_vencidos.png")
