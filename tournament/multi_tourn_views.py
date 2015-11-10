#!/usr/bin/env python
#
# View string compiler for multiple tournaments for tournament.py

def initialiseTournPlayersView(t_id):
	""" Returns SQL query string applicable to tourn players view """
	tourn_players = ('CREATE VIEW players_tourn_%s as '
    'select player_id, name from players WHERE tournament_id = %s;' % (2*(t_id,)))
	return tourn_players


def initialiseTournGamesView(t_id):
    """ Returns SQL query string applicable to tourn games view """
    tourn_games = ('CREATE VIEW games_tourn_%s as '
    'select id, win_ref, loose_ref from games WHERE tournament_id = %s;' % (2*(t_id,)))
    return tourn_games


def initialiseTournLostGames(t_id):
    """ Returns SQL query string applicable to tourn lost games view """
    lost_games = ('CREATE VIEW v_lost_games_%s as '
        'select players_tourn_%s.player_id, count(loose_ref) as lost_games from ' 
        'players_tourn_%s left join games_tourn_%s on players_tourn_%s.player_id = games_tourn_%s.loose_ref ' 
        'group by players_tourn_%s.player_id;' % (7*(t_id,)))
    return lost_games

def initialiseTournWonGames(t_id):
    """ Returns SQL query string applicable to tourn won games view """
    won_games = ('CREATE VIEW v_won_games_%s as '
        'select players_tourn_%s.name, players_tourn_%s.player_id, wins from players_tourn_%s '
        'left join (select players_tourn_%s.player_id, count(win_ref) as wins '
        'from players_tourn_%s left join games_tourn_%s ' 
        'on players_tourn_%s.player_id = games_tourn_%s.win_ref '
        'group by players_tourn_%s.player_id) as win_num ' 
        'on players_tourn_%s.player_id = win_num.player_id order by wins desc;' % (11*(t_id,)))
    return won_games


def initialiseTournCombinedStand(t_id):
    """ Returns SQL query string applicable to tourn combined standings view """
    combined_standings = ('CREATE VIEW v_combined_standings_%s as '
        'select name, table1.player_id, wins, lost_games '
        'from v_won_games_%s as table1 '
        'join v_lost_games_%s as table2 on table1.player_id = table2.player_id '
        'order by wins desc;' % (3*(t_id,)))
    return combined_standings

def initialiseTournPlayerStandings(t_id):
    """ Returns SQL query string applicable to tourn player standings view. """
    player_standings = ('CREATE VIEW player_standings_%s as '
        'select v_won_games_%s.player_id, name, v_won_games_%s.wins, total_games from ' 
        'v_won_games_%s join (select player_id, SUM(wins + lost_games) as total_games '
        'from v_combined_standings_%s group by player_id) as totaltable '
        'on v_won_games_%s.player_id = totaltable.player_id order by wins desc;' % (6*(t_id,)))
    return player_standings


def initTournRankedStandings(t_id):
    """ Returns SQL query string for tourn ranked standings view. """
    ranked_standings = ('CREATE VIEW ranked_standings_%s as '
        'select row_number() over (order by wins desc) '
        'as rank, player_id, name, wins, total_games from player_standings_%s;' % (2*(t_id,)))
    return ranked_standings


def initTournSwissPairings(t_id):

	swiss_pairings = ('CREATE VIEW v_swiss_pairings_%s as '
        'select a.player_id as "player_1_id", a.name as "player_1_name", '
        'b.player_id as "player_2_id", b.name as "player_2_name" '
        'from ranked_standings_%s a, ranked_standings_%s b '
        'where a.rank+1 = b.rank and a.rank %% 2 = 1;' % (3*(t_id,)))
	return swiss_pairings

print initialiseTournCombinedStand(4), '\n'
print initialiseTournWonGames(5), '\n'
print initialiseTournLostGames(6), '\n'
print initialiseTournGamesView(7), '\n'
print initialiseTournPlayersView(8), '\n'
print initialiseTournPlayerStandings(9), '\n'
print initTournRankedStandings(10), '\n'
print initTournSwissPairings(1), '\n'