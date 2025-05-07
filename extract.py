from dotenv import load_dotenv
import os
import base64
import json
import requests
import webbrowser
import http.server
import socketserver
import threading
from urllib.parse import urlencode
import pandas as pd
import datetime

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

SCOPE = "user-read-private user-read-email playlist-read-private user-read-recently-played"

def get_auth_code():
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "show_dialog": True
    }
    
    auth_url = f"{auth_url}?{urlencode(params)}"
    print(f"Please visit this URL to authorize the application: {auth_url}")
    webbrowser.open(auth_url)
    
    auth_code = [None]
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if 'callback' in self.path:
                auth_code[0] = self.path.split('code=')[1].split('&')[0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization successful! You can close this window.")
                threading.Thread(target=self.server.shutdown, daemon=True).start()
    
    with socketserver.TCPServer(("", 8888), Handler) as httpd:
        print("Waiting for authorization...")
        httpd.serve_forever()
    
    return auth_code[0]

def get_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    
    auth_string = CLIENT_ID + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    response_data = json.loads(response.text)
    
    return response_data["access_token"]

def get_user_profile(token):
    url = "https://api.spotify.com/v1/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    user_data = json.loads(response.text)
    
    return user_data
auth_code = get_auth_code()
    
   
TOKEN = get_token(auth_code)
    
print("Access Token:", TOKEN)   
user_profile = get_user_profile(TOKEN)
user_id = user_profile["id"]


print("User ID:", user_id)
print("Access Token:", TOKEN)

def return_song_dataframe(): 
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
     
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=2)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

        
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

          
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
           
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    return song_df