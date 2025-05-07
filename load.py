import pandas as pd
import extract
import Transform
import argparse
import psycopg2


def load(transformed_df):
    try:
        
        conn = psycopg2.connect(
            host="localhost",
            database="Spotify",
            user="postgres",
            password="yes_it_is",
            port="5432"
        )
        cursor = conn.cursor()
        
        create_sql = """
        CREATE TABLE IF NOT EXISTS Spotify_Tracks(
            song_name VARCHAR(255) NOT NULL,
            artist_name VARCHAR(255) NOT NULL,
            time VARCHAR(255) NOT NULL,
            timestamp VARCHAR(255) NOT NULL,
            "Favorite Song" INT NOT NULL,
            "Favorite Artist" INT NOT NULL,
            "Daily Listening" INT NOT NULL
        );
        """
        
        cursor.execute(create_sql)
        
       
        for index, row in transformed_df.iterrows():
            
            insert_sql = """
            INSERT INTO Spotify_Tracks(song_name, artist_name, time, timestamp, "Favorite Song", "Favorite Artist", "Daily Listening")
            VALUES(%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_sql, (
                row['song_name'], 
                row['artist_name'], 
                row['time'], 
                row['timestamp'], 
                row['Favorite Song'], 
                row['Favorite Artist'], 
                row['Daily Listening']
            ))
        
        conn.commit()
        print(" Data loaded successfully into PostgreSQL database.")

    except Exception as e:
        print(f"Error during database load: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
            print("🔒 PostgreSQL connection closed.")


if __name__ == "__main__":
    print("Extracting data...")
    raw_df = extract.return_song_dataframe()
    
    print("Transforming data...")
    transformed_df = Transform.transform_song_dataframe(raw_df)
    
    print("Loading data into database...")
    load(transformed_df)