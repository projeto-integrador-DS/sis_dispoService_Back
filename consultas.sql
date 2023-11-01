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
SELECT * -- SQLite
/*filtra os cursos de um determinado profissional*/
SELECT c.modalidade, c.instituicao, c.area
FROM cursos AS c
JOIN profissionais AS pr ON pr.ID_profiss = c.fk_idProfiss
WHERE pr.ID_profiss =1

/*filtra as experiências de um determinado profissional*/
SELECT exp.cargo, exp.temp_servico, exp.empresa
FROM experiencias AS exp
JOIN profissionais AS pr ON pr.ID_profiss = exp.fk_IDprofiss
WHERE pr.ID_profiss =1

/*retorna todas as tabelas existentes do meu banco de dados*/
SELECT * FROM sqlite_master WHERE type = 'table';

SELECT * FROM servicos

