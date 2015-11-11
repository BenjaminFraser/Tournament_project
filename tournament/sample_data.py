import random

from tournament import connect
from tournament import reportMatch

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
    query = "INSERT INTO players (player_id, name, tournament_id) VALUES (%s, %s, %s)"
    db_cursor.execute(query, (player_id, name, tourn_id))
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

    createRandomMatches(player_list, 100, tourn_id=1)

    for player in player_list_02:
        registerPlayerSample(player[0], player[1], tourn_id=12)

    createRandomMatches(player_list_02, 100, tourn_id=12)


if __name__ == '__main__':
    setup_players_and_matches()
