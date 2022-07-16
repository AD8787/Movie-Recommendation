from flask import Flask, jsonify
import csv

api = Flask(__name__)

list_of_all_movies = []

with open("movies.csv") as f:
    reader = csv.reader(f)
    data = list(reader)
    list_of_all_movies = data[1:]

list_of_liked_movies = []
list_of_disliked_movies = []
list_of_not_watched_movies = []
list_of_watched_movies = []


@api.route("/get-movies")

def get_movies():
    return jsonify({
        "data" : list_of_all_movies[0],
        "status" : "success"
    })

list_of_all_movies = []

with open("movies.csv") as f:
    reader = csv.reader(f)
    data = list(reader)
    list_of_all_movies = data[1:]

list_of_liked_movies = []
list_of_disliked_movies = []
list_of_not_watched_movies = []
list_of_watched_movies = []


@api.route("/get-movies")

def get_movies():
    return jsonify({
        "data" : list_of_all_movies[0],
        "status" : "success"
    })



# ------------------------------------------- Liked Movies ---------------------------------------------------

@api.route("/liked-movies" , methods=["POST"])

def liked_movies():
    movie = list_of_all_movies[0]
    list_of_all_movies = list_of_all_movies[1:]
    list_of_liked_movies.append(movie)
    return jsonify({
        "status" : "success"
    })


@api.route("/disliked-movies" , methods=["POST"])

def disliked_movies():
    movie = list_of_all_movies[0]
    list_of_all_movies = list_of_all_movies[1:]
    list_of_disliked_movies.append(movie)
    return jsonify({
        "status" : "success"
    })



@api.route("/liked-movies" , methods=["POST"])

def liked_movies():
    movie = list_of_all_movies[0]
    list_of_all_movies = list_of_all_movies[1:]
    list_of_liked_movies.append(movie)
    return jsonify({
        "status" : "success"
    })



if __name__ == "__main__":
    api.run()