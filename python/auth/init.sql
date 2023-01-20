-- use these credentials to access database via auth service 
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123!'; 

-- create auth database 
CREATE DATABASE auth; 

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost'; 

USE auth; 

-- create use table 
create TABLE user(
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
 email VARCHAR(255) NOT NULL UNIQUE, 
 userPassword VARCHAR(255) NOT NULL
); 

--create test user 
INSERT INTO user (email, userPassword) VALUES ('asrithabodepudi@gmail.com', 'LOCKWOOD')
