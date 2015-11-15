-- Table definitions and custom views for the tournament project.

-- Delete the database if tournament exists on executing the file.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Create a Tournament table for each available tournament.
CREATE TABLE Tournament (
        id serial PRIMARY KEY, 
        name varchar(150) NOT NULL);


-- Insert tournament 1 into Tournament table with id 1. 
INSERT INTO Tournament (id, name) VALUES (1, 'First tournament');


-- Create a players table with id (primary key) and name.
CREATE TABLE Player (
        player_id serial PRIMARY KEY,
	name varchar(40) NOT NULL);


-- Create a tournament table matching player_id's to their tournaments.
CREATE TABLE Tournament_player (
        player_id integer REFERENCES Player (player_id),
        tournament_id integer REFERENCES Tournament (id),
        PRIMARY KEY (player_id, tournament_id));


-- Create a Game table with 3 foreign keys linking to 
-- Player table player id and Tournament table id.
-- Use CHECK (win_ref <> loose_ref) to ensure winner is different to looser.
CREATE TABLE Game (
        id serial PRIMARY KEY,
	win_ref integer REFERENCES Player (player_id) ON DELETE CASCADE,
	loose_ref integer REFERENCES Player (player_id) ON DELETE CASCADE,
        tournament_id integer REFERENCES Tournament (id)
        CHECK (win_ref <> loose_ref));


-- Create a view to list players in tournament 1 only, with name and id.
CREATE VIEW players_tourn_1 as
        select Player.player_id, Player.name 
        from Player join Tournament_player 
        on Player.player_id = Tournament_player.player_id 
        AND Tournament_player.tournament_id = 1; 


-- Create a view to list matches in tournament 1 only.
CREATE VIEW games_tourn_1 as
        select id, win_ref, loose_ref from Game where tournament_id = 1;


-- Create a view that lists a player_id along with associated loss record.
CREATE VIEW lost_games_1 as
        select players_tourn_1.player_id, count(loose_ref) as lost_games from 
        players_tourn_1 left join games_tourn_1 
        on players_tourn_1.player_id = games_tourn_1.loose_ref 
        group by players_tourn_1.player_id;


-- Create a view that displays a players id, name and win count to aid further views.
CREATE VIEW won_games_1 as
        select players_tourn_1.name, players_tourn_1.player_id, wins from players_tourn_1
        left join (select players_tourn_1.player_id, count(win_ref) as wins 
        from players_tourn_1 left join games_tourn_1 
        on players_tourn_1.player_id = games_tourn_1.win_ref 
        group by players_tourn_1.player_id) as win_num 
        on players_tourn_1.player_id = win_num.player_id order by wins desc;


-- A combined view showing id, name, wins and losses.
CREATE VIEW combined_standings_1 as
        select name, table1.player_id, wins, lost_games
        from won_games_1 as table1
        join lost_games_1 as table2 on table1.player_id = table2.player_id 
        order by wins desc;


-- Create a view that combines the id, name and won games from combined standings, with 
-- a new column called total_games, which is derived from wins + lost games.
CREATE VIEW player_standings_1 as
        select won_games_1.player_id, name, won_games_1.wins, total_games from 
        won_games_1 join (select player_id, SUM(wins + lost_games) as total_games 
        from combined_standings_1 group by player_id) as totaltable 
        on won_games_1.player_id = totaltable.player_id order by wins desc;


-- Number each player standing row through adding a row number with row_number().
CREATE VIEW ranked_standings_1 as 
        select row_number() over (order by wins desc) 
        as rank, player_id, name, wins, total_games from player_standings_1;


-- Perform a self-join on view ranked_standings to produce a swiss pairings view with
-- player 1 id and name, and player 2 id and name on the same row. 
CREATE VIEW swiss_pairings_1 as 
        select a.player_id as "player_1_id", a.name as "player_1_name", 
        b.player_id as "player_2_id", b.name as "player_2_name"
        from ranked_standings_1 a, ranked_standings_1 b 
        where a.rank+1 = b.rank and a.rank % 2 = 1;
