import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error
import os

# Load Data
DATA_DIR = "ml-latest-small"

def load_data():
    movies = pd.read_csv(os.path.join(DATA_DIR, "movies.csv"))
    ratings = pd.read_csv(os.path.join(DATA_DIR, "ratings.csv"))
    return movies, ratings

def train_recommender():
    movies, ratings = load_data()
    
    # Create User-Item Matrix
    user_item_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
    
    # Apply Matrix Factorization (SVD)
    # We reduce the dimensions (latent factors)
    n_latent_factors = 12
    svd = TruncatedSVD(n_components=n_latent_factors, random_state=42)
    
    # Item-Topic Matrix (Transposed because we want to compare movies)
    item_topic_matrix = svd.fit_transform(user_item_matrix.T)
    
    # Calculate Correlation Matrix between movies based on latent factors
    corr_matrix = np.corrcoef(item_topic_matrix)
    
    return movies, user_item_matrix, item_topic_matrix, corr_matrix

def get_recommendations(movie_title, movies, corr_matrix, user_item_matrix):
    # Find movieId for title
    try:
        idx = movies[movies['title'].str.contains(movie_title, case=False)].index[0]
        movie_id = movies.iloc[idx]['movieId']
        
        # Get the internal index in the user_item_matrix columns
        movie_col_idx = user_item_matrix.columns.get_loc(movie_id)
        
        # Get correlations for this movie
        similarities = corr_matrix[movie_col_idx]
        
        # Get top 10 matches
        top_indices = np.argsort(similarities)[-11:-1][::-1]
        
        recommendations = []
        for i in top_indices:
            # Map back from matrix index -> movieId -> title
            mid = user_item_matrix.columns[i]
            title = movies[movies['movieId'] == mid]['title'].values[0]
            recommendations.append(title)
            
        return recommendations
    except Exception as e:
        return [f"Movie not found or error: {str(e)}"]

if __name__ == "__main__":
    print("Training Recommendation System...")
    m, uim, itm, corr = train_recommender()
    
    # Test
    test_movie = "Toy Story"
    print(f"\nRecommendations for '{test_movie}':")
    recs = get_recommendations(test_movie, m, corr, uim)
    for r in recs:
        print(f"- {r}")
