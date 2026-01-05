CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    sexe VARCHAR(10),
    date_naissance DATE,
    taille FLOAT NOT NULL
);

CREATE TABLE weight_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    poids FLOAT NOT NULL,
    taille FLOAT NOT NULL,
    imc FLOAT NOT NULL,
    categorie_imc VARCHAR(50) NOT NULL
);

CREATE TABLE meal_logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    date DATE NOT NULL,
    type_repas VARCHAR(50),
    calories INT
);
