import json


class JsonManager:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Carga la información almacenada en el archivo JSON."""
        try:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_data(self, data):
        """Guarda la información en el archivo JSON."""
        with open(self.file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    def add_entry(self, entry):
        """Agrega una nueva entrada al archivo JSON."""
        data = self.load_data()
        data.append(entry)
        self.save_data(data)
