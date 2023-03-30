# ~~Módulo de Predições~~

> **Esse módulo foi depreciado, o sistema atualmente já apresenta complexidade suficiente para o escopo da disciplina**.
>
> Por ora, esse módulo não será implementado. A adição de um novo módulo acarreta em maior complexidade do API Gateway bem como do módulo front-end, além de necessitar de mais recursos.

> Esse módulo provê o serviço de predição de modelos.
>
> - A API é implementada em Python 3, usando Flask + Celery.
> - O MOM é o RabbitMQ.
> - Os workers são containers do Docker que utilizam uma imagem Python 3 com Celery.

Funcionamento: as tasks executam o treinamento, copiamos o arquivo python dentro do container e nele importamos e chamamos uma função padrão de treino.
