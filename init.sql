GRANT ALL PRIVILEGES ON DATABASE dev TO devuser;
CREATE TABLE "users"(
    id serial primary key,
    username varchar(50) unique not null,
    password varchar(50) not null,
    email varchar(50)
);
CREATE TABLE "offers"(
    id serial primary key,
    user_id integer references users(id),
    title varchar(255) not null,
    text text
);