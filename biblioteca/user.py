class User:
    
    def __init__(self, id, first_name, last_name, student_id, major, email, phone, status="Activo"):
        if not first_name.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not last_name.strip():
            raise ValueError("El apellido no puede estar vacío.")

        if not email.strip():
            raise ValueError("El correo no puede estar vacío.")
        if "@" not in email or "." not in email:
            raise ValueError("El correo no es válido.")

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
        self.major = major
        self.email = email
        self.phone = phone
        self.status = status
    
    def cambiar_estado(self, nuevo_estado):
        """" Cambia el estado del usuario a Activo o Inactivo. """
        self.status = nuevo_estado