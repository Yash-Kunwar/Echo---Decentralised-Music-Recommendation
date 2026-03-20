import sys
import itertools
import config
from brain import RecommendationEngine

def main():
    print("--- Echo: decentralised music recommendation ---")
    
    # collect initial parameters
    seed_artist = input("enter artist: ").lower().strip()
    seed_track = input("enter track: ").lower().strip()

    # initialize the engine
    engine = RecommendationEngine(config.LASTFM_API_KEY)
    
    # recommended genres
    print(f"\nanalyzing '{seed_track.title()}' by {seed_artist.title()}...")
    seed_tags = engine.get_track_tags(seed_artist, seed_track)
    
    if seed_tags:
        top_genres = ", ".join(seed_tags[:5]).title()
        print(f"recommended genres: {top_genres}")
    else:
        print("can't recommend genres, too niche!!")

    target_genre = input("\npreffered genre: ").lower().strip()
    
    # fetch similar tracks
    print(f"\nfetching tracks similar to '{seed_track.title()}'...")
    raw_data = engine.get_similar_tracks(seed_artist, seed_track, limit=200) 
    
    if "similartracks" in raw_data:
        all_recs = engine.parse_results(raw_data)
        filtered_recs = []

        print(f"found {len(all_recs)} raw candidate tracks.")
        print(f"scanning for the '{target_genre}' tag and fetching ISRCs...")
        
        spinner = itertools.cycle(['|', '/', '-', '\\'])
        
        for rec in all_recs:
            sys.stdout.write(f"\r{next(spinner)} analyzing: {rec['title'][:25]:<25} ")
            sys.stdout.flush()
            
            tags = engine.get_track_tags(rec['artist'], rec['title'])
            
            if any(target_genre in tag for tag in tags):
                isrc_code = engine.get_track_isrc(rec['artist'], rec['title'])
                rec['isrc'] = isrc_code if isrc_code else "NOT_FOUND"

                final_score = engine.calculate_track_score(
                    similarity=rec['match'], 
                    tag_prominence=100.0, 
                    listen_count=50.0, 
                    alpha=0.5, 
                    beta=0.3, 
                    gamma=0.2
                )
                rec['algorithmic_score'] = final_score
                filtered_recs.append(rec)
            
            if len(filtered_recs) == 10:
                break

        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()

        # final recommendations
        if filtered_recs:
            print(f"\ntop {len(filtered_recs)} matches for genre: {target_genre.capitalize()}")
            print(f"{'#':<3} | {'Artist':<20} | {'Track':<25} | {'ISRC':<15} | {'Score'}")
            print("-" * 80)
            
            for i, rec in enumerate(filtered_recs, 1):
                artist_name = rec['artist'][:18] + ".." if len(rec['artist']) > 20 else rec['artist']
                track_name = rec['title'][:23] + ".." if len(rec['title']) > 25 else rec['title']
                print(f"{i:<3} | {artist_name:<20} | {track_name:<25} | {rec['isrc']:<15} | {rec['algorithmic_score']:.1f}")
        else:
            print(f"\nno tracks found tagged with '{target_genre}'.")
            
    elif "error" in raw_data:
        print(f"error: {raw_data['error']}")
    else:
        print("no matches found for that specific song.")

if __name__ == "__main__":
    main()