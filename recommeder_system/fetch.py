import requests
import json

movie_dict = {}

#main movie class
class movie:
    def __init__(self, id='', title="None", poster_url="None", score="None", date="None", overview="None" , back_drop="None"):
        self.id = id
        self.title = title
        self.poster= "http://image.tmdb.org/t/p/w200" + str(poster_url)
        self.score = score
        self.date = date
        self.overview = overview
        self.back_drop = "http://image.tmdb.org/t/p/w200" + str(back_drop)


        
    
class movie_collection:
    def __init__(self,results=[]):
        self.results = results
        
    def fetch(self,url):
        results = json.loads(requests.get(url).text)["results"]
        
        # print(results)
        for  i in results:
            if i["id"] and i["title"] and i["poster_path"] and i["vote_average"] and i["release_date"] and i["overview"] and i["backdrop_path"]:
                self.results.append(movie(i["id"],i["title"],i["poster_path"],i["vote_average"],i["release_date"],i["overview"],i["backdrop_path"]))
            # print(movie(i["id"],i["title"],i["poster_path"],i["vote_average"],i["release_date"],i["overview"],i["backdrop_path"]))
            
        return results
if __name__ == "__main__":
    mov = movie_collection()
    mov.results = []
    data = mov.fetch("https://api.themoviedb.org/3/search/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&query=샤잠")
    # print(data)
    for obj in data:
        # print(obj)
        for i in obj:
            print(i)
