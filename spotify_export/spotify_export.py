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
            song_title = line['Title']
            song_artist = ''
            featuring_artist = ''

            #####################################################
            # Clear the artist input from the featuring artists #
            #####################################################
            song_artist_raw = line['Artist']
            feat_number = song_artist_raw.find(' feat. ')
            and_number = song_artist_raw.find(' & ')
            slash_number = song_artist_raw.find(' / ')
            x_number = song_artist_raw.lower().find(' x ')
            safety_number = 1000
            separation_list = [feat_number, and_number, slash_number, x_number, safety_number]
            method_number = separation_list.index(min(i for i in separation_list if i > 0))
            if method_number < 4:
                song_artist, featuring_artist = separation_method_switcher(method_number, song_artist_raw,
                                                                           featuring_artist)
            else:
                song_artist = separation_method_switcher(method_number, song_artist_raw, featuring_artist)

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
                if Levenshtein.distance(item['artists'][0]['name'].lower(), song_artist.lower()) <= 3:
                    list_of_songs.append(item['uri'])
                    found = True
                if found:
                    break

            if found == False:
                result = spotify_object.search(q=song_title + ' ' + song_artist, limit=max_results_per_song)
                for item in result['tracks']['items']:
                    print(item['artists'][0]['name'])
                    print(song_artist.lower())
                    if Levenshtein.distance(item['artists'][0]['name'].lower(), song_artist.lower()) <= 5:
                        list_of_songs.append(item['uri'])
                        found = True
                    if found:
                        break

            if found == False:
                result = spotify_object.search(q=song_artist + ' ' + song_title, limit=max_results_per_song)
                for item in result['tracks']['items']:
                    print(item['artists'][0]['name'])
                    print(song_artist.lower())
                    if Levenshtein.distance(item['artists'][0]['name'].lower(), song_artist.lower()) <= 7:
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


def separation_method_switcher(method_number, song_artist_raw, featuring_artist):
    switcher = {
        0: separate_featuring_artist_feat(song_artist_raw, featuring_artist),
        1: separate_featuring_artist_and(song_artist_raw, featuring_artist),
        2: separate_featuring_artist_slash(song_artist_raw, featuring_artist),
        3: separate_featuring_artist_x(song_artist_raw, featuring_artist)
    }
    return switcher.get(method_number, song_artist_raw)


def separate_featuring_artist_feat(song_artist_raw, featuring_artist):
    if ' feat. ' in song_artist_raw:
        song_artist = song_artist_raw[0:song_artist_raw.lower().find(' feat. ')]
        featuring_artist_raw = song_artist_raw[song_artist_raw.find(' feat. ') + 7:]
        if ' feat. ' in featuring_artist_raw:
            featuring_artist = featuring_artist_raw[0: featuring_artist_raw.find(' feat. ')]
        else:
            featuring_artist = featuring_artist_raw
    else:
        song_artist = song_artist_raw

    return song_artist, featuring_artist


def separate_featuring_artist_x(song_artist_raw, featuring_artist):
    if ' X ' in song_artist_raw:
        song_artist = song_artist_raw[0:song_artist_raw.lower().find(' x ')]
        featuring_artist_raw = song_artist_raw[song_artist_raw.find(' X ') + 3:]
        if ' X ' in featuring_artist_raw:
            featuring_artist = featuring_artist_raw[0: featuring_artist_raw.find(' X ')]
        else:
            featuring_artist = featuring_artist_raw
    else:
        song_artist = song_artist_raw

    return song_artist, featuring_artist


def separate_featuring_artist_and(song_artist_raw, featuring_artist):
    if ' & ' in song_artist_raw:
        song_artist = song_artist_raw[0:song_artist_raw.lower().find(' & ')]
        featuring_artist_raw = song_artist_raw[song_artist_raw.find(' & ') + 3:]
        if ' & ' in featuring_artist_raw:
            featuring_artist = featuring_artist_raw[0: featuring_artist_raw.find(' & ')]
        else:
            featuring_artist = featuring_artist_raw
    else:
        song_artist = song_artist_raw

    return song_artist, featuring_artist


def separate_featuring_artist_slash(song_artist_raw, featuring_artist):
    if ' / ' in song_artist_raw:
        song_artist = song_artist_raw[0:song_artist_raw.lower().find(' / ')]
        featuring_artist_raw = song_artist_raw[song_artist_raw.find(' / ') + 3:]
        if ' / ' in featuring_artist_raw:
            featuring_artist = featuring_artist_raw[0: featuring_artist_raw.find(' / ')]
        else:
            featuring_artist = featuring_artist_raw
    else:
        song_artist = song_artist_raw

    return song_artist, featuring_artist
