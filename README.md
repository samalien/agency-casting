# Casting Agency
Casting Agency is a company that creating movies and managing and assigning actors to those movies.

Hosted on heroku: [https://agency-casting.herokuapp.com/](https://agency-casting.herokuapp.com/)
# Motivation
This is my capstone project for the Udacity FSND nanodegree. It covers
1.	Database modeling with postgres & sqlalchemy  : models.py
2.	API with Flask :app.py
3.	tests with Unittest :test_app
4.	Authorization & Role based Authentification with Auth0 :auth.py
5.	Deployment on Heroku
# Start Project 
* Install the latest version of [Python 3](https://www.python.org/downloads/) and [postgres](https://www.postgresql.org/download/)  on your machine.
* cd to the correct folder (with all app files) 
* To start and run the local development server,
### 1.	Initialize and activate a virtualenv:
```
$ virtualenv --no-site-packages env_capstone
$ source env_capstone/scripts/activate
```
### 2.	Install the dependencies:
```
$ pip install -r requirements.txt
```
### 3.	Configure database
to be able to run this project locally you have to edit the models.py file by modifying these two lines by putting your personal parameters. so that it connects to your local database Change database config so it can connect to your local postgres database
```
database_name = '<your_database_name>'
database_local_path = "postgres://{}@{}/{}". format('<user_name>:<password>','localhost:5432', database_name)
```
#### 4.	Setup Auth0 
If you only want to test the API, you can simply take the existing bearer tokens in config.py.

If you already know your way around Auth0, just insert your data into config.py => auth0_config.
### 5.	Run the development server:
```
$ set FLASK_APP=app.py
$ set FLASK_ENV=development
$ flask run
```
### 6.	(optional) To execute tests, run
```
$ python test_app.py
```
If you choose to run all tests, it should give this response if everything went fine:
```
$ python test_app.py
...........................
----------------------------------------------------------------------
Ran 27 tests in 18.132s
OK
```
# API Documentation
Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.
## Available Endpoints
#### GET /movies
Gets all movies from the db.
##### Response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 2,
            "release_date": "Thu, 02 Jan 2020 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 3,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 4,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 5,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 6,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 7,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 8,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 9,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 10,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        }
    ],
    "success": true,
    "total_movies": 12
}
```
#### POST /movies/search
Adds a new movie to the db.
##### Data:
```
{
    "title":"test",
    "release_date":"2020/5/7"
}

Response:
{
    "created": 13,
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 2,
            "release_date": "Thu, 02 Jan 2020 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 3,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 4,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 5,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 6,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 7,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 8,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 9,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 10,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 11,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 12,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 13,
            "release_date": "Thu, 07 May 2020 00:00:00 GMT",
            "title": "test"
        }
    ],
    "success": true,
    "total_movies": 13
}
```
#### POST /movies/search
Search Movie by title:
##### Data:
```
{
    "searchTerm":"the"
}
```
##### Response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 2,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        }
    ],
    "success": true,
    "total_movies": 2
}
```
#### PATCH /movies/<int:id>
Edit data on a movie in the db.
##### Data:
```
{
  "release_date": "2021-02-02"
}
```
##### Response :
```
{
    "movies": [
        {
            "id": 2,
            "release_date": "Thu, 02 Jan 2020 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 3,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 1,
            "release_date": "Tue, 02 Feb 2021 00:00:00 GMT",
            "title": "The Grudge"
        }
    ],
    "success": true,
    "total_movies": 3,
    "updated": 1
}
```
#### DELETE /movies/<int:id>
Delete a movie from the db.
##### Response:
```
{
    "deleted": 13,
    "movies": [
        {
            "id": 2,
            "release_date": "Thu, 02 Jan 2020 00:00:00 GMT",
            "title": "Weathering with You"
        },
        {
            "id": 3,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        {
            "id": 1,
            "release_date": "Tue, 02 Feb 2021 00:00:00 GMT",
            "title": "The Grudge"
        }
    ],
    "success": true,
    "total_movies": 3
}
```
#### GET /actors/<actor_id>/movies
Gets movies by actor
##### Response:
```
{
    "movies": {
        "1": {
            "id": 1,
            "release_date": "Fri, 03 Jan 2020 00:00:00 GMT",
            "title": "The Grudge"
        },
        "2": {
            "id": 2,
            "release_date": "Wed, 04 May 2016 00:00:00 GMT",
            "title": "Weathering with You"
        }
    },
    "success": true,
    "total_movies_by_actor": 2
}
```
#### GET /actors
Gets all actors from the db.
##### Response:
```
{
    "actors": [
        {
            "age": 25,
            "gender": "Male",
            "id": 1,
            "name": "Will smith"
        },
        {
            "age": 53,
            "gender": "Male",
            "id": 2,
            "name": "William powell"
        },
    ],
    "success": true,
    "total_actors": 2
}
```
#### POST /actors/search
Adds a new actor to the db.
##### Data:
```
{
  "name": "Test",
  "gender": "Female"
}
```
##### Response:
```
{
    "actors": [
        {
            "age": 25,
            "gender": "Male",
            "id": 1,
            "name": "Will smith"
        },
        {
            "age": 53,
            "gender": "Male",
            "id": 2,
            "name": "William powell"
        },
        {
            "age": 25,
            "gender": "Female",
            "id": 3,
            "name": "Test"
        }
    ],
    "created": 3,
    "success": true,
    "total_actors": 3
}
```
#### POST /actors/search
Search actor by name :
##### Data :
```
{
    "searchTerm":"will"
}
```
##### Response :
```
{
    "actors": [
        {
            "age": 25,
            "gender": "Male",
            "id": 1,
            "name": "Will smith"
        },
        {
            "age": 53,
            "gender": "Male",
            "id": 2,
            "name": "William powell"
        }
    ],
    "success": true,
    "total_actors": 2
}
```
#### PATCH /actors/<int:id>
Edit data on a actor in the db.
##### Data:
```
{
    "age":"20",
}
```
##### Response
```
{
    "actors": [
        {
            "age": 53,
            "gender": "Male",
            "id": 2,
            "name": "William powell"
        },
        {
            "age": 20,
            "gender": "Male",
            "id": 1,
            "name": "Will smith"
        }
    ],
    "success": true,
    "total_actors": 2,
    "updated": 1
}
```
#### DELETE /actors/<int:id>
Delete a actor from the db.
##### Response:
```
{
    "actors": [
        {
            "age": 20,
            "gender": "Male",
            "id": 1,
            "name": "Will smith"
        }
    ],
    "deleted": 2,
    "success": true,
    "total_actors": 1
}
```
#### GET /movies/<movie_id>/actors
Gets actors by movie
##### Response:
```
{
    "actors": {
        "1": {
            "age": 25,
            "gender": "Male",
            "id": 1,
            "name": "Will smith"
        }
    },
    "success": true,
    "total_actors_by_movie": 1
}
```
# Authentification
The API has three registered users:
1. Assistant:
```
email: assistant@agency.com
password: Assistant2
```
2. Director
```
email: director@agency.com
password: Director2
```
3. Producer
```
email: producer@agency.com
password: Producer2
```
All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 
## Auth0 for locally use
### Create an App & API
1.	Login to https://manage.auth0.com/
2.	Click on Applications Tab
3.	Create Application
4.	Give it a name and select "Regular Web Application"
5.	Go to Settings and find domain. Copy & paste it into config.py => AUTH0_DOMAIN
6.	Click on API Tab
7.	Create a new API:
8.	Go to Settings and find Identifier. Copy & paste it into config.py => API_AUDIENCE
### Create Roles & Permissions
1.	Before creating Roles & Permissions, you need to Enable RBAC in your API 
2.	Also, check the button Add Permissions in the Access Token.
3.	First, create a new Role under Users and Roles => Roles => Create Roles
4.	Give it a descriptive name like Casting Assistant.
5.	Go back to the API Tab and find your newly created API. Click on Permissions.
6.	Create & assign all needed permissions accordingly
7.	After you created all permissions this app needs, go back to Users and Roles => Roles and select the role you recently created.
8.	Under Permissions, assign all permissions you want this role to have.
### Auth0 to use existing API
If you want to access the real, temporary API, bearer tokens for all 3 roles are included in the config.py file.
# Existing Roles
They are 3 Roles with distinct permission sets:
##### Casting Assistant
* Can view actors and movies
##### Casting Director
* All permissions a Casting Assistant has and…
* Add or delete an actor from the database
* Modify actors or movies
##### Executive Producer
* All permissions a Casting Director has and…
* Add or delete a movie from the database
# Tests
To run the tests, run python3 test_app.py.