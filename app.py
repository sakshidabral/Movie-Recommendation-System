import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_posters.append(fetch_poster(movie_id))

    return recommended_movies,movie_posters

movies_dict = pickle.load(open('movie_list.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select',movies['title'].values)

if st.button('Recommend'):
    recommended_movies, movie_posters = recommend(selected_movie_name)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.text(recommended_movies[0])
        st.image(movie_posters[0])
    with c2:
        st.text(recommended_movies[1])
        st.image(movie_posters[1])
    with c3:
        st.text(recommended_movies[2])
        st.image(movie_posters[2])
    with c4:
        st.text(recommended_movies[3])
        st.image(movie_posters[3])
    with c5:
        st.text(recommended_movies[4])
        st.image(movie_posters[4])

