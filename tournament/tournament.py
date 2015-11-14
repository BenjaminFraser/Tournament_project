#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

# Fetch multi tournament view functions for createTournament().
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


def removeTournamentPlayers(tourn_id):
    """Remove all the players from the selected tournament."""
    conn = connect()
    c = conn.cursor()
    # Delete the tournament registrations from Tournament_player table.
    c.execute("DELETE FROM Tournament_player "
        "WHERE tournament_id = %s;" % (tourn_id,))
    conn.commit()
    conn.close()


def deleteTournament(tourn_id):
    """Remove all the speified tournament data from the database."""
    # If not already cleared, remove tournament players from the tournament. 
    try: 
        removeTournamentPlayers(tourn_id) 
    except: 
        pass
    conn = connect()
    c = conn.cursor()
    # Delete the tournament data from Game table.
    c.execute("DELETE FROM Game "
        "WHERE tournament_id = %s;" % (tourn_id,))
    conn.commit()
    # Delete the Tournament table data.
    c.execute("DELETE FROM Tournament "
        "WHERE id = %s;" % (tourn_id,))
    conn.commit()
    # Drop all created views for the specified tournament.
    view_prefix = ['players_tourn_', 'games_tourn_', 'lost_games_', 'won_games_',
        'combined_standings_', 'player_standings_', 'ranked_standings_', 'swiss_pairings_']
    tourn_views = [f + str(tourn_id) for f in view_prefix]
    # If the view exists, drop it, if not, move on.
    for f in reversed(tourn_views): 
        try:
            c.execute("DROP VIEW %s;" % f)
            conn.commit()
        except:
            pass
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    # Truncate tournaments Game tables only, preserving player records.
    c.execute("TRUNCATE TABLE Game;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    # Truncate the Player, Tournament_player and Game tables within the database.
    c.execute("TRUNCATE TABLE Player, Game, Tournament_player;")
    conn.commit()
    conn.close()


def countPlayers(tourn_id=0):
    """Returns the number of players currently registered.

       When tourn_id=0 (default) returns number of total players registered.
       When tourn_id=x (where x is any tourn id number) returns total 
       players participating within tournament id x. 
    """
    conn = connect()
    c = conn.cursor()
    # If tourn_id is 0 (default) count all registered players.
    if tourn_id == 0:
        c.execute("SELECT count(player_id) FROM Player;")
    else:
        # Count the total players within the selected tournament.
        c.execute("SELECT count(player_id) FROM Tournament_player \
                  WHERE tournament_id = %s;" % (tourn_id,))
    count_result = c.fetchone()
    conn.commit()
    conn.close()
    return count_result[0]


def registerPlayer(name, tourn_id=1):
    """Registers a player and unique id into the players table.
       By default, if no tourn_id is specified for the input
       player, the player will be registered to tournament id 1.

    Args:
      name: The players full name (no need to be unique)
      tourn_id: The tournament ID the player is to join (default 1)
    """
    conn = connect()
    c = conn.cursor()
    # return the default supplied player_id created using RETURNING clause.
    query = "INSERT INTO Player (name) VALUES (%s) RETURNING player_id;"
    c.execute(query, (name,))
    player_id = c.fetchone()[0]  
    conn.commit()
    # Using the retrieved playing_id, insert into the Tournament_player table.
    tournamentPlayer(player_id, tourn_id)
    conn.commit()
    conn.close()


def tournamentPlayer(player_id, tourn_id):
    """Adds an existing registered player to a different tournament 
       by matching the associated player_id to a tournament_id.

    Args:
      player_id: The players associated player_id
      tourn_id: The tournaments associated tournament_id
    """
    conn = connect()
    c = conn.cursor()
    query = "INSERT INTO Tournament_player (player_id, tournament_id) VALUES (%s, %s);"
    c.execute(query, (player_id, tourn_id))
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
    # Fetch standings for the selected tournament from the standings view.
    c.execute("SELECT * FROM player_standings_%s;" % tourn_id)
    performance_table = c.fetchall()
    conn.commit()
    conn.close()
    return performance_table


def reportMatch(winner, loser, tourn_id=1):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    # Insert the match results into the Game table under the approriate tourn id. 
    query = "INSERT INTO Game (win_ref, loose_ref, tournament_id) VALUES (%s, %s, %s);"
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
    # Use the generated swiss_pairings view for the selected tournament.
    c.execute("SELECT * FROM swiss_pairings_%s;" % tourn_id) 
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result
