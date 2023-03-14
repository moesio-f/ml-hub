# Módulo de Predições

> Esse módulo provê o serviço de predição de modelos.
>
> - A API é implementada em Python 3, usando Flask + Celery.
> - O MOM é o RabbitMQ.
> - Os workers são containers do Docker que utilizam uma imagem Python 3 com Celery.

Funcionamento: as tasks executam o treinamento, copiamos o arquivo python dentro do container e nele importamos e chamamos uma função padrão de treino.
