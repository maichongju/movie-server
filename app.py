from os import times

from flask.helpers import make_response
from movie import Movie
from flask import Flask, json, request
from flask_cors import CORS
from movie import Movie, MovieEncoder
from database import Database
from const import StatusCode
from datetime import datetime
from werkzeug.exceptions import HTTPException
port = 4000
app = Flask(__name__)
CORS(app)

# const
host = 'localhost'
user = 'root'
pwd = 'password'
dbName = 'movies'


MOVIEGENRESTABLE = 'view_movie_genres'

LOGFILE = 'log.log'
STATUSCODE = StatusCode()


def getDatabase():
    return Database(host, user, pwd, dbName)


def log(url, msg):
    file = open(LOGFILE, 'a', encoding='utf-8')
    timeString = datetime.now().strftime('[%Y-%m-%y %H:%M:%S]')
    file.write('{} [{}] {}\n'.format(timeString, url, str(msg)))
    print(url)
    print(msg)
    file.close


@app.route('/')
@app.route('/index')
def index():
    return 'Index Page'


def rawMoviesToDict(data):
    """Generate a single movie dict with the given data

    Args:
        data (list): single movie list

    Raises:
        ValueError: invalid input data

    Returns:
        dictionary: dictionary of the single movie
    """
    if data is None or not isinstance(data, list):
        raise ValueError('Invalid input data')
    elif len(data) == 0:
        return {}
    movie = Movie(data[0])
    for item in data[1:]:
        if 'genres' in item and item['genres'] not in movie.genres:
            movie.genres.append(item['genres'])
    return movie.toDict()


def rawMoviesCombind(data):
    if data is None:
        raise ValueError('Invalid input data')
    movies = []
    if len(data) == 0:
        return movies
    movie = Movie(data[0])
    for item in data[1:]:
        if item['id'] != movie.id:
            movies.append(movie.toDict())
            movie = Movie(item)
        else:
            if 'genres' in item and item['genres'] not in movie.genres:
                movie.genres.append(item['genres'])
    if len(movies) == 0:
        movies.append(movie.toDict())
    return movies


@app.route('/movies', methods=['GET'])
def getMovies():
    db = getDatabase()
    SQL = 'SELECT * FROM {};'.format(MOVIEGENRESTABLE)
    data = db.fetchAll(SQL, header=True)
    if db.error is not None:
        log(request.full_path, db.error)
        return json.dumps({'error': 'Internal Error'}), 500
    data = rawMoviesCombind(data)
    data = {'count': len(data), 'data': data}
    db.close()
    return json.dumps(data)


@app.route('/movie', methods=['GET'])
def getMovie():
    movieid = request.args.get('id')
    if movieid is None or not movieid.isnumeric():
        return json.dumps({'error': 'Invalid request'}), 400
    SQL = 'SELECT * FROM {} WHERE id = %s;'.format(MOVIEGENRESTABLE)
    params = (movieid,)
    db = getDatabase()
    data = db.fetchAll(SQL, params=params, header=True)
    db.close()
    if db.error is not None:
        log(request.full_path, db.error)
        return json.dumps({'error': 'Internal Error'}), 500
    return json.dumps(rawMoviesToDict(data))


@app.route('/genres', methods=['GET'])
def getGenres():
    db = getDatabase()
    SQL = 'SELECT name FROM genres;'
    raw = db.fetchAll(SQL)
    data = [d[0] for d in raw]
    if db.error is not None:
        log(request.full_path, db.error)
        return json.dumps({'error': "Internal Server Error"}), 500
    db.close()
    return json.dumps(data)


@app.route('/400')
def badrequest():
    return 'bad request', 400


@app.errorhandler(HTTPException)
def handleExceptin(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "error": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(Exception)
def handleExceptin(e):
    if isinstance(e, HTTPException):
        return e
    log(request.full_path, e)
    return {'error': 'Internal Server Error'}, 500


if __name__ == '__main__':
    app.run(host="localhost", port=port, debug=True)
