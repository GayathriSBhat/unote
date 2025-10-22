# unote

## How to run
1. python3 -m app.setup_db
2. uvicorn app.main:app --reload

## How to create db if it doesnt exists

CREATE DATABASE IF NOT EXISTS notesdb;
DROP USER IF EXISTS 'notes_user'@'localhost';
DROP USER IF EXISTS 'notes_user'@'127.0.0.1';
CREATE USER 'notes_user'@'localhost' IDENTIFIED BY 'notes_pass';
CREATE USER 'notes_user'@'127.0.0.1' IDENTIFIED BY 'notes_pass';
GRANT ALL PRIVILEGES ON notesdb.* TO 'notes_user'@'localhost';
GRANT ALL PRIVILEGES ON notesdb.* TO 'notes_user'@'127.0.0.1';
FLUSH PRIVILEGES;