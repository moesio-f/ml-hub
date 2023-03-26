USE Users;

INSERT IGNORE INTO 
user (username, password, registration_date, user_type, name, notes) 
VALUES ("root", 
        "admin", 
        "2023-01-01",
        "admin",
        "Administrador",
        "Esse é o usuário padrão de administração do sistema.");


INSERT IGNORE INTO 
has_permission (username, endpoint) 
SELECT "root", permission.endpoint
FROM permission;
