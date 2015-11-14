#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
from multi_tourn_views import *
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def createTournament(tourn_id, name):
    """Inserts a new tournament id and name into the database. 
    
    For the created tournament, associated views are created as follows:
        players_tourn_x: listed players in tournament x
        games_tourn_x: listed games taken place in tournament x
        lost_games_x: player id and losses in tournament x
        won_games_x: player id, name and wins in tournament x
        combined_standings_x: combination of won and lost in tournament x
        player_standings_x: id, name, wins and total in tournament x
        ranked_standings_x: player_standings_x numbered by rank
        swiss_pairings_x: pairings for next match in tournament x
    """
    name = str(name)
    conn = connect()
    c = conn.cursor()
    # Insert the new tournament into table Tournament.
    query = "INSERT INTO Tournament (id, name) VALUES (%s, %s);"
    c.execute(query, (tourn_id, name))
    conn.commit()
    # Store view functions from multi_tourn_views.py within a list.
    function_list = [
        initTournPlayersView, 
        initTournGamesView, 
        initTournLostGames, 
        initTournWonGames, 
        initTournCombinedStand, 
        initTournPlayerStandings, 
        initTournRankedStandings, 
        initTournSwissPairings]

    # Iterate through function_list and execute each tourn view.
    for f in function_list:
        query = f(tourn_id)
        c.execute(query)
        conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    # Truncate both tournaments games tables only, preserving player records.
    c.execute("TRUNCATE TABLE games;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    # Truncate both tournaments players and games tables from the database.
    c.execute("TRUNCATE TABLE players, games")
    conn.commit()
    conn.close()


def countPlayers(tourn_id=1):
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    if tourn_id != 1:
        c.execute("SELECT count(player_id) FROM players WHERE tournament_id = %s;" % tourn_id)
    else:
        c.execute("SELECT count(player_id) FROM players WHERE tournament_id = 1;")
    count_result = c.fetchone()
    return count_result[0]
    conn.commit()
    conn.close()


def registerPlayer(name, tourn_id=1):
    """Registers a player and unique id into the players table."""

    conn = connect()
    c = conn.cursor()
    if tourn_id != 1:
        query = "INSERT INTO players (name, tournament_id) VALUES (%s, %s);"
    else:
        query = "INSERT INTO players (name, tournament_id) VALUES (%s, %s);"
    c.execute(query, (name, tourn_id))
    conn.commit()
    conn.close()


def playerStandings(tourn_id=1):
    """Returns a list of the players and their win records, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()
    # If tournament id varies from 1, fetch standings for tournament id.
    if tourn_id != 1:
        c.execute("SELECT * FROM player_standings_%s;" % tourn_id)
    else:
        # Use the view player_standings as defined within tournament.sql
        c.execute("SELECT * FROM player_standings;")
    performance_table = c.fetchall()
    return performance_table
    conn.commit()
    conn.close()


def reportMatch(winner, loser, tourn_id=1):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    # If tournament 2 chosen, select appropriate query. 
    if tourn_id != 1:
        # Query and execute code format to escape strings, avoiding SQL inj.
        query = "INSERT INTO games (win_ref, loose_ref, tournament_id) VALUES (%s, %s, %s);"
    else:
        query = "INSERT INTO games (win_ref, loose_ref, tournament_id) VALUES (%s, %s, %s);"
    c.execute(query, (winner, loser, tourn_id))
    conn.commit()
    conn.close()


def swissPairings(tourn_id=1):
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
    conn = connect()
    c = conn.cursor()
    if tourn_id != 1:
        # Use the swiss pairings view for tournament tourn_id
        c.execute("SELECT * FROM v_swiss_pairings_%s;" % tourn_id) 
    else:
        # Use the view v_swiss_pairings as defined within tournament.sql
        c.execute("SELECT * FROM v_swiss_pairings;")
    result = c.fetchall()
    return result
    conn.commit()
    conn.close()

createTournament(13, 'superdawgs')
