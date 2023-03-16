import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('tmdb.csv')

class RECOMMEND():
    def __init__(self , vectorizer =TfidfVectorizer ):
        self.vectorzier = vectorizer
        
    
    def get_recommendation(self, title):
        count = self.vectorzier(stop_words='english')
        count_matrix = count.fit_transform(df['soup'])
        cos_sim = cosine_similarity(count_matrix,count_matrix)

        idices = pd.Series(df.index,index=df['title'])
        idx = idices[title]

        sim_score = list(enumerate(cos_sim[idx]))
        data = sorted(sim_score,key=lambda x : x[1],reverse=True)
        sim_idices = data[1:11]
        sim_sorted = [x[0] for x in sim_idices]
        title = df['title'].iloc[sim_sorted]

        release_date = df['release_date'].iloc[sim_sorted]
        homepage_url = df['homepage'].iloc[sim_sorted]
        
        movie_df = pd.DataFrame(columns=['title','release_date','homepage_url'])
        movie_df['title'] = title
        movie_df['release_date'] = release_date
        movie_df['homepage_url'] = homepage_url
        
        return movie_df



# RECOMMEND().get_recommendation('Avatar')