"""
Spotify Logger Application

Logs into spotify using the web api and a user token, and logs all playback activity to a database file.
"""

import sys
import time

import pprint

# install from requirements.txt
import spotipy
import spotipy.util
import sqlite3

# print(f'using spotipy version {spotipy.VERSION}')

if len(sys.argv) > 2:
    username = sys.argv[1]
    db_path = sys.argv[2]
else:
    print("Usage: %s username db_path" % (sys.argv[0],))
    sys.exit()

# read access to a user's "your music" library
# access to a user's top artist and tracks
# read playback state
# read currently playing track
# read recently played items
scopes = 'user-library-read, user-top-read, user-read-playback-state, user-read-currently-playing, user-read-recently-played'

# have the following environment variables set

# SPOTIPY_CLIENT_ID
# SPOTIPY_CLIENT_SECRET

# for this, just going to redirect back to localhost since it's not going to any app or anything

user_token = spotipy.util.prompt_for_user_token(username, scopes, redirect_uri='http://localhost/')

# log into the spotify web api now
sp = spotipy.Spotify(auth=user_token)
# debug
# sp.trace = True
# sp.trace_out = True

# create tables if they don't exist already
db = sqlite3.connect(db_path)

# playback table - store information about user playback
# including other tidbits of information that may be useful
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS playback
    (
    timestamp UNSIGNED BIG INT,
    
    device_id TEXT,
    device_name TEXT,
    device_type TEXT,
    device_volume_percent INT,
    
    track_id TEXT
    
    )""")


# track details table - store information about track details and also track object info
c.execute("""CREATE TABLE IF NOT EXISTS track_details
    (
    track_id TEXT,
    
    popularity INT,
    name TEXT,
    explicit BOOLEAN,
    
    acousticness REAL,
    danceability REAL,
    duration_ms UNSIGNED BIG INT,
    energy REAL,
    instrumentalness REAL,
    key INT,
    liveness REAL,
    loudness REAL, 
    mode INT,
    speechiness REAL,
    tempo REAL,
    time_signature INT,
    valence REAL
    )""")

# commit the changes when done
db.commit()

while True:
    # poll the api with details about user playback
    current = sp.current_playback()

    print('polling current_playback')
    # print('current: ')
    # pprint.pprint(current)

    if current['is_playing']:
        # check to see if the current played song matches the most recently inserted one into the table
        # if not, then count this as a new play of the song
        # could do checking to see how long the song is being played, but for now will do a dumb insert

        # the timestamp will only change when the playback state changes (user plays, pauses, etc)
        timestamp = current['timestamp']
        # the item id of what's playing
        item_id = current['item']['id']

        print(f'item_id {item_id}')

        playback_obj = (timestamp,
                        current['device']['id'],
                        current['device']['name'],
                        current['device']['type'],
                        current['device']['volume_percent'],
                        item_id)

        # get the last inserted object
        c = db.cursor()
        c.execute('SELECT track_id FROM playback ORDER BY timestamp DESC')
        last_played = c.fetchone()

        if last_played is not None and last_played[0] == item_id:
            print('already played')
            # pass
        else:
            print('logging playback obj')
            # not already played, so log the playback_obj
            c.execute("""INSERT INTO playback VALUES (?,?,?,?,?,?)""", playback_obj)
            # commit to the db
            db.commit()

        # check if this track exists in the details db
        # check first to avoid going back and forth to the api to get the track details

        c = db.cursor()
        c.execute('SELECT * FROM track_details WHERE track_id=?', (item_id, ))
        data = c.fetchone()
        if data is None:
            print('inserted new row into track details')
            # doesn't exist in the table, so hit the details api to get track details
            features = sp.audio_features(item_id)[0]

            # print('features')
            # pprint.pprint(features)

            # make a track details obj
            track_obj = (
                item_id,
                current['item']['popularity'],
                current['item']['name'],
                current['item']['explicit'],
                features['acousticness'],
                features['danceability'],
                features['duration_ms'],
                features['energy'],
                features['instrumentalness'],
                features['key'],
                features['liveness'],
                features['loudness'],
                features['mode'],
                features['speechiness'],
                features['tempo'],
                features['time_signature'],
                features['valence'],
            )

            # print(track_obj)

            c.execute("""INSERT INTO track_details 
             (track_id, popularity, name, explicit, acousticness, danceability, duration_ms, energy,
             instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence)
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", track_obj)
            db.commit()
        else:
            print('did not insert track details')
    # only update every 5s or so
    time.sleep(1)

#
#
# # while True:
#
# # check for the playing status
# # current = sp.current_user_playing_track()
# current = sp.current_playback()
# pprint.pprint(current)
#
# # only eval if the user is playing
# if current['is_playing']:
#     # get the track info by uri
#     track_uri = current['item']['uri']
#
#     print('current track info: ')
#
#     track = sp.track(track_uri)
#     pprint.pprint(track)
#
#     print('audio features: ')
#
#     features = sp.audio_features(track_uri)
#     pprint.pprint(features)
#
#
# #    pprint.pprint(current)
#
# time.sleep(1)
