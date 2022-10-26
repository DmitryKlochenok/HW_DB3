# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")

@movie_ns.route("/")
class MoviesViews(Resource):
    def get(self):
        query = Movie.query.all()
        movies_schema = MovieSchema(many=True)
        return movies_schema.dump(query)

    def post(self):
        request_json = request.json
        new_movie = Movie(**request_json)
        with db.session.begin():
            db.session.add(new_movie)
        return ""



@movie_ns.route("/<uid>")
class MovieViews(Resource):
    def get(self, uid):
        query = Movie.query.get(uid)
        movies_schema = MovieSchema()
        return movies_schema.dump(query)

    def put(self, id):
        movie = Movie.query.get(id)
        request_json = request.json
        movie.id = request_json.id
        movie.title = request_json.title
        movie.description =request_json.description
        movie.trailer =request_json.trailer
        movie.year =request_json.year
        movie.rating =request_json.rating
        db.session.add(movie)
        db.session.commit()

    def delete(self, id):
        query = Movie.query.get(id)
        db.session.delete(query)
        db.session.commit()
        return ""


@movie_ns.route("/?director_id=<id>")
class DirectorViews(Resource):
    def get(self, id):
        query = Movie.query.filter(director_id=id)
        movies_schema = MovieSchema()
        return movies_schema.dump(query)

@movie_ns.route("/?genre_id=<id>")
class GenreViews(Resource):
    def get(self, id):
        query = Movie.query.filter(genre_id=id)
        movies_schema = MovieSchema()
        return movies_schema.dump(query)

@director_ns.route("/")
class DirectorsViews(Resource):
    def get(self):
        query = Director.query.all()
        directors_schema = DirectorSchema(many=True)
        return directors_schema.dump(query)

@director_ns.route("/<uid>")
class DirectorViews(Resource):
    def get(self, uid):
        query = Director.query.get(uid)
        directors_schema = DirectorSchema()
        return directors_schema.dump(query)


if __name__ == '__main__':
    app.run(debug=True)
