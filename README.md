# Movie RECT Server
Using Flask as web host and MySQL as data storage. All data return in JSON formate 

## API

### Movies
Get all the movies in the database 
#### URL
`/movies`
#### Method
`GET`
#### Respond
**_Success_**
- _code_: 200
  _content_:
  ```json
  {
    "count": 1,
    "data": [
    {
      "date": "2021-04-30",
      "director": "Michael Rianda",
      "genres": [
        "Adventure",
        "Animation",
        "Comedy"
      ],
      "id": 1,
      "length": 113,
      "like": 0,
      "name": "The Mitchells vs. the Machines"
    }
  }
  ```

**_Error_**
- _code_: 405 METHOD NOT ALLOWED
_content_: 
```json
{
  "code": 405,
  "error": "The method is not allowed for the requested URL.",
  "name": "Method Not Allowed"
}
```
- _code_: 500 INTERNAL SERVER ERROR
_content_ : 
```json
{
  "error": "Internal Error"
}
```

### Movie
Get individual movie with id. If no record found, empty json object will be display
### URL
`/movie`
### Method
`GET`
### URL Params
`id=[integer]`
#### Respond
**_Success_**
- _code_:200
  _content_:
  ```json
  {
    "date": "2021-04-30",
    "director": "Michael Rianda",
    "genres": [
      "Adventure",
      "Animation",
      "Comedy"
    ],
    "id": 1,
    "length": 113,
    "like": 0,
    "name": "The Mitchells vs. the Machines"
  }
  ```
**_Error_**
- _code_: 400 BAD REQUEST
  _content_:
  ```json
  {
    "error":"Invalid request"
  }
  ```
- _code_: 405 METHOD NOT ALLOWED
  _content_: 
  ```json
  {
    "code": 405,
    "error": "The method is not allowed for the requested URL.",
    "name": "Method Not Allowed"
  }
  ```
- _code_: 500 INTERNAL SERVER ERROR
  _content_ : 
  ```json
  {
    "error": "Internal Error"
  }
  ```
#### Sample
```http
/movie?id=1
```
### Genres
Get all the different avilable genres
#### URL
`/genres`
#### Method
`GET`
#### Respond 
**_Success_**
- _code_: 200
  _content_:
  ``` json
  ["Adventure","Animation","Comedy"]
  ```
**_Error_**
- _code_: 405 METHOD NOT ALLOWED
  _content_: 
  ```json
  {
    "code": 405,
    "error": "The method is not allowed for the requested URL.",
    "name": "Method Not Allowed"
  }
  ```
- _code_: 500 INTERNAL SERVER ERROR
  _content_ : 
  ```json
  {
    "error": "Internal Error"
  }
  ```