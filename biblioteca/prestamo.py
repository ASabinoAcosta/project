import json


class Prestamo:

    def __init__(self, id, user_id, book_id, loan_date, expected_return_date, status= "Activo"):
        self.id = id
        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.expected_return_date = expected_return_date
        self.status = status
    
    def finalizar_prestamo(self):
        self.status = "Finalizado"
    
    def registrar_devolucion(self, return_date):
        """
        Registra la devolución del libro, marcando el préstamo como finalizado y registrando la fecha de devolución.
        """
        self.finalizar_prestamo()
        self.return_date = return_date
        self.actualizar_copias_disponibles(self.book_id)
    
    def actualizar_copias_disponibles(self, book):
        """
        Incrementa las copias disponibles del libro asociado al préstamo.
        """
        book.available_copies += 1
    
    def validar_prestamo(self, user, book):
        """
        Valida si el préstamo puede realizarse según las reglas establecidas.
        """
        if user.status != "Activo":
            return False, "El usuario no está activo."
        if book.status != "Activo":
            return False, "El libro no está activo."
        if book.available_copies <= 0:
            return False, "No hay copias disponibles del libro."
        if self.contar_prestamos_activos(user) >= 3:
            return False, "El usuario ya tiene 3 préstamos activos."
        return True, "Préstamo válido."

    def contar_prestamos_activos(self, user):
        """
        Cuenta cuántos préstamos con estado 'Activo' tiene el usuario en la base de datos.
        """
        try:
            with open("prestamos.json", "r", encoding="utf-8") as file:
                prestamos = json.load(file)
                # Contamos cuántos préstamos pertenecen a este usuario y están activos
                activos = sum(1 for p in prestamos if p["user_id"] == user.id and p["status"] == "Activo")
                return activos
        except (FileNotFoundError, json.JSONDecodeError):
            return 0 # Si el archivo no existe o está vacío, tiene 0 préstamos

