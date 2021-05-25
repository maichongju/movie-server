from os import times
import mysql.connector as connector
from flask.helpers import make_response
from movie import Movie
from flask import Flask, json, request
from flask_cors import CORS
from movie import Movie
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

# SQL Table name
MOVIEGENRESVIEW = 'view_movie_genres'
MOVIETABLE = 'movie'
GENRESTABLE = 'genres'
MOVIEGENRESTABLE = 'movie_genres'

# SQL
SQL_INSERT_MOVIE = "INSERT INTO {} (name, director,length,date) VALUES (%s, %s, %s, %s);".format(
    MOVIETABLE)
SQL_INSERT_MOVIE_GENRES = "INSERT INTO {} (movie_id,genres) VALUES (%s, %s);".format(
    MOVIEGENRESTABLE)
SQL_SELECT_GENRES = "SELECT * FROM genres;"
SQL_INSERT_GENRES = "INSERT INTO {} (id,name) VALUES (%s, %s)".format(
    GENRESTABLE)
SQL_SELECT_MOVIE_BY_NAME = "SELECT * FROM {} WHERE name=%s;".format(MOVIETABLE)

# SQL Constant
SQL_GENRES_NONE = 'NA'

LOGFILE = 'log.log'
STATUSCODE = StatusCode()

# Error Description
GENERAL_500_INTERNAL_SERVER_ERROR = json.dumps(
    {"error": "Internal server error"}), 500

GENRES = {}


def getDatabase():
    return Database(host, user, pwd, dbName)


def log(url, msg, body=None):
    file = open(LOGFILE, 'a', encoding='utf-8')
    timeString = datetime.now().strftime('[%Y-%m-%y %H:%M:%S]')
    if body is None:
        file.write('{} [{}] {}\n'.format(timeString, url, str(msg)))
    else:
        file.write('{} [{}] {} {}\n'.format(timeString, url, str(msg), body))

    print(url)
    print(msg)
    file.close


def validDateFormat(date):
    """Check the given date format is valid

    Args:
        date (str): date string need to check

    Returns:
        bool: True if is valid, False otherwise
    """
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def findGenresID(source, target):
    """check if genres existed in the given source, if found id will 
    return 

    Args:
        source (list): genres
        target (str): target genres

    Returns:
        (str): genres id if found, None otherwise
    """
    if not isinstance(source, list):
        return None
    for genres in source:
        if target.lower() == genres['name'].lower():
            return genres['id']
    return None


def genresIDExist(source, target):
    for genres in source:
        if target == genres['id']:
            return True
    return False


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
            if 'genres' in item and item['genres'].lower() != 'none' and item['genres'] not in movie.genres:
                movie.genres.append(item['genres'])
    movies.append(movie.toDict())
    return movies


@app.route('/movies', methods=['GET'])
def getMovies():
    db = getDatabase()
    SQL = 'SELECT * FROM {};'.format(MOVIEGENRESVIEW)
    try:
        data = db.fetchAll(SQL, header=True)
        data = rawMoviesCombind(data)
        data = {'count': len(data), 'data': data}
    except connector.Error as err:
        log(request.full_path, err.msg)
        return GENERAL_500_INTERNAL_SERVER_ERROR
    db.close()
    return json.dumps(data)


@app.route('/movie/<movieid>', methods=['GET', 'POST'])
def getMovie(movieid):
    if movieid is None or not movieid.isnumeric():
        return json.dumps({'error': 'Invalid request'}), 400
    if request.method == 'GET':
        SQL = 'SELECT * FROM {} WHERE id = %s;'.format(MOVIEGENRESVIEW)
        params = (movieid,)
        db = getDatabase()
        try:
            data = db.fetchAll(SQL, params=params, header=True)
        except connector.Error as err:
            log(request.full_path, err.msg)
            return GENERAL_500_INTERNAL_SERVER_ERROR
        db.close()

        return json.dumps(rawMoviesToDict(data))
    elif request.method == 'POST':
        if not request.is_json:
            return json.dumps({"error": "Request body must be in JSON"}), 400
        return 'POST REQUEST'


@app.route('/movie', methods=['POST'])
def addMovie():
    if not request.is_json:
        return json.dumps({"error": "Request body must be in JSON"}), 400
    body = request.get_json()
    # check if request json has all required field valid
    if 'name' not in body or \
        'director'not in body or \
            'genres'not in body:
        return json.dumps({"error": "Missing required field."}), 400
    # check if all the type meet the stander
    if not isinstance(body['name'], str) or \
        not isinstance(body['director'], str) or\
        not isinstance(body['genres'], list) or \
        ('date' in body and not isinstance(body['date'], str)) or \
            ('length' in body and not isinstance(body['length'], int)):
        return json.dumps({"error": "Field type error"}), 400
    if 'date' in body and not validDateFormat(body['date']):
        return json.dumps({"error": "date format must be YYYY-MM-DD"}), 400
    movie = Movie(body)
    db = getDatabase()
    try:
        # check if same name exist
        body['name'] = body['name'].strip()
        exist = len(db.fetchAll(
            SQL_SELECT_MOVIE_BY_NAME, (body['name'],))) != 0
        if exist:
            return json.dumps({"error": "Movie with same name existed"}), 400
        db.execute(SQL_INSERT_MOVIE, movie.toTuple())
        id = db.fetchAll('SELECT LAST_INSERT_ID();')[0][0]
        movieGenres = body['genres']
        if len(movieGenres) > 0:
            # Get all the genres from database and check if the genres exist
            genres = db.fetchAll(SQL_SELECT_GENRES, header=True)
            # Remove duplicate genres
            movieGenres = list(set(movieGenres))
            for g in movieGenres:
                gid = findGenresID(genres, g)
                if gid is None:
                    # by default take the first three letter as the id for the genres
                    l = 3
                    # id need to be all caps
                    newgid = g[:l].upper()
                    isPass = False
                    while genresIDExist(genres, newgid):
                        l += 1
                        if l > len(g):
                            isPass = True
                            break
                        newgid = g[:l].upper()
                    if not isPass:
                        db.execute(SQL_INSERT_GENRES, (newgid, g,))
                        gid = newgid
                        genres.append({"id": newgid, "name": g})
                if gid is not None:
                    db.execute(SQL_INSERT_MOVIE_GENRES, (id, gid,))
        else:
            # There are no genres, use NA
            db.execute(SQL_INSERT_MOVIE_GENRES, (id, 'NA'))
        db.close()
        return json.dumps({"id": id})
    except connector.Error as err:
        # 2000-2999 error code is client side error
        if err.errno >= 2000 and err.errno < 3000:
            return json.dumps({"error": err.msg}), 400
        else:
            # Other error code are server side error
            log(request.full_path, err.msg, request.get_json())
            return GENERAL_500_INTERNAL_SERVER_ERROR


@app.route('/genres', methods=['GET'])
def getGenres():
    db = getDatabase()
    SQL = 'SELECT name FROM genres;'
    try:
        raw = db.fetchAll(SQL)
        data = [d[0] for d in raw]
    except connector.Error as err:
        log(request.full_path, err.msg)
        return GENERAL_500_INTERNAL_SERVER_ERROR
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
