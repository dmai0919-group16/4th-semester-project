from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import webbrowser
import spotipy
import spotify_export.spotify_helper as spotify_helper
import spotify_export.spotify_export as export

songs_file = 'New_Music_in_My_Danish_stations.csv'

cache_file = 'spotify_cache'
creds_file = 'apiKeys.json'
server_host = 'localhost'
server_port = 8081 


response_path = None

class StoppableHttpServer (HTTPServer):
    def serve_forever (self):
        self.stop = False
        while not self.stop:
            self.handle_request()

class DummyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global response_path
        path = self.path

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("%s" % path, "utf-8"))

        if('?code=' in path):
            response_path = path
            self.server.stop = True


if __name__ == '__main__':
    client_id, client_secret = None, None

    ######################################
    # Read Spotify client keys from json #
    ######################################
    if os.path.exists(creds_file):
        with open(creds_file) as json_file:
            data = json.load(json_file)
            client_id, client_secret = data['clientId'], data['clientSecret']
    else:
        print('[!] API key file \'%s\' doesn\'t exist. Aborting...' % creds_file)
        exit(-1)

    ####################################################
    # Authenticate user to our Spotify cient via OAuth #
    ####################################################

    # Cache file belongs to a single user. Multiple users call for another caching solution
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_file) 
    oauth_object = spotify_helper.get_spotify_oauth(
        scope='playlist-modify-public',
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://%s:%i' % (server_host, server_port),
        cache_handler=cache_handler
    )

    auth_url = spotify_helper.authenticate_user_get_url(oauth_object)
    print('[*] Opening user authentication URL \'%s\'...' % auth_url)
    webbrowser.open(auth_url)

    ################################################################
    # Start dummy web-server to catch redirect URL with auth token #
    ################################################################
    print('[*] Starting web server (on %s:%i)' % (server_host, server_port))
    httpd = StoppableHttpServer((server_host, server_port), DummyRequestHandler)
    httpd.serve_forever()
    httpd.server_close()

    print('[*] Caught URL with auth token \'%s\'' % response_path)

    auth_token = spotify_helper.authenticate_user_get_token(oauth_object, response_path)
    spotify_object = spotify_helper.get_spotify_object(oauth_object)

    print(auth_token)
    print(spotify_object.current_user())
    
    export.add_songs_to_new_playlist(songs_file, oauth_object, 'lofasz')

    ############
    # Clean-up #
    ############
    if os.path.exists(cache_file):
        print('[*] Removing cache file \'%s\'' % cache_file)
        os.remove(cache_file)

