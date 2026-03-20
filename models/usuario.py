# models/usuario.py
from database import DatabaseConnection
from datetime import date
import mysql.connector

class Usuario:
    def __init__(self, id_usuario, nombre, email, telefono, fecha_nacimiento, clave, rol='usuario'):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.clave = clave
        self.rol = rol

class UsuarioRepository:
    def registrar(self, nombre, email, telefono, fecha_nacimiento, clave, rol='usuario'):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO Usuario 
                   (nombre, email, telefono, fecha_registro, fecha_nacimiento, clave, rol)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (nombre, email, telefono, date.today(), fecha_nacimiento, clave, rol)
            )
            conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False  # email duplicado
        finally:
            cursor.close()

    def iniciar_sesion(self, email, clave):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre, email, telefono, fecha_nacimiento, clave, rol "
            "FROM Usuario WHERE email = %s AND clave = %s",
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