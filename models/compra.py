# models/compra.py
from database import DatabaseConnection
from datetime import datetime

class CompraRepository:
    def registrar_prestamo(self, id_usuario, id_libro):
        """Registra un préstamo (compra con total 0) y reduce stock."""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            # Insertar compra (préstamo)
            cursor.execute(
                "INSERT INTO Compra (id_usuario, fecha, total, estado) VALUES (%s, %s, 0, 'pagada')",
                (id_usuario, datetime.now())
            )
            id_compra = cursor.lastrowid
            # Obtener precio del libro (puede ser 0 para préstamo)
            cursor.execute("SELECT precio FROM Libro WHERE id_libro = %s", (id_libro,))
            precio = cursor.fetchone()[0]
            # Insertar detalle
            cursor.execute(
                "INSERT INTO DetalleCompra (id_compra, id_libro, cantidad, precio_unitario) VALUES (%s, %s, 1, %s)",
                (id_compra, id_libro, precio)
            )
            # Reducir stock
            cursor.execute("UPDATE Libro SET stock = stock - 1 WHERE id_libro = %s AND stock > 0", (id_libro,))
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            cursor.close()

    def obtener_historial(self, id_usuario):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.titulo, c.fecha
            FROM Compra c
            JOIN DetalleCompra d ON c.id_compra = d.id_compra
            JOIN Libro l ON d.id_libro = l.id_libro
            WHERE c.id_usuario = %s
            ORDER BY c.fecha DESC
        """, (id_usuario,))
        rows = cursor.fetchall()
        cursor.close()
        return [(row[0], row[1].strftime("%Y-%m-%d %H:%M")) for row in rows]