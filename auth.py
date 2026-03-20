class Autenticador:
    def __init__(self):
        self.usuarios = {}

    def registrar(self, nombre, correo, telefono, usuario, password):
        if usuario in self.usuarios:
            return False
        self.usuarios[usuario] = {
            "nombre": nombre,
            "correo": correo,
            "telefono": telefono,
            "password": password
        }
        return True

    def iniciar_sesion(self, usuario, password):
        return usuario in self.usuarios and self.usuarios[usuario]["password"] == password