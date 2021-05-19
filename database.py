import mysql.connector as connector


class Database:
    def __init__(self, host, user, password, database) -> None:
        self.error = None
        self.cursor = None
        self._connect = None
        try:
            self._connect = connector.connect(
                host=host, user=user, password=password, db=database)
            self.cursor = self._connect.cursor()
        except connector.Error as err:
            self.error = err

    def fetchAll(self, SQL, params=None, header=False):
        """Fetch all the record from the SQL, if return value is None it means there are 
        error during execute SQL, check error variable to see the error. If header is true,
        return formate will be the follwoing format [records-dictionary] each record include 
        the column name, else only [recoreds]
        will be return

        Args:
            SQL (string): SQL statement
            header (bool, optional): does return include column name. Defaults to False.

        Returns:
            if header is True:  [records-dictionary]
            if header is False: [records]
        """

        if (self.cursor is None):
            return None
        try:
            if params is None:
                self.cursor.execute(SQL)
            else:
                self.cursor.execute(SQL, params)
            rows = self.cursor.fetchall()
            if not header:
                return rows
            columnName = [item[0] for item in self.cursor.description]
            result = []
            for item in rows:
                itemDict = {}
                for i in range(len(item)):
                    itemDict[columnName[i]] = item[i]
                result.append(itemDict)

            return result
        except connector.Error as err:
            self.error = err
            return None

    def hasError(self) -> bool:
        return self.error is not None

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self._connect is not None:
            self._connect.close()


if __name__ == "__main__":
    db = Database('localhost', 'root', 'password', 'movies')
    print(db.fetchAll('SELECT * FROM movie', True))
