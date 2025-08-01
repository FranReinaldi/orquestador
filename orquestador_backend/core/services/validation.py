import time
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

def validate_user(user_id: str) -> None:
    """
    Lógica hardcodeada para validar un usuario.
    Simula que solo usuarios que empiecen con 'user_' son válidos.
    """
    logger.info(f"Iniciando validación de usuario: {user_id}")

    if not user_id.startswith("user_"):
        logger.warning(f"Usuario inválido: {user_id}")
        raise ValidationError(f"Usuario inválido: {user_id}")

    logger.info(f"Usuario {user_id} validado correctamente.")
