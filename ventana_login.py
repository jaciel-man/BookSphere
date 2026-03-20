# # ventana_login.py
# import customtkinter as ctk
# from CTkMessagebox import CTkMessagebox
# from auth import Autenticador
# from constans import COLORES

# class VentanaLogin(ctk.CTkToplevel):
#     def __init__(self, padre, autenticador, callback_exito):
#         super().__init__(padre)
#         self.autenticador = autenticador
#         self.callback_exito = callback_exito
#         self.title("Iniciar sesión / Registro")
#         self.geometry("450x500")
#         self.resizable(False, False)
#         self.transient(padre)
#         self.grab_set()
#         self.colores = COLORES

#         self.crear_widgets()

#     def crear_widgets(self):
#         # Título
#         ctk.CTkLabel(
#             self, text="Biblioteca Digital",
#             font=("Segoe UI", 16, "bold"),
#             text_color=self.colores["jet_black"]
#         ).pack(pady=10)

#         # Tabview
#         self.tabview = ctk.CTkTabview(self, fg_color=self.colores["soft_peach"])
#         self.tabview.pack(pady=10, padx=20, fill="both", expand=True)

#         self.tab_login = self.tabview.add("Iniciar sesión")
#         self.tab_registro = self.tabview.add("Registrarse")

#         self.crear_login()
#         self.crear_registro()

#     def crear_login(self):
#         frame = self.tab_login
#         self.login_entries = {}

#         # Usuario
#         ctk.CTkLabel(frame, text="Usuario:", text_color=self.colores["jet_black"]).grid(row=0, column=0, padx=10, pady=8, sticky="e")
#         entry_usuario = ctk.CTkEntry(frame)
#         entry_usuario.grid(row=0, column=1, padx=10, pady=8)
#         self.login_entries["Usuario:"] = entry_usuario

#         # Contraseña
#         ctk.CTkLabel(frame, text="Contraseña:", text_color=self.colores["jet_black"]).grid(row=1, column=0, padx=10, pady=8, sticky="e")
#         entry_pass = ctk.CTkEntry(frame, show="*")
#         entry_pass.grid(row=1, column=1, padx=10, pady=8)
#         self.login_entries["Contraseña:"] = entry_pass

#         # Botón entrar
#         btn = ctk.CTkButton(
#             frame, text="Entrar",
#             fg_color=self.colores["tangerine"],
#             text_color=self.colores["jet_black"],
#             command=self.procesar_login
#         )
#         btn.grid(row=2, columnspan=2, pady=15)

#         # Mensaje
#         self.lbl_mensaje_login = ctk.CTkLabel(frame, text="", text_color=self.colores["tangerine"])
#         self.lbl_mensaje_login.grid(row=3, columnspan=2)

#     def crear_registro(self):
#         frame = self.tab_registro
#         self.reg_entries = {}

#         campos = [
#             ("Nombre completo:", 0),
#             ("Correo electrónico:", 1),
#             ("Teléfono:", 2),
#             ("Usuario:", 3),
#             ("Contraseña:", 4),
#             ("Confirmar contraseña:", 5)
#         ]

#         for texto, fila in campos:
#             ctk.CTkLabel(frame, text=texto, text_color=self.colores["jet_black"]).grid(row=fila, column=0, padx=10, pady=5, sticky="e")
#             show = "*" if "Contraseña" in texto else ""
#             entry = ctk.CTkEntry(frame, show=show)
#             entry.grid(row=fila, column=1, padx=10, pady=5)
#             self.reg_entries[texto] = entry

#         # Fecha de nacimiento
#         ctk.CTkLabel(frame, text="Fecha de nacimiento:", text_color=self.colores["jet_black"]).grid(row=6, column=0, padx=10, pady=5, sticky="e")
#         self.fecha_entry = ctk.CTkEntry(frame)
#         self.fecha_entry.grid(row=6, column=1, padx=10, pady=5)

#         # Botón registrarse
#         btn = ctk.CTkButton(
#             frame, text="Registrarse",
#             fg_color=self.colores["tangerine"],
#             text_color=self.colores["jet_black"],
#             command=self.procesar_registro
#         )
#         btn.grid(row=7, columnspan=2, pady=15)

#         # Mensaje
#         self.lbl_mensaje_reg = ctk.CTkLabel(frame, text="", text_color=self.colores["tangerine"])
#         self.lbl_mensaje_reg.grid(row=8, columnspan=2)

#     def procesar_login(self):
#         usuario = self.login_entries["Usuario:"].get()
#         password = self.login_entries["Contraseña:"].get()
#         if self.autenticador.iniciar_sesion(usuario, password):
#             self.callback_exito(usuario)
#             self.destroy()
#         else:
#             self.lbl_mensaje_login.configure(text="Usuario o contraseña incorrectos")

#     def procesar_registro(self):
#         datos = {k: v.get() for k, v in self.reg_entries.items()}
#         fecha = self.fecha_entry.get()
#         if any(not v for v in datos.values()) or not fecha:
#             self.lbl_mensaje_reg.configure(text="Todos los campos son obligatorios")
#             return
#         if datos["Contraseña:"] != datos["Confirmar contraseña:"]:
#             self.lbl_mensaje_reg.configure(text="Las contraseñas no coinciden")
#             return
#         exito = self.autenticador.registrar(
#             datos["Nombre completo:"],
#             datos["Correo electrónico:"],
#             datos["Teléfono:"],
#             datos["Usuario:"],
#             datos["Contraseña:"]
#         )
#         if exito:
#             CTkMessagebox(self, title="Registro", message="Usuario registrado con éxito. Se ha iniciado sesión automáticamente.", icon="info")
#             self.callback_exito(datos["Usuario:"])
#             self.destroy()
#         else:
#             self.lbl_mensaje_reg.configure(text="El nombre de usuario ya existe")

#     def limpiar_registro(self):
#         for entry in self.reg_entries.values():
#             entry.delete(0, "end")
#         self.fecha_entry.delete(0, "end")
#         self.lbl_mensaje_reg.configure(text="")