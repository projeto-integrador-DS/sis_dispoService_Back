-- SQLite

SELECT *
FROM profissionais AS pr
JOIN cursos AS cur ON pr.ID_profiss = cur.fk_idProfiss
JOIN experiencias AS exp ON pr.ID_profiss = exp.fk_idProfiss

DROP TABLE cursos;
DROP TABLE profissionais;
DROP TABLE experiencias;
DROP TABLE servicos;
DROP TABLE loginProf;
DROP TABLE clientes;
DROP TABLE oferece;


SELECT * FROM profissionais;
SELECT * FROM cursos;
SELECT * FROM loginProf;
SELECT * FROM experiencias;
SELECT * FROM clientes;
SELECT * FROM servicos;

SELECT * 
FROM loginProf 
WHERE username='lala';


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
WHERE pr.ID_profiss =3


SELECT serv.ID_servico, serv.nome, serv.categoria, serv.valor 
FROM oferece AS o 
JOIN profissionais AS pr on o.fk_profiss=pr.ID_profiss 
JOIN servicos AS serv ON o.fk_servic = serv.ID_servico
where o.fk_profiss=2

/*retorna todas as tabelas existentes do meu banco de dados*/
SELECT * FROM sqlite_master WHERE type = 'table';

SELECT * FROM servicos