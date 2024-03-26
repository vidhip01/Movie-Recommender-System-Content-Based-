import streamlit as st
import pickle
import requests
import re

def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    return data

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data= data.json()
    poster_path= data['poster_path']
    full_path= "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommended(movie):
    index= movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x:x[1])
    recommended_movie_name=[]
    recommended_movie_posters=[]
    for i in distance[1:6]:
        movie_id= movies.iloc[i[0]].movie_id
        recommended_movie_name.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_name, recommended_movie_posters

def ascii_sort_key(title):
    # Return the ASCII value of each character
    return [ord(char) for char in title]


st.header('Movie Recommendor System')
movies= pickle.load(open('movies.pkl', 'rb'))
similarity= pickle.load(open('similarity.pkl', 'rb'))

movie_list = sorted(movies['title'].values, key=ascii_sort_key)
selected_movie= st.selectbox(
    "Type or select any movie from dropdown",
    movie_list,
    key="dropdown_movies"
)



if st.button('Show Recommendations'):
    recommended_movie_name, recommended_movie_posters= recommended(selected_movie)
    col_num = 5  # Number of columns
    with st.container():
        for i in range(len(recommended_movie_name)):
            if i % col_num == 0:
                col = st.columns(col_num)
            with col[i % col_num]:
                st.text(recommended_movie_name[i])
                st.image(recommended_movie_posters[i])



