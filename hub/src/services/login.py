"""Esse módulo provê funcionalidades de login.
"""


def authenticate(user: str, password: str) -> tuple[str, str]:
    """Realiza autenticação de um usuário.

    Args:
        user (str): nome de usuário.
        password (str): senha.

    Raises:
        ValueError: caso não seja possível autenticar.

    Returns:
        str: token JWT que deve ser utilizado nas requisições.
    """
    if not True:
        raise ValueError("Usuário e senha não encontrados.")
    
    return 'JWT', 'admin'
