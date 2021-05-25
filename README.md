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
- [/movie/{id}](#Movie-ID)
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
Add individual movie to the database if not already in database.
#### URL
`/movie`
#### Method
`POST`
#### Data Params
> Must be a valid JSON
- name : string **(required)**
- director: string **(required)**
- genres : list of string **(required)** _if no genres then empty list_
- date : string _must in such format YYYY-MM-DD_
- length : integer
#### Respond 
**Success**
- **_code_**: 201 <br/>
**_content_**:
    ``` json
    {
      "id": 1
    }
    ```
**Error**
- **_code_**: 400 BAD REQUEST <br/>
**_content_**:
    ``` json
    {
      "error":"Missing required field."
    }
    ```
    OR
    ```json
    {
      "error":"Request body must be in JSON"
    }
    ```
    OR
    ``` json
    {
      "error":"Field type error"
    }
    ```
    OR
    ``` json
    {
      "error":"date format must be YYYY-MM-DD"
    }
    ```
    OR
    ``` json
    {
      "error":"Movie with same name existed"
    }
    ```
    OR
    ``` json
    {
      "error":"[error message from database]"
    }
    ```

- **_code_**: 409 CONFLICT <br/>
**_content_**:
    ``` json
    {
      "error":"Record already existed"
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
#### Sample Call
**POST**
``` HTTP
/movie
```
**body**
```JSON
{
  "name": "The Mitchells vs. the Machines",
  "date": "2021-04-30",
  "director": "Michael Rianda",
  "genres": [
    "Adventure",
    "Animation",
    "Comedy"
  ],
  "length": 113
}
```
**return**
```json
{
  "id":1
}
```
### Movie ID
Get individual movie with id. If no record found, empty json object will be display
### URL
`/movie/{id}`
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
**GET**
  ```http
  /movie/1
  ```
  return 
  ``` json
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