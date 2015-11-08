import random

from tournament import connect
from tournament import reportMatch

from tournament_test import testDelete


the_players = [
    (1, 'Jeff'),
    (2, 'Adarsh'),
    (3, 'Amanda'),
    (4, 'Eduardo'),
    (5, 'Philip'),
    (6, 'Jee')
]


def registerPlayerUpdated(player_id, name):
    """Add a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    db_cursor = db.cursor()
    query = "INSERT INTO players (player_id, name) VALUES (%s, %s)"
    db_cursor.execute(query, (player_id, name))
    db.commit()
    db.close()

for player in the_players:
        registerPlayerUpdated(player[0], player[1])