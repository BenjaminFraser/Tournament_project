#!/usr/bin/env python
# 
# sample_data.py -- sample database data for a Swiss-system tournament.
# imports two sets of ten players into two tournaments each, four total.
#

import random

from tournament import connect
from tournament import reportMatch
from tournament import createTournament
from tournament import tournamentPlayer
from tournament import deleteTournament

from tournament_test import testDelete


player_list = [
    (1, 'Benjamin'),
    (2, 'Peter'),
    (3, 'Tracy'),
    (4, 'Alexander'),
    (5, 'Phil'),
    (6, 'Jess'),
    (7, 'Felix'),
    (8, 'Norman'),
    (9, 'Shaun'),
    (10, 'Andrew')
]

player_list_02 = [
    (11, 'Ronald'),
    (12, 'Harry'),
    (13, 'Hermione'),
    (14, 'Hagrid'),
    (15, 'Padfoot'),
    (16, 'Lupin'),
    (17, 'Ginny'),
    (18, 'Albus'),
    (19, 'George'),
    (20, 'Fred')
]


def registerPlayerSample(player_id, name, tourn_id=1):
    """Add a player to the tournament database.
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO Player (player_id, name) VALUES (%s, %s)"
    db_cursor.execute(query, (player_id, name))
    db.commit()
    tournamentPlayer(player_id, tourn_id)
    db.commit()
    db.close()


def createRandomMatches(player_list, num_matches, tourn_id=1):
    num_players = len(player_list)
    for i in xrange(num_matches):
        print 'match1'
        player1_index = random.randint(0, num_players - 1)
        player2_index = random.randint(0, num_players - 1)
        if player2_index == player1_index:
            player2_index = (player1_index + 1) % num_players
        winner_id = player_list[player1_index][0]
        winner_name = player_list[player1_index][1]
        loser_id = player_list[player2_index][0]
        loser_name = player_list[player2_index][1]
        reportMatch(winner_id, loser_id, tourn_id)
        print "%s (id=%s) beat %s (id=%s)" % (
            winner_name,
            winner_id,
            loser_name,
            loser_id)


def setup_players_and_matches():
    testDelete()
    for player in player_list:
        registerPlayerSample(player[0], player[1], tourn_id=1)
        tournamentPlayer(player[0], 5)
    for player in player_list_02:
        registerPlayerSample(player[0], player[1], tourn_id=13)
        tournamentPlayer(player[0], 6)
    createRandomMatches(player_list, 100, tourn_id=1)
    createRandomMatches(player_list, 100, tourn_id=5)
    createRandomMatches(player_list_02, 100, tourn_id=13)
    createRandomMatches(player_list_02, 100, tourn_id=6)


if __name__ == '__main__':
    tournies = [5, 6, 13]
    for f in tournies:
        deleteTournament(tourn_id=f)
        print "Tournament %s deleted." % str(f)
    createTournament(5, 'Tournament 5')
    createTournament(6, 'Sixth')
    createTournament(13, 'Numero 13')
    setup_players_and_matches()
