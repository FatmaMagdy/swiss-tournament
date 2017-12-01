-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players(
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE matches(
    match_id SERIAL PRIMARY KEY ,
    winner INT REFERENCES players(player_id) ,
    loser INT REFERENCES players(player_id) 
);

CREATE VIEW standings AS
SELECT players.player_id, players.name,
(SELECT count(matches.winner)
    FROM matches
    WHERE players.player_id = matches.winner)
    AS no_of_wins,
(SELECT count(matches.match_id)
    FROM matches
    WHERE players.player_id = matches.winner
    OR players.player_id = matches.loser)
    AS no_of_matches
FROM players
ORDER BY no_of_wins DESC, no_of_matches DESC;

