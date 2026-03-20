
# import customtkinter as ctk
# from constans import COLORES

# class PanelCategorias(ctk.CTkFrame):
#     def __init__(self, padre, colores, callback_categoria):
#         super().__init__(padre, fg_color=colores["dry_sage"], corner_radius=0)
#         self.colores = colores
#         self.callback = callback_categoria
#         self.botones = []
#         self.categorias = ["Todos", "Ficción", "No ficción", "Infantil", "Revistas", "Tesis"]
#         self.crear_botones()

#     def crear_botones(self):
#         ctk.CTkLabel(
#             self, text="Categorías",
#             font=("Segoe UI", 12, "bold"),
#             text_color=self.colores["jet_black"]
#         ).pack(pady=10)

#         for cat in self.categorias:
#             btn = ctk.CTkButton(
#                 self, text=cat,
#                 fg_color=self.colores["soft_peach"],
#                 text_color=self.colores["jet_black"],
#                 hover_color=self.colores["tangerine"],
#                 command=lambda c=cat: self.seleccionar(c)
#             )
#             btn.pack(fill="x", padx=10, pady=3)
#             self.botones.append(btn)

#     def seleccionar(self, categoria):
#         for btn in self.botones:
#             if btn.cget("text") == categoria:
#                 btn.configure(fg_color=self.colores["tangerine"])
#             else:
#                 btn.configure(fg_color=self.colores["soft_peach"])
#         self.callback(categoria)


# class PanelLibros(ctk.CTkFrame):
#     def __init__(self, padre, colores, libros_ejemplo):
#         super().__init__(padre, fg_color=colores["soft_peach"], corner_radius=0)
#         self.colores = colores
#         self.todos_libros = libros_ejemplo
#         self.libros_filtrados = self.todos_libros[:]
#         self.crear_widgets()

#     def crear_widgets(self):
#         self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
#         self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

#         # Encabezados
#         self.encabezados = ["Título", "Autor", "Año", "Estado"]
#         for i, texto in enumerate(self.encabezados):
#             lbl = ctk.CTkLabel(
#                 self.scroll_frame, text=texto,
#                 font=("Segoe UI", 12, "bold"),
#                 text_color=self.colores["jet_black"]
#             )
#             lbl.grid(row=0, column=i, padx=5, pady=5, sticky="w")
#             self.scroll_frame.grid_columnconfigure(i, weight=1 if i < 2 else 0)

#         separator = ctk.CTkFrame(self.scroll_frame, height=2, fg_color=self.colores["jet_black"])
#         separator.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)

#         self.filas = []
#         self.actualizar_tabla()

#     def actualizar_tabla(self):
#         # Eliminar filas anteriores
#         for fila in self.filas:
#             for widget in fila:
#                 widget.destroy()
#         self.filas.clear()

#         # Insertar nuevos libros
#         for idx, libro in enumerate(self.libros_filtrados):
#             fila_widgets = []
#             for col, valor in enumerate(libro[:4]):
#                 lbl = ctk.CTkLabel(
#                     self.scroll_frame, text=str(valor),
#                     text_color=self.colores["jet_black"]
#                 )
#                 lbl.grid(row=idx+2, column=col, padx=5, pady=2, sticky="w")
#                 fila_widgets.append(lbl)
#             self.filas.append(fila_widgets)

#     def filtrar(self, texto, categoria):
#         texto = texto.lower()
#         filtrados = []
#         for libro in self.todos_libros:
#             if categoria != "Todos" and libro[4] != categoria:
#                 continue
#             if texto in libro[0].lower() or texto in libro[1].lower():
#                 filtrados.append(libro)
#         self.libros_filtrados = filtrados
#         self.actualizar_tabla()