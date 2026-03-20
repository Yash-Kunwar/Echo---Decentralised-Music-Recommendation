# Echo: Decentralized Music Discovery & Export Engine

![Echo Header Image](https://raw.githubusercontent.com/yashk/echo/main/assets/header.png)

## 1. The Problem: Centralized Music Ecosystems
Digital music is currently a "walled garden." Platforms like Spotify and Apple Music centralize discovery algorithms and API access to enforce user lock-in.

* **Monolithic Control:** Discovery is dictated by proprietary black-box algorithms.
* **Paywalled Automation:** Exporting playlists via official APIs often requires $99/year developer fees (Apple) or restricted "Development Mode" quotas (Spotify).
* **Data Silos:** Metadata is proprietary and often inconsistent across platforms.

**Echo** decentralizes this process. It orchestrates recommendations using open-source community data, bypassing proprietary paywalls through precise ISRC fingerprinting and client-side automation.

---

## 2. Technical Profile
**Echo (Music Recommendation)** (Python, REST API, OAuth 2.0, Feature Engineering)
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
