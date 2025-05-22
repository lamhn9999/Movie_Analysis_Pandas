import pandas as pd
from collections import Counter
import time

start = time.time()

res_dir = "../Results/"
df_main = pd.read_csv("../Data/Movies_Data.csv")    

def normalize():
    global df_main
    df_main = df_main.map(lambda x : x.strip() if isinstance(x, str) else x) 
    df_main = df_main.drop_duplicates(keep='first')
    pd.to_numeric([df_main['vote_average'], df_main['revenue']], errors='coerce')

def transform_release_date(row):
    return row['release_date'][:-2] + str(row['release_year'])
def asc_release_date():
    df_release_date_asc = df_main
    df_release_date_asc['release_date'] = df_release_date_asc.apply(transform_release_date, axis=1)
    df_release_date_asc['release_date'] = pd.to_datetime(df_release_date_asc['release_date'], format="%m/%d/%Y")
    df_release_date_asc = df_release_date_asc.sort_values(by = 'release_date', ascending=True)
    df_release_date_asc.to_csv(res_dir + "Asc_Release_date.csv", index = False)

def abv_7point5():
    df_abv_7point5 = df_main[df_main['vote_average'] >= 7.5].sort_values(by = 'vote_average', ascending=False)
    df_abv_7point5.to_csv(res_dir + "Abv_7point5.csv", index = False)

def highest_lowest_revenue():
    df_highest_rev = df_main.sort_values(by = 'revenue', ascending=False)
    df_highest_rev.head(20).to_csv(res_dir + "Highest_revenue.csv", index = False)
    lowest_rev = df_highest_rev.iloc[-1]['revenue']
    df_lowest_rev = df_main[df_main['revenue'] == lowest_rev]
    df_lowest_rev.to_csv(res_dir + "Lowest_revenue.csv", index = False)

def most_movies():
    director_total_movies = df_main['director'].str.split('|').explode().value_counts().reset_index()
    director_total_movies.columns = ['director', 'count']
    actor_total_movies = df_main['cast'].str.split('|').explode().value_counts().reset_index()
    actor_total_movies.columns = ['actor', 'count']
    actor_total_movies.columns = ['actor', 'count']
    director_ground = director_total_movies.iloc[9]['count']
    actor_ground = actor_total_movies.iloc[9]['count']
    director_total_movies[director_total_movies['count'] >= director_ground].to_csv(res_dir + 'Most_movies_director.csv', index = False)
    actor_total_movies[actor_total_movies['count'] >= actor_ground].to_csv(res_dir + 'Most_movies_actor.csv', index = False)

def genres_count():
    genres = df_main['genres'].str.split('|').explode().value_counts().reset_index()
    genres.columns = ['genre', 'count']
    genres.to_csv(res_dir + 'Genres_count.csv', index = False)

def most_collaborated():
    pair_counter = Counter()
    for _, row in df_main.iterrows():
        try:
            directors = row['director'].split('|')
            actors = row['cast'].split('|')
        except:
            pass
        else:
            for director in directors:
                director = director.strip()
                for actor in actors:
                    actor = actor.strip()
                    if director != actor:
                        pair_counter[(director, actor)] += 1
    most_common = pair_counter.most_common(10)
    for pair, count in most_common:
        print(f"{pair[0]} & {pair[1]} worked together {count} times")
        

def single_output():
    full_revenue_sum = df_main['revenue'].sum()
    print(f"Total revenue of all movies: {full_revenue_sum}")

if(__name__ == "__main__"):
    normalize()
    genres_count()
    most_movies()
    highest_lowest_revenue()
    abv_7point5()
    asc_release_date()
    single_output()
    most_collaborated()
    print(f"Execution time: {time.time() - start}")
