INSERT INTO users (nom, prenom, sexe, date_naissance, taille)
VALUES ('Dupont', 'Jean', 'Homme', '1998-06-15', 1.75);

INSERT INTO weight_logs (user_id, date, poids, imc, categorie_imc) VALUES
(1, '2025-03-01', 80, 26.12, 'Surpoids'),
(1, '2025-04-01', 78, 25.47, 'Surpoids'),
(1, '2025-05-01', 75, 24.49, 'Poids normal');

INSERT INTO meal_logs (user_id, date, type_repas, calories) VALUES
(1, '2025-03-01', 'Déjeuner', 700),
(1, '2025-03-01', 'Dîner', 600),
(1, '2025-04-01', 'Déjeuner', 650),
(1, '2025-05-01', 'Dîner', 550);

