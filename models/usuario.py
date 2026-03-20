# models/usuario.py
from database import DatabaseConnection
from datetime import date
import mysql.connector

class Usuario:
    def __init__(self, id_usuario, nombre, email, telefono, fecha_nacimiento, clave, rol='usuario', verificado=False):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.clave = clave
        self.rol = rol
        self.verificado = verificado

class UsuarioRepository:
    def registrar_pendiente(self, nombre, email, telefono, fecha_nacimiento, clave, rol='usuario'):
        """Guarda un usuario pendiente de verificación (verificado=False)."""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO Usuario 
                   (nombre, email, telefono, fecha_registro, fecha_nacimiento, clave, rol, verificado)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)""",
                (nombre, email, telefono, date.today(), fecha_nacimiento, clave, rol)
            )
            conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False  # email duplicado
        finally:
            cursor.close()

    def confirmar_usuario(self, email):
        """Marca un usuario como verificado."""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Usuario SET verificado = TRUE WHERE email = %s", (email,))
        conn.commit()
        cursor.close()

    def usuario_existe(self, email):
        """Verifica si ya existe un usuario con ese email (sin importar verificado)."""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Usuario WHERE email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        return row is not None

    def iniciar_sesion(self, email, clave):
        """Solo permite acceso si el usuario está verificado."""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, email, telefono, fecha_nacimiento, clave, rol, verificado "
            "FROM Usuario WHERE email = %s AND clave = %s AND verificado = TRUE",
            (email, clave)
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Usuario(*row)
        return None

    def obtener_rol(self, email):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT rol FROM Usuario WHERE email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else None

    def obtener_todos_usuarios(self):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, email, telefono, rol FROM Usuario")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def obtener_cantidad_usuarios(self):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Usuario")
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def eliminar_usuario_pendiente(self, email):
        """Elimina un usuario que no ha sido verificado (por si falla la verificación)."""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuario WHERE email = %s AND verificado = FALSE", (email,))
        conn.commit()
        cursor.close()