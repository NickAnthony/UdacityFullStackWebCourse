# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

### Authenticate with Auth0

- https://fsnd-app-nickanthony.us.auth0.com/authorize?audience=coffeeshop&response_type=token&client_id=Hr477pZ0drtdCl05L8YthbHShnddXhCi&redirect_uri=https://127.0.0.1:8080/login-results

Manager JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh6Z3Z4U3lDNm9fU0t4c25nSnR0ZiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYXBwLW5pY2thbnRob255LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDBkMDQ0OGZmY2JlMjAwNmE4ODY2MWUiLCJhdWQiOiJjb2ZmZWVzaG9wIiwiaWF0IjoxNjExNTM2ODc0LCJleHAiOjE2MTE1NDQwNzQsImF6cCI6IkhyNDc3cFowZHJ0ZENsMDVMOFl0aGJIU2huZGRYaENpIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.XpKu7bbhLdAePuZBOuGNwTS1qkg2Ol1eYNjZ92HDg5RdJwo1VdekR0z3NtJt9B0FmXEPWHyRN3I1wfhMX9DiZ2rkLhxcIN456LLHKllH5nEjcT0gCtuxK9zmnFEdBG_ND0cOdYqpc31AsSmGB7APPHscRTdMqw_Jws0qamJk--mWzbBJkwJ8dt9k5wv-id9NLh_1zB6O7SyjwVGcPOAJEjyek82MMr6jVYucRg6VP2S1rW4VaisMWuvUgA-WbrBYFHjDaFX_wfm9ayWfQRA_LJjIL_6zzQo3Jm5JRBwV_tyOOjMI71PAzvBdJGejTS_AXyMIkK0PPd16WhBviZlMcQ
