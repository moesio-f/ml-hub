# ML Hub: a Machine Learning Hub for Developers

Esse repositório contém o *ML Hub*, um projeto desenvolvido para facilitar o acesso a recursos computacionais distribuídos para o treinamento, registro e monitoramento de modelos de Aprendizagem de Máquina (ML).

O escopo do projeto se restringe às questões de experimentação e de desenvolvimento, não considerando o processo de servimento de modelos aos usuários finais. Em outras palavras, o ML Hub é um facilitador para experimentação dentro de um projeto de ML. 

## Visão Geral

O projeto utiliza uma arquitetura orientada a serviços (SOA). Em particular, os componentes do sistema disponibilizam uma ou mais funcionalidades através de APIs. 

Iremos considerar que o aplicativo opera em uma zona "low trust", onde após a autenticação os usuários são considerados seguros e não é necessário gerar tokens temporários. 

![](.img/architecture.png)

## Componentes

- **Aplicativo cliente** ([hub](hub)): interface para acessar os recursos compartilhados;
  - Interface gráfica;
  - Faz requisições a APIs dos outros serviços;
  - Módulo de login;
  - Módulo de autenticação;
  - Implementado em Python usando a biblioteca PySimpleGUI;
- **API Gateway**: realiza autenticação de solicitações e realiza as solicitações aos respectivos serviços;
  - Esse componente realiza a checagem de permissões para o usuário autenticado;
  - Repassa as solicitações para os respectivos serviços;
  - Armazena métricas relacionadas com as solicitações;
  - Implementado em Python usando Flask;
- **IAM Gateway**: sistema simples com login e senha;
  - Faz solicitações ao serviço de controle de usuário para obtenção de um JWT;
  - Repassa as solicitações para os respectivos serviços;
  - Implementado em Python usando Flask e PyJWT;
- **Serviço de Artefatos**: responsável acesso e controle dos artefatos (modelos, datasets).
  - API RESTful para comunicação;
  - Reúne os dados (CSVs) armazenados pelo usuário;
  - Reúne os modelos (binários) armazenados pelo usuário;
  - Também armazena metadados (usuário que fez upload, tipo do artefato, data de upload, etc);
  - Implementado em Java usando Spring;
- **Serviço de controle de usuários**
  - API RESTful para comunicação com o BD relacional;
  - Reúne todos os usuários do sistema;
  - Permite checagem de usuário-senha;
  - Armazena meta-dados dos usuários (e.g., tipo, data de criação);
  - Implementado em Java usando Spring;
- **Serviço de Treinamento**
  - API RESTful para comunicação com o serviço;
  - Seleção da pipeline de treinamento (scikit-learn);
  - Seleção do dataset que deve ser utilizado;
  - Salvamento e obtenção do modelo (possibilidade de salvar diretamente o artefato);
  - Implementado em Python usando Flask e Celery;
  - RabbitMQ como MOM;
- **~~Serviço de Predição~~** (suporte removido, complexidade atual do sistema já é suficiente)
  - API RESTful para comunicação com o serviço;
  - Selecionar um modelo;
  - Selecionar um dataset ou passar entradas manuais;
  - Retorna os resultados como um report;


## Usuários e Funcionalidades

### Administrador

- Criação de contas de usuários;
- Controle de permissões de acesso (IAM);
- Dashboards de monitoramento de recursos;

### Usuário

- Registro de artefatos (modelos e datasets);
- Treinamento de modelos de ML usando o scikit-learn;
- ~~Avaliação em batch para um dado modelo;~~

# Referências

- https://deimos.io/post/authentication-and-authorization-in-a-distributed-system
- https://wso2.com/blogs/cloud/end-user-authentication-via-api-gateway/
- https://www.styra.com/blog/centralized-vs-distributed-authorization-the-cap-theorem/
