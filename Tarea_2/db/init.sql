CREATE EXTENSION "uuid-ossp";

CREATE TABLE products (
    id  TEXT PRIMARY KEY,
    name TEXT, 
    price TEXT,
    email TEXT
);
