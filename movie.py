import json
from datetime import datetime, date


class Movie():
    def __init__(self, data=None):
        self.id = data['id'] if data is not None and 'id' in data else -1
        self.name = data['name'] if data is not None and 'name' in data else None
        self.director = data['director'] if data is not None and 'director' in data else None
        self.length = data['length'] if data is not None and 'length' in data else 0
        if data is not None and 'date' in data:
            if isinstance(data['date'], date):
                self.date = data['date'].strftime('%Y-%m-%d')
            else:
                self.date = data['date']
        else:
            self.date = datetime.now().strftime('%Y-%m-%d')
        self.genres = [data['genres']
                       ] if data is not None and 'genres' in data else []
        self.like = data['like'] if data is not None and 'liek' in data else 0

    def toJSON(self):
        return json.dumps(self.__dict__)

    def toDict(self):
        return self.__dict__

    def toTuple(self):
        return self.name, self.director, self.length, self.date,


if __name__ == '__main__':
    m = Movie()
    print(m.toJSON())
