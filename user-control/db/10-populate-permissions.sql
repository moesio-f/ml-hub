USE Users;

INSERT IGNORE INTO 
permission (endpoint, description, name) 
VALUES ("/user-control/list", 
        "Obtém uma lista de todos os usuários cadastrados no sistema.", 
        "User Control: LIST"),
        ("/user-control/get/",
        "Obtém informações de 1 usuário do sistema.",
        "User Control: GET"),
        ("/user-control/delete/",
        "Remove um usuário do sistema.",
        "User Control: DELETE"),
        ("/user-control/create/",
        "Adiciona um usuário do sistema.",
        "User Control: CREATE"),
        ("/user-control/update/",
        "Atualiza informações de um usuário do sistema.",
        "User Control: UPDATE");
