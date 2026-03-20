# models/verificacion.py
from database import DatabaseConnection
from datetime import datetime, timedelta
import random

class VerificacionRepository:
    def crear_codigo(self, email):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        # Generar código de 6 dígitos
        codigo = ''.join(random.choices('0123456789', k=6))
        expiracion = datetime.now() + timedelta(minutes=10)
        try:
            cursor.execute(
                "INSERT INTO Verificacion (email, codigo, expiracion) VALUES (%s, %s, %s)",
                (email, codigo, expiracion)
            )
            conn.commit()
            return codigo
        except Exception as e:
            print(f"Error al crear código: {e}")
            return None
        finally:
            cursor.close()

    def verificar_codigo(self, email, codigo):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM Verificacion WHERE email = %s AND codigo = %s AND usado = FALSE AND expiracion > NOW()",
            (email, codigo)
        )
        row = cursor.fetchone()
        if row:
            # Marcar como usado
            cursor.execute("UPDATE Verificacion SET usado = TRUE WHERE id = %s", (row[0],))
            conn.commit()
            cursor.close()
            return True
        cursor.close()
        return False

    def limpiar_codigos_expirados(self):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Verificacion WHERE expiracion < NOW()")
        conn.commit()
        cursor.close()