# drop database vslib;
# create database vflib;
use vflib;
SET foreign_key_checks = 0;
drop TABLE IF EXiSTS users;
drop TABLE IF EXiSTS books;
drop TABLE IF EXiSTS items;
drop TABLE IF EXiSTS borrow_records;
-- ------------------
CREATE TABLE users (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       nickname VARCHAR(255) not null,
                       username VARCHAR(255) not null,
                       position ENUM('student', 'teacher', 'admin') DEFAULT 'student',
                       pwd VARCHAR(255),
                       sex VARCHAR(255),
                       addr VARCHAR(255),
                       phone VARCHAR(255),
                       balance FLOAT(10,2)
);
INSERT INTO users (id, nickname, username, pwd, sex, addr, phone, balance, position)
VALUES
    (8209, 'j2ee', '张三', 'j2ee', '男', '北京市朝阳区', '13812345678', 1000.00, 'teacher'),
    (8210, '456', '李四', 'pass456', '女', '上海市浦东新区', '13987654321', 500.50, 'student'),
    (8211, 'abc', '王五', 'abc@123', '男', '广州市天河区', '13698765432', 300.75, 'student'),
    (8288, 'admin', '宋铁', 'admin', '男', '广州市天河区', '13698765432', 300.75, 'admin');
-- --------------------
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(255),
    name VARCHAR(255),
    price DECIMAL(10,2),
    author VARCHAR(255),
    publisher VARCHAR(255),
    category VARCHAR(255),
    img VARCHAR(255),
    publish_time VARCHAR(255),
    info VARCHAR(255),
    pages INT,
    borrow_times INT DEFAULT 0,
    want INT DEFAULT 0,
    is_hidden BOOLEAN DEFAULT FALSE
);
INSERT INTO books (id, isbn, name, price, author, publisher, category, img, publish_time, pages, borrow_times, want, info)
VALUES
    (1, '9787508654799', '活着', 39.80, '余华', '作家出版社', '小说', 'cover_image.jpg', '2012-09-01', 208, 120, 0, 'cn'),
    (2, '9787020002100', '白夜行', 29.80, '东野圭吾', '南海出版公司', '推理', 'cover_image.jpg', '2010-08-01', 400, 90, 0,'jp'),
    (3, '9787530219014', '三体', 45.00, '刘慈欣', '重庆出版社', '科幻', 'cover_image.jpg', '2008-01-01', 302, 200, 0, 'cn'),
    (4, '9787540455958', '围城', 26.80, '钱钟书', '人民文学出版社', '小说', 'cover_image.jpg', '2015-04-01', 528, 80, 0, 'cn');
-- -----------------------
CREATE TABLE items(
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      book_id INT not null,
                      is_borrowed BOOLEAN default false,
                      record_id INT default null,
                      foreign key (record_id) references borrow_records(id),
                      foreign key (book_id) references books(id)
);
INSERT INTO items(id, book_id, is_borrowed, record_id)
VALUES
    (101, 1, FALSE, null),
    (102, 1, FALSE, null),
    (103, 1, FALSE, null),
    (201, 2, TRUE, 2),
    (202, 2, FALSE, null),
    (301, 3, TRUE, 3),
    (302, 3, FALSE, null),
    (401, 4, FALSE, null),
    (402, 4, FALSE, null);
-- ----------------------
CREATE TABLE borrow_records(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT not null,
    isbn VARCHAR(255),
    book_id INT not null,
    item_id INT not null,
    book_name VARCHAR(255),
    borrow_time DATETIME not null,
    return_time DATETIME,
    foreign key (user_id) references users(id),
    foreign key (book_id) references books(id),
    foreign key (item_id) references items(id)
);
INSERT INTO borrow_records(id, user_id, item_id, isbn, book_id, book_name, borrow_time, return_time)
VALUES
    (1, 8209, 101, '9787508654799', 1, '活着', '2024-04-20 10:00:00', '2024-05-05 12:00:00'),
    (2, 8209, 201, '9787020002100', 2, '白夜行', '2024-04-21 09:30:00', NULL),
    (3, 8209, 301, '9787530219014', 3, '三体', '2024-04-22 14:15:00', NULL);
-- ----------------------
SET foreign_key_checks = 1;
