import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from dotenv import load_dotenv
import json
import time

load_dotenv()

def setup_spotify_client():
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.environ.get('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
    
    scope = "playlist-read-private"
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ))
    
    return sp

def setup_ytmusic_client():
    return YTMusic('browser.json')

def get_spotify_playlist_tracks(sp, playlist_url):
    if 'playlist/' in playlist_url:
        playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
    else:
        playlist_id = playlist_url
    
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    playlist_info = sp.playlist(playlist_id)
    playlist_name = playlist_info['name']
    
    return tracks, playlist_name

def search_track_on_ytmusic(ytmusic, track_info):
    track_name = track_info['track']['name']
    artists = [artist['name'] for artist in track_info['track']['artists']]
    artist_name = artists[0]  
    
    search_query = f"{track_name} {artist_name}"
    
    search_results = ytmusic.search(search_query, filter="songs")
    
    if search_results:
        print(f'Track found : {json.dumps(search_results[0])}')
        return search_results[0]['videoId']
    return None

def create_ytmusic_playlist(ytmusic, playlist_name, video_ids, spotify_playlist_url=None):
    description = f"Converted from Spotify playlist: {spotify_playlist_url}" if spotify_playlist_url else "Converted from Spotify"
    
    playlist_id = ytmusic.create_playlist(
        title=f"{playlist_name} (from Spotify)",
        description=description,
        privacy_status="PRIVATE"
    )
    
    for video_id in video_ids:
        try:
            result = ytmusic.add_playlist_items(
                playlistId=playlist_id,
                videoIds=[video_id],
                duplicates=False  
            )
            print(f"Added track with video ID: {video_id}")
            time.sleep(0.5) 
        except Exception as e:
            print(f"Failed to add video {video_id}: {e}")
    
    return playlist_id

def convert_playlist(spotify_playlist_url):
    try:
        sp = setup_spotify_client()
        ytmusic = setup_ytmusic_client()
        spotify_tracks, playlist_name = get_spotify_playlist_tracks(sp, spotify_playlist_url)
        
        
        print(json.dumps(spotify_tracks[0]))
        print(f"Found {len(spotify_tracks)} tracks in Spotify playlist: {playlist_name}")
        video_ids = []
        not_found = []
        
        for i, track_info in enumerate(spotify_tracks):
            if track_info['track'] is None:
                continue
                
            track_name = track_info['track']['name']
            artist_name = track_info['track']['artists'][0]['name']
            
            print(f"Processing {i+1}/{len(spotify_tracks)}: {track_name} by {artist_name}")
            
            video_id = search_track_on_ytmusic(ytmusic, track_info)
            
            if video_id:
                video_ids.append(video_id)
            else:
                not_found.append(f"{track_name} by {artist_name}")
    
        
        if video_ids:
            ytmusic_playlist_id = create_ytmusic_playlist(
                ytmusic, playlist_name, video_ids, spotify_playlist_url
            )
            
            print(f"\nCreated YouTube Music playlist with {len(video_ids)} tracks!")
            print(f"YouTube Music Playlist ID: {ytmusic_playlist_id}")
            
            if not_found:
                print(f"\nCouldn't find {len(not_found)} tracks on YouTube Music:")
                for track in not_found:
                    print(f"- {track}")
        else:
            print("No tracks found to add to YouTube Music playlist.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    spotify_playlist_url = input("Enter Spotify playlist URL: ")
    convert_playlist(spotify_playlist_url)