-- SQLite

SELECT *
FROM profissionais AS pr
JOIN cursos AS cur ON pr.ID_profiss = cur.fk_idProfiss
JOIN experiencias AS exp ON pr.ID_profiss = exp.fk_idProfiss




DROP TABLE cursos;
DROP TABLE profissionais;
DROP TABLE experiencias;

SELECT * FROM profissionais;
SELECT * FROM cursos;
SELECT * FROM experiencias;