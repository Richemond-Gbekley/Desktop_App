
use desktopdb;
CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Firstname VARCHAR(255),
    Lastname VARCHAR(255),
    Email VARCHAR(255),
    login_time DATETIME
);
select * from login_logs;
select * from registerdb;

drop table login_logs;