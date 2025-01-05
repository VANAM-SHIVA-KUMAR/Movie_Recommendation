from flask import Flask
from flask import render_template, request
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
@app.route("/")
def man():
    return render_template('home.html')
@app.route('/Predict',methods=['POST'])
def home():
    data = pd.read_csv('final_data.csv')
    # genre = 'Drama'  
    # threshold = 20  #no.of recommendations
    # min_rating = 4
    # N = 1 #no.of movies to be returned
    genre = request.form['a'].title()
    threshold = int(request.form['b'])
    min_rating = int(request.form['c'])
    N = int(request.form['d'])
    recommended_movies = popularity_recommender(genre, threshold, min_rating,N,data)
    #recommended_movies
    html_output = recommended_movies.to_html(index=True)
    html_output = html_output.replace('<table', '<table style="border-collapse: collapse;"')
    return render_template('prediction.html',data=html_output)


def popularity_recommender(genre, threshold, min_rating, N,data):
    genre_movies = data[data['genres'].str.contains(genre)]
    movie_stats = genre_movies.groupby('title').agg({'rating': ['mean', 'count']})
    popular_movies = movie_stats[movie_stats['rating']['count'] >= threshold]
    popular_movies = popular_movies[popular_movies['rating']['mean'] >= min_rating]
    popular_movies = popular_movies.sort_values(('rating', 'mean'), ascending=False)
    if popular_movies.empty:
        return "No Movies Found for given criteria"
    recommended_movies = popular_movies.head(N)
    return recommended_movies




if __name__ == "__main__":
    app.run(debug=True)

