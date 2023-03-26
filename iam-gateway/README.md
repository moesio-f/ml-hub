# IAM Gateway

> Esse módulo é responsável pela autenticação e autorização dos usuários do sistema.
>
> - Esse módulo é implementado em **Python 3** usando a biblioteca PyJWT;

## Anotações

- Ordem de checagem por autenticação: (1) checar se o usuário existe no sistema; (2) checar se a senha é correta; (3) gerar JWT com data de expiração;
- Ordem de checagem por autorização: (1) checar se o usuário faz parte do sistema; (2) checar se o token é válido;


# Referências

- https://jwt.io/introduction
- https://developers.onelogin.com/authentication/tools/jwt
- 