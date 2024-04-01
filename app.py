import streamlit as st
import pickle
import pandas as pd
import requests
st.set_page_config(layout="wide")
def fetch_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()

    # fetching ratings
    ratings = data['vote_average']

    # fetching overview
    overview = data['overview']

    # fetching poster url
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path, ratings, overview


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    recommended_movie_overviews = []
    recommended_movie_ratings = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movie_posters.append(fetch_details(movie_id)[0])
        recommended_movie_ratings.append(fetch_details(movie_id)[1])
        recommended_movie_overviews.append(fetch_details(movie_id)[2])
    return recommended_movies, recommended_movie_posters, recommended_movie_overviews, recommended_movie_ratings


movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

st.title(" Movie Recommender System ")

selected_movie_name = st.selectbox(' Select a movie you recently watched!', movies['title'].values)

if st.button("Recommend"):
    names, posters, overviews, ratings = recommend(selected_movie_name)
    tabs = st.tabs(names)
    for i in range(5):
        with tabs[i]:
            cols = st.columns(2)
            with cols[0]:
                st.subheader(names[i])
                st.image(posters[i], use_column_width="auto")

            with cols[1]:
                st.subheader("Ratings")
                st.subheader("{0:.1f}/10".format(ratings[i]))

            with st.expander("Overview"):
                st.write(overviews[i])
