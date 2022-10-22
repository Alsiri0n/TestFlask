CREATE TABLE IF NOT EXISTS mainmenu (
    id serial PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    cururl VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id serial PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    posttext VARCHAR(255) NOT NULL,
    posttime timestamp NOT NULL
);