CREATE DATABASE sakhi_saarthi;
USE sakhi_saarthi;

-- ADMIN TABLE
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);

INSERT INTO admin (username, password)
VALUES ('admin', 'admin123');

-- COMPLAINTS TABLE
CREATE TABLE complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50),
    description TEXT,
    status VARCHAR(20),
    date DATE,
    remarks TEXT
);

-- SCHEMES TABLE
CREATE TABLE schemes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    beneficiary VARCHAR(100)
);

-- ANGANWADI TABLE
CREATE TABLE anganwadi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    center_name VARCHAR(100),
    village VARCHAR(100),
    worker VARCHAR(100),
    services VARCHAR(200)
);
