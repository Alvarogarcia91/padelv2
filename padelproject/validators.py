from django.core.exceptions import ValidationError
import re

class NumberValidator:
    def validate(self, password, user=None):
        if not re.search(r'\d', password):  # Verifica que la contraseña tenga al menos un número
            raise ValidationError("Password must have at least one number.")

    def get_help_text(self):
        return "Password must have at least one number."
