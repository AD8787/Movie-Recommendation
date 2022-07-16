import pandas as pd
import numpy as np
import plotly.express as px
from ast import literal_eval

df1 = pd.read_csv("datasets/tmdb_5000_credits.csv")
df2 = pd.read_csv("datasets/tmdb_5000_movies.csv")
from sklearn.feature_extraction.text import CountVectorizer
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])
print(df1.head())



# 	movie_id	    title	                                                cast	                                        crew
# 0	19995	    Avatar                                     	[{"cast_id": 242, "character": "Jake Sully", "...	[{"credit_id": "52fe48009251416c750aca23", "de...
# 1	285	        Pirates of the Caribbean: At World's End	[{"cast_id": 4, "character": "Captain Jack Spa...	[{"credit_id": "52fe4232c3a36847f800b579", "de...
# 2	206647	    Spectre	                                    [{"cast_id": 1, "character": "James Bond", "cr...	[{"credit_id": "54805967c3a36829b5002c41", "de...
# 3	49026	    The Dark Knight Rises	                    [{"cast_id": 2, "character": "Bruce Wayne / Ba...	[{"credit_id": "52fe4781c3a36847f81398c3", "de...
# 4	49529	    John Carter                                	[{"cast_id": 5, "character": "John Carter", "c...	[{"credit_id": "52fe479ac3a36847f813eaa3", "de


from sklearn.metrics.pairwise import cosine_similarity
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# print(df2.head())

#    budget	            genres	                                             homepage	                             id	            keywords	original_language	original_title	overview	popularity	production_companies	production_countries	release_date	revenue	runtime	spoken_languages	status	tagline	title	vote_average	vote_count
# 0	237000000	[{"id": 28, "name": "Action"}, {"id": 12, "nam...	http://www.avatarmovie.com/	                    19995	      [{"id": 1463, "name": "culture clash"}, {"id":...	en	Avatar	In the 22nd century, a paraplegic Marine is di...	150.437577	[{"name": "Ingenious Film Partners", "id": 289...	[{"iso_3166_1": "US", "name": "United States o...	2009-12-10	2787965087	162.0	[{"iso_639_1": "en", "name": "English"}, {"iso...	Released	Enter the World of Pandora.	Avatar	7.2	11800
# 1	300000000	[{"id": 12, "name": "Adventure"}, {"id": 14, "...	http://disney.go.com/disneypictures/pirates/	285     	[{"id": 270, "name": "ocean"}, {"id": 726, "na...	en	Pirates of the Caribbean: At World's End	Captain Barbossa, long believed to be dead, ha...	139.082615	[{"name": "Walt Disney Pictures", "id": 2}, {"...	[{"iso_3166_1": "US", "name": "United States o...	2007-05-19	961000000	169.0	[{"iso_639_1": "en", "name": "English"}]	Released	At the end of the world, the adventure begins.	Pirates of the Caribbean: At World's End	6.9	4500

df1.columns = ['id', 'title', 'cast', 'crew']
df2 = df2.merge(df1, on = 'id')

print(df2.head())

# budget	genres	homepage	id	keywords	original_language	original_title	overview	popularity	production_companies	production_countries	release_date	revenue	runtime	spoken_languages	status	tagline	title	vote_average	vote_count	tittle	cast	crew


# --------------------------------------- Demographic Filtering -----------------------------------------------------------------------------


#IMDb Rating/ Weighted Rating = ((v/(v+m))*R)+((m/(v+m))*C)

# ● v - The number of votes for the
# movies (or number of
# ratings/reviews in case of an
# amazon product)

# ● m - The minimum votes
# required to be listed in the
# chart

# ● R - Average rating of the movie

# ● C - Mean votes across the
# whole report


C = df2['vote_average'].mean()
print("----------------------")
print(C)


m = df2['vote_count'].quantile(0.9)
print("----------------------")
print(m)

q_movies = df2.copy().loc[df2['vote_count'] >= m]
print("----------------------")
print(q_movies.shape)

def weighted_rating(x, m = m, C = C):
    v = x['vote_count']
    R = x['vote_average']
    return ((v/(v+m))*R)+((m/(v+m))*C)

q_movies['score'] = q_movies.apply(weighted_rating, axis = 1)
q_movies = q_movies.sort_values('score', ascending = False)

print("----------------------------------------------------------------------")

# print(q_movies[['original_title' , 'vote_count' , 'vote_average' , 'score']].head(10))
# print(q_movies.head(17))

graph = px.bar((q_movies.head(10).sort_values('score', ascending=True)), x="score", y="original_title", orientation='h')
graph.show()



# ----------------------------------------- Content Based Filtering ----------------------------------------------------------------




print(df2[['original_title', 'cast', 'crew', 'keywords', 'genres']].head(3))


def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
        else:
            return i.nan

df2['director'] = df2['crew'].apply(get_director)

def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        return names
    return []
   
features = ['cast', 'keywords', 'genres']

for feature in features:
    df2[feature] = df2[feature].apply(get_list)


print(df2[['title', 'cast', 'director', 'keywords', 'genres']].head(3))


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    df2[feature] = df2[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
df2['soup'] = df2.apply(create_soup, axis=1)

indices = pd.Series(df2.index, index=df2['title'])

def get_recommendations(title, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df2['title'].iloc[movie_indices]


get_recommendations("Iron Man" , cosine_sim2)