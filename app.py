import requests
import streamlit as st
import pickle
import pandas as pd
import gdown

API_KEY = "a7a30f30fbcd1e0d561d63faf713f6b0"

# ---- Google Drive File IDs ----
MOVIES_FILE_ID = "1PTi4P7N_FGIksojIpNvmeGXnODdrNKf6"
SIMILARITY_FILE_ID = "1wEOB82JzO31usq7hNwdfH1knLv4uT4fS"

# ---- Download from Google Drive if not exists ----
gdown.download(f"https://drive.google.com/uc?id={MOVIES_FILE_ID}", "movies_dict_main1.pkl", quiet=False)
gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}", "similarity_new1.pkl", quiet=False)

@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


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


# ---- Load Pickle files ----
movies_dict = pickle.load(open('movies_dict_main1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity_new1.pkl', 'rb'))

# ---- Streamlit UI ----
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # first row
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

    # second row
    cols = st.columns(5)
    for i in range(5, 10):
        with cols[i-5]:
            st.text(names[i])
            st.image(posters[i])
