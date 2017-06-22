CREATE DATABASE shadow_db DEFAULT CHARACTER SET utf8;
USE shadow_db;

CREATE TABLE t_server_list (
    f_id INT PRIMARY KEY AUTO_INCREMENT,
    f_host VARCHAR(50) NOT NULL,
    f_port INT DEFAULT 22 NOT NULL,
    f_user VARCHAR(50) DEFAULT 'root' NOT NULL,
    f_password VARCHAR(50) NOT NULL
) CHARSET=utf8;


#INSERT INTO t_server_list(f_host, f_password) VALUES ('host', 'password');
