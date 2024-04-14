CREATE DATABASE taskmanager;
USE taskmanager;
CREATE TABLE tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    assigned_to VARCHAR(255),
    priority ENUM('Low', 'Medium', 'High') NOT NULL,
    status ENUM('To Do', 'In Progress', 'Done') NOT NULL
);