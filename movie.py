import json
from datetime import datetime


class Movie():
    def __init__(self, data=None):
        self.id = data['id'] if data is not None and 'id' in data else -1
        self.name = data['name'] if data is not None and 'name' in data else None
        self.director = data['director'] if data is not None and 'director' in data else None
        self.length = data['length'] if data is not None and 'length' in data else 0
        self.date = data['date'].strftime('%Y-%m-%d') if data is not None and 'date' in data else datetime.now(
        ).strftime('%Y-%m-%d')
        self.genres = [data['genres']
                       ] if data is not None and 'genres' in data else []
        self.like = data['like'] if data is not None and 'liek' in data else 0

    def toJSON(self):
        return json.dumps(self.__dict__)

    def toDict(self):
        return self.__dict__


class MovieEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == '__main__':
    m = Movie()
    print(m.toJSON())
