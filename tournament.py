
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
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM players")
    no_of_players =cursor.fetchone()[0]
    db.commit()
    db.close()
    return no_of_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Players (name) VALUES (%s)",(name,))
    db.commit()
    db.close()

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
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM standings ")
    results = cursor.fetchall()
    db.commit()
    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO matches (winner,loser) VALUES (%s,%s)",(winner,loser,))
    db.commit()
    db.close()
 
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
    pairs = []
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT player_id, name,no_of_wins FROM standings ORDER BY no_of_wins DESC;")   
    list_of_players = cursor.fetchall()
    size = len(list_of_players)
    for i in range (0, size,2):
        id1   = list_of_players[i][0]
        name1 = list_of_players[i][1]
        id2   = list_of_players[i+1][0]
        name2 = list_of_players[i+1][1]
        pairs.append([id1, name1, id2, name2])
    return pairs
	
	
 	