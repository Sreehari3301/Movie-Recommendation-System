import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="TMDB AI Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #415a77;
        color: white;
        border: none;
    }
    .movie-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #334155;
        transition: transform 0.3s ease;
        height: 100%;
    }
    .movie-card:hover {
        transform: scale(1.05);
        border-color: #6366f1;
    }
    .feature-tag {
        display: inline-block;
        padding: 4px 12px;
        background: #312e81;
        border-radius: 20px;
        font-size: 0.8em;
        margin: 4px;
    }
    h1, h2, h3 {
        color: #e2e8f0;
    }
    .stMetric {
        background: #1e293b;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Constants
TMDB_API_BASE = 'https://api.themoviedb.org/3'
TMDB_IMG_BASE = 'https://image.tmdb.org/t/p/w500'

TMDB_KEYS = [
    'fb7bb23f03b6994dafc674c074d01761','e55425032d3d0f371fc776f302e7c09b',
    '8301a21598f8b45668d5711a814f01f6','8cf43ad9c085135b9479ad5cf6bbcbda',
    'da63548086e399ffc910fbc08526df05','13e53ff644a8bd4ba37b3e1044ad24f3',
    '269890f657dddf4635473cf4cf456576','a2f888b27315e62e471b2d587048f32e',
    '8476a7ab80ad76f0936744df0430e67c','5622cafbfe8f8cfe358a29c53e19bba0',
    'ae4bd1b6fce2a5648671bfc171d15ba4','257654f35e3dff105574f97fb4b97035',
    '2f4038e83265214a0dcd6ec2eb3276f5','9e43f45f94705cc8e1d5a0400d19a7b7',
    'af6887753365e14160254ac7f4345dd2','06f10fc8741a672af455421c239a1ffc',
    '09ad8ace66eec34302943272db0e8d2c'
]

IMDB_KEYS = [
    '4b447405','eb0c0475','7776cbde','ff28f90b','6c3a2d45','b07b58c8',
    'ad04b643','a95b5205','777d9323','2c2c3314','b5cff164','89a9f57d',
    '73a9858a','efbd8357'
]

import random

import time

# TMDB API Helper Class
class TMDBClient:
    def __init__(self, api_key=None):
        self.manual_key = api_key
        self.api_key = api_key if api_key else random.choice(TMDB_KEYS)
        self.base_url = TMDB_API_BASE
        self.img_url = TMDB_IMG_BASE
        self.timeout = 15

    def _safe_get(self, url, params=None):
        # If manual key is provided, use ONLY that key.
        # If no manual key, rotate through the pool.
        if self.manual_key:
            keys_to_try = [self.manual_key]
        else:
            keys_to_try = [self.api_key] + random.sample(TMDB_KEYS, 3)
        
        for key in keys_to_try:
            current_params = params.copy() if params else {}
            current_params["api_key"] = key
            try:
                time.sleep(0.1)
                response = requests.get(url, params=current_params, timeout=self.timeout)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    time.sleep(1)
                    continue
                else:
                    continue
            except:
                continue
        return None

    @st.cache_data(show_spinner="Searching TMDB...", ttl=3600)
    def search_movie(_self, query):
        url = f"{_self.base_url}/search/movie"
        data = _self._safe_get(url, {"query": query})
        return data.get('results', []) if data else []

    @st.cache_data(show_spinner="Fetching details...", ttl=3600)
    def get_details(_self, movie_id):
        url = f"{_self.base_url}/movie/{movie_id}"
        return _self._safe_get(url, {"append_to_response": "credits"}) or {}

    @st.cache_data(show_spinner="Generating recommendations...", ttl=3600)
    def get_recommendations(_self, movie_id):
        url = f"{_self.base_url}/movie/{movie_id}/recommendations"
        data = _self._safe_get(url)
        return data.get('results', []) if data else []

    @st.cache_data(show_spinner="Fetching trending...", ttl=3600)
    def get_trending(_self, media_type="movie"):
        url = f"{_self.base_url}/trending/{media_type}/week"
        data = _self._safe_get(url)
        return data.get('results', []) if data else []

    @st.cache_data(show_spinner="Fetching latest...", ttl=3600)
    def get_now_playing(_self):
        url = f"{_self.base_url}/movie/now_playing"
        data = _self._safe_get(url)
        return data.get('results', []) if data else []

# Sidebar for API Configuration
st.sidebar.title("🔐 Connection Status")

# Diagnostic Tool
try:
    with st.sidebar:
        test_res = requests.get("https://api.themoviedb.org", timeout=2)
        st.success("🟢 TMDB Reachable")
except:
    st.sidebar.error("🔴 TMDB Blocked (Use VPN)")
    st.sidebar.info("💡 **Tip:** Since your ISP blocks TMDB, please keep your VPN **ON** while searching. Once a movie is loaded, it will be saved in the app's cache.")

manual_key = st.sidebar.text_input("Manual TMDB Key (Optional)", type="password")

# Initialization logic - Ensure these exist
if "applied_key" not in st.session_state:
    st.session_state.applied_key = None # Initialize as None vs empty string to force first check

if "client" not in st.session_state or manual_key != st.session_state.applied_key:
    st.session_state.applied_key = manual_key
    st.session_state.client = TMDBClient(manual_key if manual_key else None)
    # Clear cache only if we are actually switching keys or setting a manual one
    if st.session_state.applied_key:
        st.cache_data.clear()

client = st.session_state.client

st.title("🍿 TMDB AI Recommendation Engine")

search_query = st.text_input("🔍 Search for a movie (e.g., Inception, Interstellar)", "")

if not search_query:
    st.subheader("🔥 Explore Trending & New Releases")
    
    t1, t2, t3 = st.tabs(["🎥 Trending Movies", "📺 Trending TV Shows", "🆕 New Releases"])
    
    def display_grid(items, is_tv=False):
        if not items:
            st.warning("No data found. Please check your VPN.")
            return
        
        cols = st.columns(5)
        for i, item in enumerate(items[:15]):
            with cols[i % 5]:
                title = item.get('title') if not is_tv else item.get('name')
                date = item.get('release_date', 'N/A') if not is_tv else item.get('first_air_date', 'N/A')
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{client.img_url}{item.get('poster_path', '')}" style="width:100%; border-radius:10px;">
                    <p style="font-weight:bold; margin-top:10px; font-size:0.8em; height: 3em; overflow: hidden;">{title}</p>
                    <p style="font-size:0.7em; color:#94a3b8;">📅 {date[:4] if date != 'N/A' else 'N/A'}</p>
                    <p style="font-size:0.8em; color:#6366f1;">⭐️ {item.get('vote_average', 0):.1f}</p>
                </div>
                """, unsafe_allow_html=True)
                st.write("") # Spacer

    with t1:
        trending_movies = client.get_trending("movie")
        display_grid(trending_movies)

    with t2:
        trending_tv = client.get_trending("tv")
        display_grid(trending_tv, is_tv=True)

    with t3:
        new_releases = client.get_now_playing()
        display_grid(new_releases)

else:
    search_results = client.search_movie(search_query)
    
    if not search_results:
        st.warning("No movies found. Try another search.")
    else:
        # Dropdown for specific movie selection
        movie_options = {res['title'] + " (" + res.get('release_date', 'N/A')[:4] + ")": res['id'] for res in search_results}
        selected_display = st.selectbox("Select the exact movie:", list(movie_options.keys()))
        movie_id = movie_options[selected_display]
        
        if movie_id:
            details = client.get_details(movie_id)
            recs = client.get_recommendations(movie_id)
            
            # Layout for details
            col_post, col_info = st.columns([1, 2])
            
            with col_post:
                if details.get('poster_path'):
                    st.image(f"{client.img_url}{details['poster_path']}")
                else:
                    st.write("No image available")
            
            with col_info:
                st.header(details['title'])
                st.write(f"*{details.get('tagline', '')}*")
                st.write(details.get('overview', ''))
                
                st.divider()
                
                # Features Grid
                f1, f2, f3 = st.columns(3)
                f1.metric("Rating", f"{details.get('vote_average', 0):.1f}/10")
                f2.metric("Release", details.get('release_date', 'N/A')[:4])
                f3.metric("Runtime", f"{details.get('runtime', 0)} min")
                
                st.write("**Genres:** " + ", ".join([g['name'] for g in details.get('genres', [])]))
                
                # Financial Stats
                st.write("**Financials:**")
                col_b, col_r = st.columns(2)
                col_b.write(f"💰 Budget: ${details.get('budget', 0):,}")
                col_r.write(f"💵 Revenue: ${details.get('revenue', 0):,}")
            
            st.divider()
            
            # Recommendations Section
            st.subheader("🎭 Recommended for You")
            if not recs:
                st.write("No recommendations found for this movie.")
            else:
                rec_cols = st.columns(5)
                for i, movie in enumerate(recs[:10]):
                    with rec_cols[i % 5]:
                        st.markdown(f"""
                        <div class="movie-card">
                            <img src="{client.img_url}{movie.get('poster_path', '')}" style="width:100%; border-radius:10px;">
                            <p style="font-weight:bold; margin-top:10px; font-size:0.9em;">{movie['title']}</p>
                            <p style="font-size:0.7em; color:#94a3b8;">📅 {movie.get('release_date', 'N/A')[:4]}</p>
                            <p style="font-size:0.8em; color:#6366f1;">⭐️ {movie.get('vote_average', 0):.1f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("") # Spacer

st.divider()
st.caption("Powered by The Movie Database (TMDB) API | Built with Streamlit")
