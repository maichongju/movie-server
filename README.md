# Movie RECT Server
> This is server side of the Movie Site project, client side can be find [here](https://github.com/maichongju/movie-client).

Using Flask as web host and MySQL as data storage. All data return in JSON formate 

## Requirement 
- python 3.x
- MySQL Server

## Quick Start
> Make sure meet all requirement software is install.
1. Install all the packages in `requirement.txt` to python
    ```python 
    pip install -r requirements.txt
    ```
2. Start MySQL server and load `db.sql` to database.
3. Start Flask Server
    ``` python
    python app.py
    ```

## API Documentation

**Table Of Content**
- [/movies](#Movies)
- [/movie](#Movie)
- [/genres](#genres)

### Movies
Get all the movies in the database 
#### URL
`/movies`
#### Method
`GET`
#### Respond
**_Success_**
- **_code_**: 200 <br>
  **_content_**:
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
    ]
  }
  ```

**_Error_**
- **_code_**: 405 METHOD NOT ALLOWED <br/>
**_content_**: 
```json
{
  "code": 405,
  "error": "The method is not allowed for the requested URL.",
  "name": "Method Not Allowed"
}
```
- **_code_**: 500 INTERNAL SERVER ERROR <br/>
**_content_** : 
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
- **_code_**: 200 <br/>
  **_content_**:
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
- **_code_**: 400 BAD REQUEST <br/>
  **_content_**:
  ```json
  {
    "error":"Invalid request"
  }
  ```
- **_code_**: 405 METHOD NOT ALLOWED <br/>
  **_content_**: 
  ```json
  {
    "code": 405,
    "error": "The method is not allowed for the requested URL.",
    "name": "Method Not Allowed"
  }
  ```
- **_code_**: 500 INTERNAL SERVER ERROR <br/>
  **_content_**: 
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
- **_code_**: 200 <br/>
  **_content_**:
  ``` json
  ["Adventure","Animation","Comedy"]
  ```
**_Error_**
- **_code_**: 405 METHOD NOT ALLOWED <br/>
  **_content_**: 
  ```json
  {
    "code": 405,
    "error": "The method is not allowed for the requested URL.",
    "name": "Method Not Allowed"
  }
  ```
- **_code_**: 500 INTERNAL SERVER ERROR <br/>
  **_content_** : 
  ```json
  {
    "error": "Internal Error"
  }
  ```