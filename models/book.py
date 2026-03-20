# models/book.py

class Book:
    def __init__(self, title, author, year, status, category):
        self.title = title
        self.author = author
        self.year = year
        self.status = status
        self.category = category

class BookRepository:
    def __init__(self):
        self._books = [
            Book("Cien años de soledad", "Gabriel García Márquez", 1967, "Disponible", "Ficción"),
            Book("1984", "George Orwell", 1949, "Prestado", "Ficción"),
            Book("El Quijote", "Miguel de Cervantes", 1605, "Disponible", "Ficción"),
            Book("Breve historia del tiempo", "Stephen Hawking", 1988, "Disponible", "No ficción"),
            Book("Cosmos", "Carl Sagan", 1980, "Disponible", "No ficción"),
            Book("El principito", "Antoine de Saint-Exupéry", 1943, "Disponible", "Infantil"),
        ]

    def get_all(self):
        return self._books

    def filter(self, search_text, category):
        search_text = search_text.lower()
        return [b for b in self._books
                if (category == "Todos" or b.category == category) and
                   (search_text in b.title.lower() or search_text in b.author.lower())]

    def agregar(self, book):
        self._books.append(book)

    def eliminar(self, index):
        del self._books[index]

    def actualizar(self, index, book):
        self._books[index] = book

class CategoryRepository:
    def __init__(self):
        self._categories = ["Todos", "Ficción", "No ficción", "Infantil", "Revistas", "Tesis"]

    def obtener_nombres(self):
        return self._categories

    def agregar(self, category):
        if category not in self._categories:
            self._categories.append(category)

    def eliminar(self, category):
        if category in self._categories and category not in ["Todos", "Ficción", "No ficción", "Infantil", "Revistas", "Tesis"]:
            self._categories.remove(category)