# 🎬 Movie Recommendation System

A powerful, real-time movie and TV show discovery platform powered by the **The Movie Database (TMDB) API**. This application offers personalized recommendations, trending insights, and deep metadata analysis in a sleek, modern dashboard.

## 🚀 Key Features

- **🏠 Discovery Hub**: Instantly view Trending Movies, Trending TV Shows, and New Releases.
- **🔍 Smart Search**: Real-time search across millions of titles with instant results.
- **🤖 AI Recommendations**: Fetches similar content based on TMDB’s advanced collaborative filtering patterns.
- **📊 Rich Metadata**: 
    - Full detailed overviews and taglines.
    - Financial performance (Budget vs. Revenue).
    - Ratings, Runtimes, and Release dates.
    - High-quality Poster gallery.
- **🛡️ Intelligent API Management**:
    - **Smart Key Rotation**: Automatically cycles through a pool of 15+ API keys to prevent rate limiting.
    - **Manual Key Support**: Option to input your own API key for personal use.
    - **Deep Caching**: Efficient data storage to minimize network calls and speed up browsing.
- **🔌 Network Diagnostics**: Built-in connectivity checker to help troubleshoot ISP-level blocks (recommends VPN usage when needed).

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd project
```

### 2. Install dependencies
Ensure you have Python 3.8+ installed.
```bash
pip install streamlit requests pandas
```

### 3. Run the application
```bash
streamlit run tmdb_app.py
```

## 🔐 API Configuration

The app comes pre-loaded with a rotating pool of TMDB API keys for convenience. However, you can also manually enter your own key in the sidebar:
1.  Sign up at [The Movie Database (TMDB)](https://www.themoviedb.org/).
2.  Navigate to **Settings > API**.
3.  Generate your free API Key and paste it into the **"Manual TMDB Key"** field in the app.

## 🌐 Network Troubleshooting

If your ISP blocks TMDB (often seen as a "Connection Timeout" error):
- **VPN**: Keep your VPN **ON** for the best experience.
- **Cache**: The app caches viewed movies for 1 hour, allowing you to browse previously loaded content even after turning the VPN off.
- **Diagnostic**: Check the **"Connection Status"** in the sidebar to verify if TMDB is reachable from your network.

## 📂 Project Structure

- `tmdb_app.py`: The main entry point (Streamlit application).
- `recommend_engine.py`: Standalone Python logic for local matrix factorization (legacy mode).
- `rec_app.py`: Interactive Decision Tree classifier (Data Science demo).
- `README.md`: This documentation.

## 📼 Legacy Recommendation System (Offline)

If you want to run the offline version that uses the MovieLens dataset:

### 1. Run the Logic Engine
To see recommendations in your terminal:
```bash
python recommend_engine.py
```

### 2. Run the Legacy App
To open the local dashboard on a different port:
```bash
streamlit run rec_app.py --server.port 8502
```
♻️You can use different ports like 8503, 8504, 8505 etc.
---
