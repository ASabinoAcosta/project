import datetime
from collections import Counter
from biblioteca.book import Book
from biblioteca.user import User
from biblioteca.prestamo import Prestamo
from biblioteca.library import LibrarySystem

class Menu:

    def __init__(self, library_system):
        self.library_system = library_system
    
    def run(self):
        while True:
            if not self.display_menu():
                break
    
    def mostrar_libro(self,book):
            print(f"""
        ========================================
        📚 LIBRO
        ========================================
        ID:                 {book['id']}
        Título:             {book['title']}
        Autor:              {book['author']}
        Categoría:          {book['category']}
        ISBN:               {book['isbn']}
        Copias totales:     {book['total_copies']}
        Disponibles:        {book['available_copies']}
        Estado:             {book['status']}
        ========================================
        """)
    
    def mostrar_prestamo(self, loan):
            print(f"""
        ========================================
        📖 PRÉSTAMO
        ========================================
        ID:                 {loan['id']}
        Usuario:            {loan['user_id']}
        Libro:              {loan['book_id']}
        Fecha préstamo:     {loan['loan_date']}
        Fecha devolución:   {loan['expected_return_date']}
        Estado:             {loan['status']}
        ========================================
        """)

    def mostrar_usuario(self,user):
            print(f"""
        ========================================
        👤 USUARIO
        ========================================
        ID:                 {user['id']}
        Nombre:             {user['first_name']} {user['last_name']}
        Matrícula:          {user['student_id']}
        Carrera:            {user['major']}
        Correo:             {user['email']}
        Teléfono:           {user['phone']}
        Estado:             {user['status']}
        ========================================
        """)    

    def manage_books(self):
        """
        Mostrar submenú de libros
        Pedir opción
        Llamar a LibrarySystem
        """


        user_input = input("""
        ======== GESTIÓN DE LIBROS =========
        1. Registrar nuevo libro
        2. Consultar catálogo
        3. Buscar libro                  
        4. Editar información
        5. Eliminar libro
        6. Volver al menú principal
        """)

        if user_input == "1":
            self.register_book()
        elif user_input == "2":
            self.show_books()
        elif user_input == "3": 
            self.search_book()
        elif user_input == "4":
            self.edit_book()


        elif user_input == "5":
            self.delete_book()
        elif user_input == "6":
            return

    def register_book(self):
       
#Lógica para registrar un nuevo libro
            print("\n===== AGREGAR LIBRO =====")

            title = input("Título: ")
            author = input("Autor: ")
            try:
                year = int(input("Año: "))
            except ValueError:
                print("Debe ingresar un número.")
                return
            isbn = input("ISBN: ")
            try:
                copies = int(input("Cantidad de copias: "))
            except ValueError:
                print("Debe ingresar un número.")
                return

            categorias = {
                "1": "novela",
                "2": "programación",
                "3": "historia",
                "4": "ciencia",
                "5": "matemáticas"
            }

            print("""
            Categorías
            1. Novela
            2. Programación
            3. Historia
            4. Ciencia
            5. Matemáticas
            """)

            opcion = input("Seleccione una categoría: ").lower()

            if opcion not in categorias:
                print("Categoría inválida.")
                return

            category = categorias[opcion]


            book_id = self.library_system.generate_book_id(category)
            if self.library_system.exists_isbn(isbn):
                print("Ese ISBN ya existe.")
                return


            try:
                book = Book(
                    book_id,
                    title,
                    author,
                    year,
                    category,
                    isbn,
                    copies,
                    copies,
                    "Activo"
                )

                self.library_system.register_book(book)
                print("Libro agregado correctamente.")

            except ValueError as e:
                print(f"Error: {e}")
    def show_books(self):
        # Lógica para consultar el catálogo

        books = self.library_system.books_manager.load_data()

        print("\n===== CATÁLOGO DE LIBROS =====")

        for book in books:
            if book["status"] == "Activo":
                print(f"""
                ID: {book["id"]}
                Título: {book["title"]}
                Autor: {book["author"]}
                Categoría: {book["category"]}
                Copias disponibles: {book["available_copies"]}
                ----------------------------
                """)
    def search_book(self):
# Lógica para buscar un libro

        search = input("Ingrese título, autor o ISBN: ").lower()

        books = self.library_system.books_manager.load_data()

        found = False

        for book in books:

            if book["status"] == "Activo":

                if (
                    search in book["title"].lower()
                    or search in book["author"].lower()
                    or search in book["isbn"]
                ):

                    self.mostrar_libro(book)

                    found = True

        if not found:
            print("No se encontró ningún libro.")
    def edit_book(self):
        # Lógica para editar información de un libro

        book_id = input("Ingrese ID del libro a editar: ")

        books = self.library_system.books_manager.load_data()

        for book in books:

            if book["id"] == book_id:

                print("Deje vacío si no desea cambiar el dato.")

                title = input("Nuevo título: ")
                author = input("Nuevo autor: ")
                category = input("Nueva categoría: ")

                if title:
                    book["title"] = title

                if author:
                    book["author"] = author

                if category:
                    book["category"] = category


                self.library_system.books_manager.save_data(books)

                print("Libro actualizado correctamente.")
                break

            else:
                print("Libro no encontrado.")
    def delete_book(self):
        # Lógica para eliminar un libro

        book_id = input("Ingrese ID del libro a eliminar: ")

        books = self.library_system.books_manager.load_data()
        loans = self.library_system.loans_manager.load_data()

        found = False

        for book in books:

            if book["id"] == book_id:

                prestado = any(
                    loan["book_id"] == book_id and loan["status"] == "Activo"
                    for loan in loans
                )

                if prestado:
                    print("No se puede eliminar un libro con préstamos activos.")
                    break

                book["status"] = "Inactivo"
                found = True
                break

        if found:
            self.library_system.books_manager.save_data(books)
            print("Libro eliminado correctamente.")
        else:
            print("Libro no encontrado.")

    def manage_users(self):
        # Mostrar submenú de usuarios
        # Pedir opción
        # Llamar a LibrarySystem
        while True:

            user_input = input("""
            ===== GESTIÓN DE USUARIOS =====

            1. Registrar usuario
            2. Consultar usuarios
            3. Buscar usuario
            4. Editar usuario
            5. Eliminar usuario
            6. Volver

            Seleccione: 
            """)

            if user_input == "1":

                # Aquí va tu lógica de agregar usuario
                print("\n===== AGREGAR USUARIO =====")
                first_name = input("Nombre: ")
                last_name = input("Apellido: ")
                student_id = input("Matrícula: ")
                major = input("Carrera: ")
                email = input("Correo: ")
                phone = input("Teléfono: ")

                # Validación global
                conflicto = self.library_system.exists_user_data(student_id, email)
                if conflicto:
                    print(f"Error: Ya existe un usuario con ese/a {conflicto}.")
                    continue

                user_id = self.library_system.generate_user_id()
                try:
                    nuevo_usuario = User(user_id, first_name, last_name, student_id, major, email, phone)
                    self.library_system.register_user(nuevo_usuario)
                    print(f"Usuario {first_name} registrado con éxito (ID: {user_id}).")
                except ValueError as e:
                    print(f"Error al registrar: {e}")

            elif user_input == "2":

                users = self.library_system.users_manager.load_data()

                for user in users:
                    if user["status"] == "Activo":
                        self.mostrar_usuario(user)

            elif user_input == "3":

                search = input("Nombre o matrícula: ").lower()

                users = self.library_system.users_manager.load_data()

                for user in users:

                    if (
                        search in user["first_name"].lower()
                        or search in user["last_name"].lower()
                        or search in user["student_id"]
                    ):
                        self.mostrar_usuario(user)

            elif user_input == "4":

                # editar usuario
                user_id = input("Ingrese ID o Matrícula del usuario a editar: ")
                users = self.library_system.users_manager.load_data()
                found = False

                for user in users:
                    if user["id"] == user_id or user["student_id"] == user_id:
                        print("Deje vacío si no desea cambiar el dato.")
                        phone = input(f"Nuevo teléfono ({user['phone']}): ")
                        major = input(f"Nueva carrera ({user['major']}): ")
                        
                        if phone: user["phone"] = phone
                        if major: user["major"] = major
                        
                        self.library_system.users_manager.save_data(users)
                        print("Usuario actualizado.")
                        found = True
                        break
                if not found: print("Usuario no encontrado.")

            elif user_input == "5":

                user_id = input("Ingrese ID o Matrícula del usuario a eliminar: ")
                users = self.library_system.users_manager.load_data()
                loans = self.library_system.loans_manager.load_data()
                found = False

                for user in users:
                    if user["id"] == user_id or user["student_id"] == user_id:

                        tiene_prestamos = any(
                            loan["user_id"] == user["id"] and loan["status"] == "Activo"
                            for loan in loans
                        )

                        if tiene_prestamos:
                            print("El usuario tiene préstamos activos.")
                            break

                        user["status"] = "Inactivo"
                        self.library_system.users_manager.save_data(users)
                        print("Usuario eliminado (baja lógica).")
                        found = True
                        break
                if not found: print("Usuario no encontrado.")

            elif user_input == "6":
                break

    def manage_loans(self):
        # Mostrar submenú de préstamos
        # Registrar préstamo
        # Registrar devolución
        while True:

            user_input = input("""
            ===== GESTIÓN DE PRÉSTAMOS =====

            1. Registrar préstamo
            2. Registrar devolución
            3. Ver préstamos activos
            4. Volver

            Seleccione:
            """)


            if user_input == "1":

                # pedir usuario
                # pedir libro
                # validar
                # descontar copia
                # guardar préstamo

                print("\n===== NUEVO PRÉSTAMO =====")
                user_id = input("ID o Matrícula del usuario: ")
                book_id = input("ID o ISBN del libro: ")

                # Cargar datos
                users = self.library_system.users_manager.load_data()
                books = self.library_system.books_manager.load_data()
                
                # Buscar objetos
                user_data = next((u for u in users if u["id"] == user_id or u["student_id"] == user_id), None)
                book_data = next((b for b in books if b["id"] == book_id or b["isbn"] == book_id), None)

                if not user_data or not book_data:
                    print("Error: Usuario o Libro no encontrado.")
                    continue

                # Recrear objetos temporalmente para usar sus métodos
                user_obj = User(**user_data)
                book_obj = Book(**book_data)

                # Generar ID de préstamo y fechas
                loans = self.library_system.loans_manager.load_data()
                loan_id = f"PRS-{str(len(loans) + 1).zfill(4)}"
                
                fecha_actual = datetime.date.today()
                fecha_devolucion = fecha_actual + datetime.timedelta(days=7) # Presta por 7 días

                nuevo_prestamo = Prestamo(loan_id, user_obj.id, book_obj.id, str(fecha_actual), str(fecha_devolucion))

                # Validar usando el método de tu clase
                valido, mensaje = nuevo_prestamo.validar_prestamo(user_obj, book_obj)
                
                if valido:
                    # Descontar copia del libro y guardar
                    for b in books:
                        if b["id"] == book_obj.id:
                            b["available_copies"] -= 1
                            break
                    
                    self.library_system.books_manager.save_data(books)
                    self.library_system.loans_manager.add_entry(nuevo_prestamo.__dict__)
                    print(f"Préstamo exitoso. Fecha de devolución esperada: {fecha_devolucion}")
                else:
                    print(f"Préstamo rechazado: {mensaje}")


            elif user_input == "2":

                # buscar préstamo
                # finalizar
                # aumentar copia

                print("\n===== DEVOLUCIÓN =====")
                loan_id = input("ID del préstamo a devolver: ")
                loans = self.library_system.loans_manager.load_data()
                books = self.library_system.books_manager.load_data()

                found = False
                for loan in loans:
                    if loan["id"] == loan_id and loan["status"] == "Activo":
                        loan["status"] = "Finalizado"
                        loan["return_date"] = str(datetime.date.today())
                        
                        # Devolver copia al libro
                        for b in books:
                            if b["id"] == loan["book_id"]:
                                b["available_copies"] += 1
                                break
                        
                        self.library_system.loans_manager.save_data(loans)
                        self.library_system.books_manager.save_data(books)
                        print("Devolución registrada correctamente.")
                        found = True
                        break
                
                if not found:
                    print("No se encontró un préstamo activo con ese ID.")


            elif user_input == "3":

                loans = self.library_system.loans_manager.load_data()

                for loan in loans:

                    if loan["status"] == "Activo":
                        self.mostrar_prestamo(loan)


            elif user_input == "4":
                break

    def perform_queries(self):
        # Buscar libros
        # Buscar usuarios
        # Mostrar préstamos
        while True:

            user_input = input("""
            ===== CONSULTAS =====

            1. Buscar libro
            2. Buscar usuario
            3. Libros disponibles
            4. Libros agotados
            5. Préstamos activos
            6. Volver

            Seleccione:
            """)


            if user_input == "1":

                # llamar búsqueda libros
                search = input("Ingrese título, autor o ISBN: ").lower()
                books = self.library_system.books_manager.load_data()
                for book in books:
                    if (search in book["title"].lower() or search in book["author"].lower() or search in book["isbn"]):
                        print(f"ID: {book['id']} | Título: {book['title']} | Disponibles: {book['available_copies']}")


            elif user_input == "2":

                # llamar búsqueda usuarios
                search = input("Nombre o matrícula: ").lower()
                users = self.library_system.users_manager.load_data()
                for user in users:
                    if (search in user["first_name"].lower() or search in user["last_name"].lower() or search in user["student_id"]):
                        print(f"ID: {user['id']} | Nombre: {user['first_name']} {user['last_name']} | Estado: {user['status']}")


            elif user_input == "3":

                books = self.library_system.books_manager.load_data()

                for book in books:

                    if book["available_copies"] > 0:
                        self.mostrar_libro(book)


            elif user_input == "4":

                books = self.library_system.books_manager.load_data()

                for book in books:

                    if book["available_copies"] == 0:
                        self.mostrar_libro(book)


            elif user_input == "5":

                loans = self.library_system.loans_manager.load_data()

                for loan in loans:

                    if loan["status"] == "Activo":
                        self.mostrar_prestamo(loan)


            elif user_input == "6":
                break

    def generate_reports(self):
        # Pedir el reporte
        # Mostrarlo en pantalla
        books = self.library_system.books_manager.load_data()
        users = self.library_system.users_manager.load_data()
        loans = self.library_system.loans_manager.load_data()

        active_loans = sum(1 for loan in loans if loan["status"] == "Activo")
        
        # Calcular préstamos de hoy
        hoy = str(datetime.date.today())
        loans_today = sum(1 for loan in loans if loan["loan_date"] == hoy)

        # Encontrar libro y categoría más solicitados
        if not loans:
            most_requested_book_name = "N/A"
            top_category = "N/A"
        else:
            # Contar IDs de libros en los préstamos
            book_ids_in_loans = [loan["book_id"] for loan in loans]
            contador_libros = Counter(book_ids_in_loans)
            most_requested_id = contador_libros.most_common(1)[0][0]
            
            # Buscar el nombre y categoría de ese libro
            most_requested_book_name = "Desconocido"
            categorias_prestadas = []
            
            for b in books:
                if b["id"] == most_requested_id:
                    most_requested_book_name = b["title"]
                # Guardar las categorías de los libros prestados para el conteo de categorías
                if b["id"] in book_ids_in_loans:
                    # Agregamos la categoría tantas veces como se prestó el libro
                    veces_prestado = contador_libros[b["id"]]
                    categorias_prestadas.extend([b["category"]] * veces_prestado)
            
            contador_categorias = Counter(categorias_prestadas)
            top_category = contador_categorias.most_common(1)[0][0] if categorias_prestadas else "N/A"

        # Imprimir el reporte
        print(f"""
        ======== REPORTES ========
        Libros registrados: {len(books)}
        Usuarios registrados: {len(users)}
        Préstamos activos: {active_loans}
        Libros prestados hoy: {loans_today}
        Libro más solicitado: {most_requested_book_name}
        Categoría con más préstamos: {top_category}
        """)

    def display_menu(self):
        """Muestra el menú principal del sistema."""
        user = input("""
        =====================================
              SISTEMA DE BIBLIOTECA
        =====================================
        1. Gestión de libros
        2. Gestión de usuarios
        3. Gestión de préstamos
        4. Consultas
        5. Reportes
        6. Salir
        """)

        if user == "1":
            self.manage_books()
        elif user == "2":
            self.manage_users()
        elif user == "3":
            self.manage_loans()
        elif user == "4":
            self.perform_queries()
        elif user == "5":
            self.generate_reports()
        elif user == "6":
            print("\nSaliendo del sistema de biblioteca. ¡Hasta pronto!")
            return False
        else:
            print("\nOpción no válida. Por favor intente de nuevo.")
        return True
