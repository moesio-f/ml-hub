CREATE DATABASE IF NOT EXISTS Users;
USE Users;

CREATE TABLE IF NOT EXISTS user (
    `username` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci PRIMARY KEY,
    `password` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `registration_date` DATE NOT NULL,
    `user_type` ENUM('admin', 'normal') NOT NULL,
    `name` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `notes` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
    
);

CREATE TABLE IF NOT EXISTS permission (
    `endpoint` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci PRIMARY KEY,
    `description` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci,
    `name` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci
);

CREATE TABLE IF NOT EXISTS has_permission (
    `username` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci,
    `endpoint` VARCHAR(256) CHARACTER SET utf8 COLLATE utf8_general_ci,
    Foreign Key (`username`) REFERENCES user(`username`),
    Foreign Key (`endpoint`) REFERENCES permission(`endpoint`)
);

