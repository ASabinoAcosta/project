"""
OBJETIVO:

El sistema debe permitir administrar una biblioteca pequeña de forma sencilla y segura.

Debe evitar préstamos imposibles, libros duplicados y usuarios inexistentes.

El sistema utilizará tres archivos JSON.

    libros.json

    usuarios.json

    prestamos.json

=====================================
      SISTEMA DE BIBLIOTECA
=====================================

1. Gestión de libros

2. Gestión de usuarios

3. Gestión de préstamos

4. Consultas

5. Reportes

6. Guardar datos

7. Salir
"""
from biblioteca.json_manager import JsonManager
from biblioteca.menu import Menu

"""
2. Gestión de usuarios

Registrar estudiantes.

Cada usuario tendrá:
    ID
    Nombre
    Apellido
    Matrícula
    Carrera
    Correo
    Teléfono
    Estado

Validaciones

No permitir

Matrícula repetida
Correo repetido
Datos vacíos
"""

"""
3. Gestión de préstamos

Este será el corazón del sistema.

El bibliotecario podrá prestar libros únicamente si

✔ El usuario existe.

✔ El libro existe.

✔ Hay copias disponibles.

✔ El usuario tiene menos de tres préstamos activos.

Cuando un préstamo ocurra

Automáticamente

copias_disponibles --

sE GUARDARÁ:
ID préstamo
Usuario
Libro
Fecha préstamo
Fecha devolución esperada
Estado
"""


class LibrarySystem:
    
    def __init__(self, books_file, users_file, loans_file):
        self.books_manager = JsonManager(books_file)
        self.users_manager = JsonManager(users_file)
        self.loans_manager = JsonManager(loans_file)
    
    def register_book(self, book):
        """Registra un nuevo libro en el sistema."""
        self.books_manager.add_entry(book.__dict__)
    
    def register_user(self, user):
        """Registra un nuevo usuario en el sistema."""
        self.users_manager.add_entry(user.__dict__)
    
    def generate_book_id(self, category):

        abreviaturas = {
            "Novela": "NOV",
            "Programación": "PRO",
            "Historia": "HIS",
            "Ciencia": "CIE",
            "Matemáticas": "MAT"
        }
        libros = self.books_manager.load_data()

        contador = 0

        for libro in libros:

            if libro["category"] == category:
                contador += 1

        contador += 1

        numero = str(contador).zfill(3)

        abreviatura = abreviaturas.get(category, category[:3].upper())

        return f"LIB-{abreviatura}-{numero}"

    def exists_isbn(self, isbn):
        """Devuelve True si el ISBN ya está registrado."""
        books = self.books_manager.load_data()
        return any(book["isbn"] == isbn for book in books)

    def exists_user_data(self, student_id, email):
        """Devuelve 'matricula', 'correo' o None si los datos son únicos."""
        users = self.users_manager.load_data()
        for user in users:
            if user["student_id"] == student_id:
                return "matricula"
            if user["email"] == email:
                return "correo"
        return None
        
    def generate_user_id(self):
        """Genera un ID correlativo para el usuario."""
        users = self.users_manager.load_data()
        numero = len(users) + 1
        return f"USR-{str(numero).zfill(3)}"
