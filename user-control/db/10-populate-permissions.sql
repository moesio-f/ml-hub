USE Users;

INSERT IGNORE INTO 
permission (endpoint, description, name) 
VALUES ("/user-control/list", 
        "Obtém uma lista de todos os usuários cadastrados no sistema.", 
        "user_control.list"),
        ("/user-control/get/",
        "Obtém informações de 1 usuário do sistema.",
        "user_control.get"),
        ("/user-control/delete/",
        "Remove um usuário do sistema.",
        "user_control.delete"),
        ("/user-control/create/",
        "Adiciona um usuário do sistema.",
        "user_control.create"),
        ("/user-control/update/",
        "Atualiza informações de um usuário do sistema.",
        "user_control.update");
