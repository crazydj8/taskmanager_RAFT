CREATE DATABASE taskmanager;
USE taskmanager;
CREATE TABLE tasks 
(
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    assigned_to VARCHAR(255),
    priority ENUM('Low', 'Medium', 'High') NOT NULL,
    status ENUM('To Do', 'In Progress', 'Done') NOT NULL
);

INSERT INTO tasks (task, assigned_to, priority, status) VALUES ('Complete project proposal','Akshat', 'High', 'In Progress');
INSERT INTO tasks (task, assigned_to, priority, status) VALUES ('Prepare presentation slides', 'Ankush', 'Medium', 'To Do');
INSERT INTO tasks (task, assigned_to, priority, status) VALUES ('Review code for bug fixes', 'Avani', 'Medium', 'Done');
INSERT INTO tasks (task, assigned_to, priority, status) VALUES ('Push the changes', 'Ayra', 'Low', 'In Progress');