CREATE DATABASE adacontabilidade;

USE adacontabilidade;

CREATE TABLE arquivos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_arquivo VARCHAR(255) NOT NULL,
    numero_linhas INT NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
