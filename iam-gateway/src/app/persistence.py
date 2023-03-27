"""Esse módulo contém utilidades para
persistência de JWTs.
"""

import json
from entities import UserJWT
import pathlib


_SAVE_PATH = pathlib.Path('.ml_hub_iam', 'tokens')
_SAVE_PATH.mkdir(parents=True, exist_ok=True)


def save_user_jwt(jwt: UserJWT) -> None:
    """Realiza o salvamento de um JWT para um dado usuário.
    """
    p = _SAVE_PATH.joinpath(f'{jwt.username}.jwt')
    f = p.open('w+')
    json.dump(jwt.asdict(),
              f,
              indent=4,
              ensure_ascii=False)
    f.close()


def read_user_jwt(username: str) -> UserJWT | None:
    """Realiza o carregamento do JWT para um dado usuário.

    Args:
        username (str): nome do usuário.

    Returns:
        UserJWT: JWT para esse usuário.
    """
    p = _SAVE_PATH.joinpath(f'{username}.jwt')

    if not p.exists():
        return None

    f = p.open('r')
    jwt = json.load(f)
    f.close()
    return UserJWT.loadFromDict(jwt)
