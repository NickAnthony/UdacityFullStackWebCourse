import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## UTILS

def format_drinks_short(drinks):
    return [drink.short() for drink in drinks]
def format_drinks_long(drinks):
    return [drink.long() for drink in drinks]

## ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks(payload):
    drinks = Drink.query.all()
    # If there are no drinks, throw a 404
    if not drinks:
        abort(404)
    return jsonify({
                'success': True,
                'drinks': format_drinks_short(drinks)
            })

'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    drinks = Drink.query.all()
    # If there are no drinks, throw a 404
    if not drinks:
        abort(404)
    return jsonify({
                'success': True,
                'drinks': format_drinks_long(drinks)
            })

'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    # Json payload is of the format:
    # { "title": title.
    #   "recipe": [{
    #     "name": name (string),
    #     "parts": parts (number),
    #     "color": color (string)
    #   },]}
    title = request.get_json().get('title', None)
    recipe = request.get_json().get('recipe', []])

    # Verify that the title and recipe exist
    if (title is None or
        len(recipe) == 0):
        abort(400)

    try:
        # Verify recipe works.  Do so in a try/catch in case of key errors
        for piece in recipe:
            if not piece['name'] or not piece['parts'] or not piece['color']:
                abort(400)
            if piece['parts'] < 1:
                abort(400)

        new_drink = Drink(
            title = title,
            recipe = recipe
        )
        new_drink.insert()
        # We can get the id of the new_drink because it has been flushed.
        return jsonify({
            'success': True,
            'id': new_drink.id,
            'drinks': format_drinks_long([new_drink])
        })
    except:
        abort(422)

'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def add_new_drink(drink_id):
    # Json payload is of the format:
    # { "title": title.
    #   "recipe": [{
    #     "name": name (string),
    #     "parts": parts (number),
    #     "color": color (string)
    #   },]}
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if not drink:
        abort(404)

    title = request.get_json().get('title', None)
    recipe = request.get_json().get('recipe', []])
    # Verify that the title and recipe exist
    if (title is None or
        len(recipe) == 0):
        abort(400)

    try:
        # Verify recipe works.  Do so in a try/catch in case of key errors
        for piece in recipe:
            if not piece['name'] or not piece['parts'] or not piece['color']:
                abort(400)
            if piece['parts'] < 1:
                abort(400)
        drink.title = title
        drink.recipe = recipe
        drink.update()
        # We can get the id of the new_drink because it has been flushed.
        return jsonify({
            'success': True,
            'id': new_drink.id,
            'drinks': format_drinks_long([drink])
        })
    except:
        abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

'''
@DONE implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource was not found"
    }), 404

@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method is not allowed"
    }), 405

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422

@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500



'''
@DONE implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_auth_error(e):
    # Get the original AuthError code
    original_error = e.get_response()
    return jsonify({
        "success": False,
        "error": original_error.code,
        "code": original_error.code,
        "message": original_error.description,
    }), original_error.code
