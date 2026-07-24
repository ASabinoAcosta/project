class Report:

    def __init__(self, total_books, total_users, active_loans, loans_today, most_requested_book, category_with_most_loans):
        self.total_books = total_books
        self.total_users = total_users
        self.active_loans = active_loans
        self.loans_today = loans_today
        self.most_requested_book = most_requested_book
        self.category_with_most_loans = category_with_most_loans
    
    def generate_report(self):
        report = f"""
        ======== REPORTES ========
        Libros registrados: {self.total_books}
        Usuarios registrados: {self.total_users}
        Préstamos activos: {self.active_loans}
        Libros prestados hoy: {self.loans_today}
        Libro más solicitado: {self.most_requested_book}
        Categoría con más préstamos: {self.category_with_most_loans}
        """
        return report
