import pickle """Used to serialize and deserialize Python objects. Here, it's used to load the 
               movie list (movie_list.pkl) and similarity matrix (similarity.pkl) from files."""
import streamlit as st  """  Imports the Streamlit library, which is used for 
                             building web applications with Python. """
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
    
""" Extracts the poster path from the API response and constructs the full poster image URL.
    Returns the full URL of the poster image."""

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    """ Takes a movie title as input and returns a list of 5 recommended movie names and their poster URLs.
        For each recommended movie, fetches the poster URL using the fetch_poster function and adds the movie name and poster URL to the respective lists.
        Returns the lists of recommended movie names and poster URLs """

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
""" The st.header function displays a header at the top of the web application """
movies = pickle.load(open('model/movie_list.pkl','rb'))
""" Loads the movie list (movies) and similarity matrix (similarity) using pickle.load'  """
similarity = pickle.load(open('model/similarity.pkl','rb'))
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

""" When the button is clicked, calls the recommend function with the selected movie 
    and retrieves the recommended movie names and poster URLs.
    Uses st.image to display the poster images of the recommended movies in a grid layout 
    (st.beta_columns) with their names (st.text).   """
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])




