CREATE TABLE IF NOT EXISTS mainmenu (
    id serial PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    cururl VARCHAR(255) NOT NULL
);