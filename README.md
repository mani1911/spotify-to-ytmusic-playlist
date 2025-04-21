## Convert Spotify to YT Music playlist
This project is for converting any spotify playlist to YT music playlist using URL of the playlist

### Usage
1. Create a virtual environment and activate it (optional but recommended).

2. Install requirements
    ```
    pip install -r requirements.txt
    ```

3. Create an application at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

4. Get your Client ID and Client Secret.

5. Create a .env file and paste your client ID and secret in it.
    ```
    cp .env.example .env
    ```

6. Set a redirect URI as http://localhost:8888/callback
(Spotipy library automatically starts a temporary web server on your computer at this address to receive the authentication response from Spotify).

7. Run script.py with headers filled accordingly

    ```python3 script.py```

    Refer [here](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html#manual-file-creation) on how to get the headers accordingly for your browser.

8. Running the above script will create a __browser.json__ file in your root directory.

9. Now that you are good to go run the script using
    ```python3 main.py``` 
    and paste your Spotify playlist URL when prompted.





