import requests
import time

class RecommendationEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://ws.audioscrobbler.com/2.0/"

    def get_similar_tracks(self, artist, track, limit=10):
        # API Parameters
        params = {
            "method": "track.getSimilar",
            "artist": artist,
            "track": track,
            "api_key": self.api_key,
            "format": "json",
            "limit": limit
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status() # Check for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def parse_results(self, data):
        if not data or 'similartracks' not in data:
            return []

        tracks = data['similartracks']['track']
        cleaned_list = []

        for t in tracks:
            # take the name, artist, and match percentage (0.0 to 1.0)
            refined_track = {
                "title": t['name'],
                "artist": t['artist']['name'],
                "match": float(t['match']) * 100  # Convert to percentage
            }
            cleaned_list.append(refined_track)
        
        return cleaned_list
    
    def get_track_tags(self, artist, track):
        """Fetches the top tags (genres) for a given track to use for filtering."""
        params = {
            "method": "track.getTopTags",
            "artist": artist,
            "track": track,
            "api_key": self.api_key,
            "format": "json"
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Safely parse the tags out of the JSON response
            if 'toptags' in data and 'tag' in data['toptags']:
                tags = data['toptags']['tag']
                # Extract the tag names, convert to lowercase for easy matching
                return [tag['name'].lower() for tag in tags]
            return []

        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not fetch tags for {track} by {artist}")
            return []
        
    def get_track_isrc(self, artist, track):
        """
        Queries MusicBrainz and checks the top 3 matching recordings.
        Often the #1 search result is a compilation missing an ISRC,
        while the #2 or #3 result is the official studio release that has it.
        """
        search_url = "https://musicbrainz.org/ws/2/recording"
        
        safe_track = track.replace('"', '').replace("'", "")
        safe_artist = artist.replace('"', '').replace("'", "")
        
        # pulling the top 3 results now to give us backup options
        search_params = {
            "query": f'recording:({safe_track}) AND artist:({safe_artist})',
            "fmt": "json",
            "limit": 3
        }
        
        headers = {
            "User-Agent": "EchoRecommendationProject/1.0 ( student@localhost.com )"
        }

        try:
            import time
            time.sleep(1.2) # Rate limit for the initial search
            
            search_res = requests.get(search_url, params=search_params, headers=headers)
            search_res.raise_for_status()
            search_data = search_res.json()

            if "recordings" in search_data and len(search_data["recordings"]) > 0:
                # Loop through the top 3 recordings instead of giving up after the first one
                for idx, recording in enumerate(search_data["recordings"]):
                    mbid = recording["id"]
                    
                    time.sleep(1.2) # Rate limit for each specific lookup
                    
                    lookup_url = f"https://musicbrainz.org/ws/2/recording/{mbid}"
                    lookup_params = {"inc": "isrcs", "fmt": "json"}
                    
                    lookup_res = requests.get(lookup_url, params=lookup_params, headers=headers)
                    
                    if lookup_res.status_code == 200:
                        lookup_data = lookup_res.json()
                        # If we find an ISRC, return it immediately and break the loop!
                        if "isrcs" in lookup_data and len(lookup_data["isrcs"]) > 0:
                            return lookup_data["isrcs"][0]
                        # else:
                        #     print(f"[Debug] Match #{idx+1} for '{track}' had no ISRC. Checking next...")
                    
                # If we check all 3 and STILL find nothing:
                # print(f"[Debug] Exhausted top {len(search_data['recordings'])} matches for '{track}', no ISRCs found.")
                return "NOT_FOUND"
            else:
                return "NOT_FOUND"

        except Exception as e:
            # print(f"\n[Debug] Connection/HTTP Error for '{track}': {e}")
            return "NOT_FOUND"
        
    def calculate_track_score(self, similarity, tag_prominence, listen_count, alpha=0.5, beta=0.3, gamma=0.2):
        """
        Calculates the algorithmic score for a track to determine its final rank.
        Formula: Score = (α * Similarity) + (β * TagProminence) + (γ * ListenCount)
        """
        # Ensure all inputs are floats to prevent math errors
        sim_score = float(similarity)
        tag_score = float(tag_prominence)
        listen_score = float(listen_count)

        final_score = (alpha * sim_score) + (beta * tag_score) + (gamma * listen_score)
        return round(final_score, 2)