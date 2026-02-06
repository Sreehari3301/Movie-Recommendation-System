import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
import os

# Page Config
st.set_page_config(page_title="Movie Matcher AI", page_icon="🎬", layout="wide")

# Custom Styling
st.markdown("""
<style>
    .reportview-container { background: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .movie-card { padding: 15px; background: white; border-radius: 10px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_and_train():
    DATA_DIR = "ml-latest-small"
    movies = pd.read_csv(os.path.join(DATA_DIR, "movies.csv"))
    ratings = pd.read_csv(os.path.join(DATA_DIR, "ratings.csv"))
    
    # Preprocessing
    user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    
    # SVD
    svd = TruncatedSVD(n_components=12, random_state=42)
    item_topic_matrix = svd.fit_transform(user_item_matrix.T)
    corr_matrix = np.corrcoef(item_topic_matrix)
    
    return movies, user_item_matrix, corr_matrix

# Sidebar
st.sidebar.title("🎬 Movie Matcher")
st.sidebar.info("Using Collaborative Filtering & Matrix Factorization (SVD) to find your next favorite movie.")

# Load Data
movies, uim, corr = load_and_train()

# App Body
st.title("🍿Movie Recommendation System")
st.write("Enter a movie you love, and we'll find similar titles based on user viewing patterns.")

# Search components
movie_list = movies['title'].values
search_term = st.selectbox("Search for a movie:", [""] + list(movie_list))

if search_term:
    col1, col2 = st.columns([1, 2])
    
    # Get metadata for selected movie
    movie_info = movies[movies['title'] == search_term].iloc[0]
    
    with col1:
        st.subheader("Selected Movie")
        st.markdown(f"**Title:** {movie_info['title']}")
        st.markdown(f"**Genres:** {movie_info['genres']}")
        
    with col2:
        st.subheader("Top 10 Recommendations")
        
        # Calculate Recommendations
        movie_id = movie_info['movieId']
        try:
            movie_col_idx = uim.columns.get_loc(movie_id)
            similarities = corr[movie_col_idx]
            top_indices = np.argsort(similarities)[-11:-1][::-1]
            
            for i in top_indices:
                mid = uim.columns[i]
                rec_title = movies[movies['movieId'] == mid]['title'].values[0]
                rec_genres = movies[movies['movieId'] == mid]['genres'].values[0]
                rec_score = similarities[i]
                
                with st.container():
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4 style="margin:0;">{rec_title}</h4>
                        <p style="color:#666; font-size:0.8em; margin:5px 0;">{rec_genres}</p>
                        <progress value="{rec_score}" max="1" style="width:100%"></progress>
                        <small>Similarity Score: {rec_score:.2f}</small>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating recommendations: {e}")

else:
    # Landing Page Visuals
    st.info("Please select a movie from the dropdown to start.")
    
    # Show some popular movies
    st.subheader("Discover New Titles")
    cols = st.columns(4)
    sample_movies = movies.sample(4)
    for i, (_, m) in enumerate(sample_movies.iterrows()):
        cols[i].markdown(f"**{m['title']}**\n\n_{m['genres']}_")

# Footer
st.divider()
st.caption("Algorithm: Singular Value Decomposition (SVD) | Dataset: MovieLens 100k")
