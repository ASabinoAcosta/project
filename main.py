import datetime
from collections import Counter
from biblioteca.book import Book
from biblioteca.user import User
from biblioteca.prestamo import Prestamo
from biblioteca.library import LibrarySystem
from biblioteca.menu import Menu


if __name__ == "__main__":
    sistema = LibrarySystem("data/libros.json", "data/usuarios.json", "data/prestamos.json")
    menu = Menu(sistema)
    menu.run()