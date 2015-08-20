create table if not exists users (
    id integer primary key autoincrement,
    users text unique key,
    password text
    );
