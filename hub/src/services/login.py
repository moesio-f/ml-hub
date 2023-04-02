"""Esse módulo provê funcionalidades de login.
"""
import requests


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
    response = requests.get('http://localhost:8080/iam/authenticate',
                            json={
                                'username': user,
                                'password': password
                            })

    if response.status_code != 200:
        raise ValueError()
    
    data = response.json()

    if 'jwt' in data:
        return data['jwt'], data['user_type']
    else:
        return ValueError()
