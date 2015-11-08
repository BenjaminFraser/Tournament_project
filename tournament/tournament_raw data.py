#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE TABLE games;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE TABLE players, games")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(player_id) FROM players;")
    count_result = c.fetchone()
    return count_result[0]
    conn.commit()
    conn.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    query = "INSERT INTO players (name) VALUES (%s);"
    c.execute(query, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM player_standings;")
    performance_table = c.fetchall()
    return performance_table
    conn.commit()
    conn.close()



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    query = "INSERT INTO games (win_ref, loose_ref) VALUES (%s, %s);"
    c.execute(query, (winner, loser))
    conn.commit()
    conn.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    player_standings = playerStandings()
    pairing_results = []

    """for i in range(0, len(player_standings), 2):
        pairing_results_a.append(player_standings[i])
        print 'Added number %s to the tuples' % (i)
    print pairing_results_a

    for i in range(1, len(player_standings), 2):
        pairing_results_b.append(player_standings[i])
        print 'Added number %s to the tuples' % (i)

    print pairing_results_a[1][0]"""

   

    for i in range(0, (len(player_standings)-1), 2):
        one = player_standings[i][0]
        two = player_standings[i+1][0]
        three = player_standings[i+1][0]
        four = player_standings[i+1][1]
        pairing_results.append((one, two, three, four))
    print pairing_results
    return pairing_results

    #if len(player_standings) % 2 != 0:
        #for a, b in player_standings[]

    #pairing_results = zip(a[1], a[2], b[1], b[2])
