from flask import Flask , render_template , request
import requests
import json
from datetime import date
from fetch import movie, movie_collection
import pandas as pd

app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        year = date.today().year
        year_url = f'http://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&primary_release_year={year}&sort_by=popularity.desc'
        result = json.loads(requests.get('https://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&primary_release_year=2023&sort_by=popularity.desc').text)
        # print(result['results'][1])
        top_year = movie_collection()
        top_year.results=[]
        top_year.fetch(year_url)
        genre_url =f'https://api.themoviedb.org/3/genre/movie/list?api_key=da396cb4a1c47c5b912fda20fd3a3336&language=en-US'
        genres = json.loads(requests.get(genre_url).text)
        # print(genres)
        top_genre_collection = []
        for data in genres['genres']:
            # print(data['id'])
            genre_id = f'https://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&with_genres={data["id"]}&sort_by=popularity.desc'
            # print(genre_id)
            top_genre = movie_collection()
            top_genre.fetch(genre_id)
            # for result in top_genre.results:
            #     print(result.title)
            top_genre_id = [top_genre.results , data['name']]
            top_genre_collection.append(top_genre_id)
        # print(top_genre_collection)
        return render_template('index.html',top_year = top_year.results, year= year, top_genre=top_genre_collection)

    elif request.method == "POST":
        search  = request.form["search"]
        # print(search)
        movie_dic = movie_collection()
        movie_dic.results=[]
        id_url = f"http://api.themoviedb.org/3/search/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&query={search}"
        movie_dic.fetch(id_url)
        return render_template('landing.html', movie=movie_dic.results, key_word=search)

@app.route('/details/<id>')
def details(id):
    url = f"http://api.themoviedb.org/3/movie/{id}?api_key=da396cb4a1c47c5b912fda20fd3a3336"
    data = json.loads(requests.get(url).text)
    data_json = movie(data["id"],data["title"],data["poster_path"],data["vote_average"],data["release_date"],data["overview"],data["backdrop_path"])
    return render_template('details.html', movie=data_json)
    

if __name__ == '__main__':
    app.run(debug=True)