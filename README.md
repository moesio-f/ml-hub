# ML Hub: a Machine Learning Hub for Developers

Esse repositório contém o *ML Hub*, um projeto desenvolvido para facilitar o acesso a recursos computacionais distribuídos para o treinamento, registro e monitoramento de modelos de Aprendizagem de Máquina (ML).

O escopo do projeto se restringe às questões de experimentação e de desenvolvimento, não considerando o processo de servimento de modelos aos usuários finais. Em outras palavras, o ML Hub é um facilitador para experimentação dentro de um projeto de ML. 

## Visão Geral

O projeto utiliza uma arquitetura orientada a serviços (SOA). Em particular, os componentes do sistema disponibilizam uma ou mais funcionalidades através de APIs. 

Iremos considerar que o aplicativo opera em uma zona "low trust", onde após a autenticação os usuários são considerados seguros e não é necessário gerar tokens temporários.

## Componentes

- **Aplicativo cliente**: interface para acessar os recursos compartilhados;
  - Interface gráfica;
  - Faz requisições a APIs dos outros serviços;
  - Módulo de login;
  - Módulo de autenticação;
- **API Gateway**: realiza autenticação de solicitações e realiza as solicitações aos respectivos serviços;
  - Esse componente realiza a checagem de permissões para o usuário autenticado;
  - Repassa as solicitações para os respectivos serviços;
- **IAM Gateway**: sistema simples com login e senha;
  - Faz solicitações ao serviço de controle de usuário para obtenção de um JWT;
  - Repassa as solicitações para os respectivos serviços;
- **Serviço de Artefatos**: responsável acesso e controle dos artefatos (modelos, datasets).
  - API RESTful para comunicação;
  - Reúne os dados (CSVs e JSONs) armazenados pelo usuário;
  - Reúne os modelos (binários) armazenados pelo usuário;
  - Também armazena metadados (usuário que fez upload, tipo do artefato, data de upload, etc);
- **Serviço de controle de usuários**
  - API RESTful para comunicação com o BD relacional;
  - Reúne todos os usuários do sistema;
  - Permite checagem de usuário-senha;
  - Armazena meta-dados dos usuários (e.g., ID, data de criação);
- **Serviço de Treinamento**
  - API RESTful para comunicação com o serviço;
  - Upload de código Python (versão, requisitos do pip);
    - Padronizado: script com função X para treinamento;
  - Seleção do dataset que deve ser utilizado;
- **Serviço de Predição**
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
- Treinamento de modelos de ML através de Script's Python;
- Avaliação em batch para um dado modelo;

# Referências

- https://deimos.io/post/authentication-and-authorization-in-a-distributed-system
- https://wso2.com/blogs/cloud/end-user-authentication-via-api-gateway/
- https://www.styra.com/blog/centralized-vs-distributed-authorization-the-cap-theorem/
