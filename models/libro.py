# models/libro.py
from database import DatabaseConnection
import mysql.connector

class Libro:
    def __init__(self, id_libro, titulo, autor, precio, stock, publicacion, categoria_nombre):
        self.id = id_libro
        self.titulo = titulo
        self.autor = autor
        self.precio = precio
        self.stock = stock
        self.publicacion = publicacion
        self.categoria_nombre = categoria_nombre
        # Atributos para compatibilidad con la GUI
        self.year = publicacion
        self.status = "Disponible" if stock > 0 else "Prestado"
        self.category = categoria_nombre

class LibroRepository:
    def get_all(self):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.id_libro, l.titulo, l.autor, l.precio, l.stock, l.publicacion, c.nombre
            FROM Libro l
            LEFT JOIN Categoria c ON l.id_categoria = c.id_categoria
        """)
        rows = cursor.fetchall()
        cursor.close()
        return [Libro(*row) for row in rows]

    def filter(self, search_text, categoria_nombre):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT l.id_libro, l.titulo, l.autor, l.precio, l.stock, l.publicacion, c.nombre
            FROM Libro l
            LEFT JOIN Categoria c ON l.id_categoria = c.id_categoria
            WHERE (c.nombre = %s OR %s = 'Todos')
              AND (l.titulo LIKE %s OR l.autor LIKE %s)
        """
        like = f"%{search_text}%"
        cursor.execute(query, (categoria_nombre, categoria_nombre, like, like))
        rows = cursor.fetchall()
        cursor.close()
        return [Libro(*row) for row in rows]

    def agregar(self, libro):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        # Obtener id_categoria
        cursor.execute("SELECT id_categoria FROM Categoria WHERE nombre = %s", (libro.category,))
        row = cursor.fetchone()
        id_categoria = row[0] if row else None
        cursor.execute(
            """INSERT INTO Libro (titulo, autor, precio, stock, publicacion, id_categoria)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (libro.titulo, libro.autor, libro.precio, libro.stock, libro.publicacion, id_categoria)
        )
        conn.commit()
        cursor.close()

    def actualizar(self, libro):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria FROM Categoria WHERE nombre = %s", (libro.category,))
        row = cursor.fetchone()
        id_categoria = row[0] if row else None
        cursor.execute(
            """UPDATE Libro SET titulo=%s, autor=%s, precio=%s, stock=%s, publicacion=%s, id_categoria=%s
               WHERE id_libro=%s""",
            (libro.titulo, libro.autor, libro.precio, libro.stock, libro.publicacion, id_categoria, libro.id)
        )
        conn.commit()
        cursor.close()

    def eliminar(self, id_libro):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Libro WHERE id_libro = %s", (id_libro,))
        conn.commit()
        cursor.close()

class CategoriaRepository:
    def obtener_nombres(self):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM Categoria")
        rows = cursor.fetchall()
        cursor.close()
        return [row[0] for row in rows]

    def agregar(self, nombre):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Categoria (nombre) VALUES (%s)", (nombre,))
            conn.commit()
        except mysql.connector.IntegrityError:
            pass  # ya existe
        finally:
            cursor.close()

    def eliminar(self, nombre):
        # No permitir eliminar categorías predeterminadas
        if nombre in ["Todos", "Ficción", "No ficción", "Infantil", "Revistas", "Tesis"]:
            return
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Categoria WHERE nombre = %s", (nombre,))
        conn.commit()
        cursor.close()