"""Esse módulo contém definições
para geração de JWTs.
"""

import jwt
from entities import UserJWT
from datetime import datetime


def get_jwt(username: str,
            user_type: str,
            key: str,
            creation_date: datetime,
            expiration_date: datetime) -> UserJWT:
    create_date = creation_date.strftime("%d/%m/%y-%H:%M:%S")
    exp_date = expiration_date.strftime("%d/%m/%y-%H:%M:%S")
    encoded = jwt.encode({
        'user': username,
        'user_type': user_type,
        'expiration_date': exp_date
    },
    key,
    algorithm="HS256")

    return UserJWT(username=username,
                   user_type=user_type,
                   creation_date=create_date,
                   expiration_date=exp_date,
                   jwt=encoded,
                   key=key)
