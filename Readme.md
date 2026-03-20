# Echo: Decentralized Music Discovery & Export Engine

---

![Echo Header](https://github.com/user-attachments/assets/65a72a1d-1023-49f1-9cea-cebb0c122d18)

---

## 1. The Problem: Centralized Music Ecosystems
Digital music is currently a "walled garden." Platforms like Spotify and Apple Music centralize discovery algorithms and API access to enforce user lock-in.

* **Monolithic Control:** Discovery is dictated by proprietary black-box algorithms.
* **Paywalled Automation:** Exporting playlists via official APIs often requires $99/year developer fees (Apple) or restricted "Development Mode" quotas (Spotify).
* **Data Silos:** Metadata is proprietary and often inconsistent across platforms.

**Echo** decentralizes this process. It orchestrates recommendations using open-source community data, bypassing proprietary paywalls through precise ISRC fingerprinting and client-side automation.

---

## 2. Technical Profile
*A decentralized music recommendation system leveraging open-source metadata and algorithmic scoring to automate cross-platform playlist generation without proprietary API licensing costs.*

* **Engine Architecture:** Synchronizes Last.fm metadata and MusicBrainz ISRC resolution via a weighted ranking algorithm.
* **Export Pipeline:** Dual-path execution via Spotify OAuth 2.0 and URL-encoded iOS Shortcut strings.
* **Performance:** Maintains <1.2s per-track resolution latency through synchronized API throttling.

---

## 3. System Architecture
Echo operates as a multi-node pipeline to ensure zero-cost operation and high metadata accuracy.

| Node | Function | Technology |
| :--- | :--- | :--- |
| **Discovery** | Collaborative Filtering | Last.fm API |
| **Identity** | ISRC Resolution | MusicBrainz API |
| **Ranking** | Feature Fusion | Weighted Heuristics |
| **Export A** | Server-Side Injection | Spotify OAuth 2.0 |
| **Export B** | Client-Side Automation | Apple Music / iOS Shortcuts |

### Feature Engineering & Scoring
The engine utilizes a custom weighted ranking formula to refine candidates:
$$Score(t) = (\alpha \cdot Sim) + (\beta \cdot Tag) + (\gamma \cdot Pop)$$
* **Log-Scaled Normalization:** Play counts are log-transformed to prevent popularity bias.
* **Hybrid Filtering:** Combines collaborative behavior (Last.fm) with attribute verification (MusicBrainz/Tags).

---

## 4. Installation & Setup

### Step 1: Clone & Install
```bash
git clone [https://github.com/yashk/echo.git](https://github.com/yashk/echo.git)
cd echo
pip install requests
```
### Step 2: Configure Credentials
```python
LASTFM_API_KEY = "your_lastfm_key"
LASTFM_SECRET = "your_lastfm_secret"
```

## 5. Usage
Run the main engine. The CLI will autonomously detect the seed track's genre before prompting for your target discovery parameters.

### Pipeline Flow:
**Input:** Enter Seed Artist & Track
**Analyze:** System derives genre tags autonomously
**Fetch:** 150+ candidates pulled from decentralized nodes
**Resolve:** ISRCs matched (Match 1-3) with 1.2s throttling
**Export:** Select Spotify (OAuth) or Apple Music (Shortcut URL)

### 6. Zero-Cost Deployment Logic
Echo avoids the $99/year Apple Developer fee by generating **Delimiter-Separated Value (DSV)** strings. These are passed via *shortcuts://run-shortcut* deep links to a local iOS Shortcut, which handles the final "Add to Library" action on the user's hardware rather than the server.


