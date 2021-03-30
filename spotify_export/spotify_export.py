import csv

import spotify_export.spotify_helper as spotify_helper


def add_songs_to_playlist(csv_filename, oauth_object, playlist_id, max_results_per_song=5):
    """ """
    list_of_songs = []
    spotify_object = spotify_helper.get_spotify_object(oauth_object)

    with open(csv_filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for line in reader:
            song_input = line['Title']
            song_artist = line['Artist']
            found = False

            result = spotify_object.search(q=song_input, limit=max_results_per_song)

            for item in result['tracks']['items']:
                if item['artists'][0]['name'] == song_artist:
                    list_of_songs.append(item['uri'])
                    found = True
                if found:
                    break

            if found == False:
                result = spotify_object.search(q=song_input + ' ' + song_artist, limit=max_results_per_song)
                for item in result['tracks']['items']:
                    if item['artists'][0]['name'] == song_artist:
                        list_of_songs.append(
                            item['uri'])
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
