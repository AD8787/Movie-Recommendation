import csv
import pandas as pd

with open("movies.csv") as f:
    csvreader = csv.reader(f)
    data = list(csvreader)
    all_movies = data[1:]
    headers = data[0]

headers.append("poster_link")

with open("final.csv" , "a+") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)

with open("movie_links.csv") as f:
    csvreader = csv.reader(f)
    data = list(csvreader)
    all_movie_links = data[1:]

for i in all_movies:
    poster_found = any(i[8] in movie_link_items for movie_link_items in all_movie_links)   
    if poster_found:
        for movie_link_item in all_movie_links:
            if i[8] == movie_link_item[0]:
                i.append(movie_link_item[1])
                if len(i) == 28:
                    with open("final.csv" , "a+") as f:
                        csvwriter = csv.writer(f)
                        csvwriter.writerow(i)
