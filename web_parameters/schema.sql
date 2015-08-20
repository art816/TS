create table if not exists users (
    id integer primary key autoincrement,
    user_name text not NULL,
    user_s_name text not NULL,
    user_class int,
    user_mail text,
    user_password text,
    UNIQUE (user_name, user_s_name)
    );