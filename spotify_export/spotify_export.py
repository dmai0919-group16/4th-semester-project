import csv
import Levenshtein
import spotify_export.spotify_helper as spotify_helper


def add_songs_to_playlist(csv_filename, oauth_object, playlist_id, max_results_per_song=5):
    """ """
    list_of_songs = []
    spotify_object = spotify_helper.get_spotify_object(oauth_object)

    with open(csv_filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for line in reader:
            if line['Title'] is not None:

                song_title = line['Title']
                song_artist = ''
                featuring_artist = ''

                #####################################################
                # Clear the artist input from the featuring artists #
                #####################################################
                if ' feat.' in line['Artist']:
                    song_artist_raw = line['Artist']
                    song_artist = song_artist_raw[0:song_artist_raw.lower().find('feat.')]
                    featuring_artist = song_artist_raw[song_artist_raw.find(' feat.')+7:-1]
                elif ' X ' in line['Artist']:
                    song_artist_raw = line['Artist']
                    song_artist = song_artist_raw[0:song_artist_raw.lower().find(' x ')]
                    featuring_artist_raw = song_artist_raw[song_artist_raw.find(' X ') +3:-1]
                    if ' X ' in featuring_artist_raw:
                        featuring_artist = featuring_artist_raw[ 0 : featuring_artist_raw.find(' X ')]
                elif ' & ' in line['Artist']:
                    song_artist_raw = line['Artist']
                    song_artist = song_artist_raw[0:song_artist_raw.lower().find(' & ')]
                    featuring_artist_raw = song_artist_raw[song_artist_raw.find(' & ') +3:-1]
                    if ' & ' in featuring_artist_raw:
                        featuring_artist = featuring_artist_raw[ 0 : featuring_artist_raw.find(' & ')]
                elif ' / ' in line['Artist']:
                    song_artist_raw = line['Artist']
                    song_artist = song_artist_raw[0:song_artist_raw.lower().find(' / ')]
                    featuring_artist_raw = song_artist_raw[song_artist_raw.find(' / ') +3:-1]
                    if ' / ' in featuring_artist_raw:
                        featuring_artist = featuring_artist_raw[ 0 : featuring_artist_raw.find(' / ')]
                else: song_artist = line['Artist']

                found = False
                print(song_title)
                print(song_artist)

                result = spotify_object.search(q=song_title, limit=max_results_per_song)

                #####################################################
                # Search for the song with different configurations #
                #####################################################
                for item in result['tracks']['items']:
                    print(item['artists'][0]['name'])
                    print(song_artist.lower())
                    if Levenshtein.distance(item['artists'][0]['name'].lower(),song_artist.lower())<=4:
                        list_of_songs.append(item['uri'])
                        found = True
                    if found:
                        break

                if found == False:
                    result = spotify_object.search(q=song_title + ' ' + song_artist, limit=max_results_per_song)
                    for item in result['tracks']['items']:
                        print(item['artists'][0]['name'])
                        print(song_artist.lower())
                        if Levenshtein.distance(item['artists'][0]['name'].lower(),song_artist.lower())<=5:
                            list_of_songs.append(item['uri'])
                            found = True
                        if found:
                            break

                if found == False:
                    result = spotify_object.search(q=song_artist + ' ' + song_title, limit=max_results_per_song)
                    for item in result['tracks']['items']:
                        print(item['artists'][0]['name'])
                        print(song_artist.lower())
                        if Levenshtein.distance(item['artists'][0]['name'].lower(),song_artist.lower())<=8:
                            list_of_songs.append(item['uri'])
                            found = True
                        if found:
                            break


    user_id = spotify_object.me()['id']

    print(user_id, playlist_id, list_of_songs)

    spotify_object.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=list_of_songs)
    
def add_songs_to_new_playlist(csv_filename, oauth_object, playlist_name, max_results_per_song=5):
    spotify_object = spotify_helper.get_spotify_object(oauth_object)


    playlist = spotify_object.user_playlist_create(spotify_object.me()['id'], playlist_name)
    playlist_id = playlist['id']

    add_songs_to_playlist(csv_filename, oauth_object, playlist_id, max_results_per_song)

    return playlist_id
