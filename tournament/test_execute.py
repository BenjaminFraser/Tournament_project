import psycopg2
import tournament

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

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
    c.execute("select * from player_standings;")
    performance_results = c.fetchall()
    if len(performance_results) < 2:
        print 'The standings should contain everything!'
    #if len(performance_results) > 4:
     # print ' The list was %s results long!' % results_list
    print performance_results[0]
    conn.commit()
    conn.close()

playerStandings()