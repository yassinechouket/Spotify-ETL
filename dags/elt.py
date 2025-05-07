from dotenv import load_dotenv
import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN = os.getenv("TOKEN")

def return_song_dataframe():
    if not TOKEN:
        raise Exception("TOKEN is missing. Please set it in your .env file.")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    two_weeks_ago = datetime.now() - timedelta(days=14)
    unix_timestamp = int(two_weeks_ago.timestamp()) * 1000

    response = requests.get(
        f"https://api.spotify.com/v1/me/player/recently-played?after={unix_timestamp}",
        headers=headers
    )
    
    data = response.json()

    if "items" not in data:
        print("No recent tracks found or token expired.")
        return pd.DataFrame()

    songs = []
    for song in data["items"]:
        songs.append({
            "song_name": song["track"]["name"],
            "artist_name": song["track"]["album"]["artists"][0]["name"],
            "played_at": song["played_at"],
            "timestamp": song["played_at"][:10]
        })
    print(pd.DataFrame(songs))  
    return pd.DataFrame(songs)

def transform_song_dataframe(df):
    if df.empty:
        print("No songs to transform.")
        return pd.DataFrame()

    df['played_at'] = pd.to_datetime(df['played_at'], format="%Y-%m-%dT%H:%M:%S.%fZ")
    df['hour'] = df['played_at'].dt.hour
    df['time'] = df['played_at'].dt.strftime("%H:%M:%S")
    df.dropna(inplace=True)

    if df[['song_name', 'played_at']].drop_duplicates().shape[0] != df.shape[0]:
        raise Exception("Primary Key Exception: Duplicate records found.")

    df = df.merge(df.groupby('artist_name').size().reset_index(name='favorite_artist'), on='artist_name')
    df = df.merge(df.groupby('song_name').size().reset_index(name='favorite_song'), on='song_name')
    df = df.merge(df.groupby('hour').size().reset_index(name='daily_listening'), on='hour')

    return df[['song_name', 'artist_name', 'time', 'timestamp', 'favorite_song', 'favorite_artist', 'daily_listening']]

def spotify_etl():
    df = return_song_dataframe()
    transformed_df = transform_song_dataframe(df)
    print(transformed_df)
    return transformed_df


spotify_etl()