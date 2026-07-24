import datetime


class Book:

    def __init__(self, id, title, author, publication_year, category, isbn, total_copies, available_copies, status="Activo"):

        if not title.strip():
            raise ValueError("El título no puede estar vacío.")

        if not author.strip():
            raise ValueError("El autor no puede estar vacío.")

        if total_copies < 0:
            raise ValueError("La cantidad de copias no puede ser negativa.")

        año_actual = datetime.date.today().year
        if publication_year > año_actual:
            raise ValueError(f"El año de publicación no puede ser mayor a {año_actual}.")
        if not category.strip():
            raise ValueError("La categoría no puede estar vacía.")

        if not isbn.strip():
            raise ValueError("El ISBN no puede estar vacío.")
        
        self.id = id
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.category = category
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = available_copies
        self.status = status
    
    def cambiar_estado(self, nuevo_estado):
        self.status = nuevo_estado
    
    def actualizar_copias(self, nuevas_copias):
        prestados = self.total_copies - self.available_copies

        if nuevas_copias < prestados:
            raise ValueError(
                f"No puedes reducir las copias a {nuevas_copias}. "
                f"Actualmente hay {prestados} libros prestados."
            )

        self.total_copies = nuevas_copias
        self.available_copies = nuevas_copias - prestados