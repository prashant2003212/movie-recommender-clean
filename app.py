import requests
import streamlit as st
import pickle
import pandas as pd

# ----------------------------
# Page Config & Layout
# ----------------------------
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="assets/favicon.png",
    layout="wide"   # expands layout
)

# Custom CSS for max-width
st.markdown("""
    <style>
        .block-container {
            max-width: 85% !important;   /* increase width */
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .movie-title {
            font-size: 14px;
            font-weight: 600;
            text-align: center;
            margin-top: 5px;
        }
    </style>
""", unsafe_allow_html=True)



# ----------------------------
# API Key for TMDB
# ----------------------------
API_KEY = "a7a30f30fbcd1e0d561d63faf713f6b0"

# ---- Poster Fetch Function ----
@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# ---- Recommend Function ----
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id   # ✅ Use TMDB movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# ----------------------------
# Load Pickle files
# ----------------------------
movies_dict = pickle.load(open('movies_dict_main1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity_new1.pkl', 'rb'))

# ----------------------------
# Streamlit UI
# ----------------------------
# Center the title
st.markdown("""
    <style>
        .centered-title {
            text-align: center;
            font-size: 45px;
            font-weight: bold;
        }
    </style>
    <h1 class="centered-title">🎬 Movie Recommender System</h1>
""", unsafe_allow_html=True)


selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # First row
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)

    # Second row
    cols = st.columns(5)
    for i in range(5, 10):
        with cols[i-5]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)
