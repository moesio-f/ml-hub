# API Gateway

> Esse módulo é responsável pelo controle das requisições aos serviços do sistema. Por simplicidade, os endpoints de todos os serviços são armazenados em arquivos de configuração.
>
> - A API REST é implementada em Python 3 usando a biblioteca Flask.

## Anotações

- Lembrar que o JWT tem uma data de expiração, quando esse tempo ter passado do limite e for feita alguma solicitação, deve ser retornada uma resposta que o módulo Hub compreenda e solicite um novo JWT ao IAM Gateway;

