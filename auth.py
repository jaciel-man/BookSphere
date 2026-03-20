class Autenticador:
    def __init__(self):
        self.usuarios = {}
        # Crear administrador por defecto
        self.usuarios["admin"] = {
            "nombre": "Administrador",
            "correo": "admin@biblioteca.com",
            "telefono": "0000000000",
            "password": "admin",
            "rol": "admin"
        }

    def registrar(self, nombre, correo, telefono, usuario, password, rol="usuario"):
        if usuario in self.usuarios:
            return False
        self.usuarios[usuario] = {
            "nombre": nombre,
            "correo": correo,
            "telefono": telefono,
            "password": password,
            "rol": rol
        }
        return True

    def iniciar_sesion(self, usuario, password):
        return usuario in self.usuarios and self.usuarios[usuario]["password"] == password

    def obtener_rol(self, usuario):
        return self.usuarios.get(usuario, {}).get("rol", "usuario")