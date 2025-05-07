import extract
import pandas as pd
from datetime import datetime

def transform_song_dataframe(df):
    if df.empty:
        print('No Songs Extracted')
        return pd.DataFrame()


    df2 = df.copy()

    
    df2['played_at'] = pd.to_datetime(df2['played_at'], format="%Y-%m-%dT%H:%M:%S.%fZ")

    
    df2['hour'] = df2['played_at'].dt.hour
    df2['time'] = df2['played_at'].dt.strftime("%H:%M:%S")

    
    df2.dropna(inplace=True)

    
    if not df2[['song_name', 'played_at']].drop_duplicates().shape[0] == df2.shape[0]:
        raise Exception("Primary Key Exception: Duplicate records detected.")

    
    artist_counts = df2.groupby('artist_name').size().reset_index(name='Favorite Artist')
    df2 = df2.merge(artist_counts, on='artist_name', how='left')

    
    song_counts = df2.groupby('song_name').size().reset_index(name='Favorite Song')
    df2 = df2.merge(song_counts, on='song_name', how='left')

    
    hour_counts = df2.groupby('hour').size().reset_index(name='Daily Listening')
    df2 = df2.merge(hour_counts, on='hour', how='left')

    
    df2 = df2[['song_name', 'artist_name', 'time', 'timestamp', 'Favorite Song', 'Favorite Artist', 'Daily Listening']]

    return df2



if __name__ == "__main__":
     
    
    df=extract.return_song_dataframe()
    
    Transformed_df=transform_song_dataframe(df)    
    print(Transformed_df)