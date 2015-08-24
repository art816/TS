create table if not exists users (
    id integer primary key autoincrement,
    user_login text not NULL UNIQUE,
    user_name text not NULL,
    user_s_name text not NULL,
    user_class int not NULL,
    user_mail text not NULL,
    user_password text not NULL,
    UNIQUE (user_name, user_s_name)
    );