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
# db_drop_and_create_all()

# UTILS


def format_drinks_short(drinks):
    return [drink.short() for drink in drinks]


def format_drinks_long(drinks):
    return [drink.long() for drink in drinks]


# ROUTES


'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where
        drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
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
    returns status code 200 and json {"success": True, "drinks": drinks} where
        drinks is the list of drinks
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
    returns status code 200 and json {"success": True, "drinks": drink} where
        drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    if not request.get_json():
        abort(400)
    title = request.get_json().get('title', None)
    recipe = request.get_json().get('recipe', [])

    # Verify that the title and recipe exist
    if (not title or not recipe):
        abort(400)
    # Verify recipe works
    for piece in recipe:
        if 'name' not in piece or 'parts' not in piece or 'color' not in piece:
            abort(400)
        if piece['parts'] < 1:
            abort(400)
    # Ensure that the title is unique
    if Drink.query.filter(Drink.title == title).one_or_none():
        abort(400)

    try:
        new_drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )
        new_drink.insert()
        # We can get the id of the new_drink because it has been flushed.
        return jsonify({
            'success': True,
            'id': new_drink.id,
            'drinks': format_drinks_long([new_drink])
        })
    except for Exception as e:
        abort(422)


'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where
        drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def modify_exiting_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        abort(404)

    # Verify that either one of title and recipe exist
    if (not request.get_json().get('title') and
            not request.get_json().get('recipe')):
        abort(400)

    title = request.get_json().get('title', drink.title)
    recipe = request.get_json().get('recipe', json.loads(drink.recipe))
    # Verify recipe works
    for piece in recipe:
        if 'name' not in piece or 'parts' not in piece or 'color' not in piece:
            abort(400)
        if piece['parts'] < 1:
            abort(400)

    try:
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        # We can get the id of the new_drink because it has been flushed.
        return jsonify({
            'success': True,
            'id': drink.id,
            'drinks': format_drinks_long([drink])
        })
    except for Exception as e:
        abort(422)


'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id
        is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink_to_delete = Drink.query.get(drink_id)
    if not drink_to_delete:
        abort(404)
    try:
        drink_to_delete_id = drink_to_delete.id
        drink_to_delete.delete()
        return jsonify({
            'success': True,
            'delete': drink_to_delete_id
        })
    except for Exception as e:
        abort(422)


# Error Handling
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
    return jsonify({
        "success": False,
        "error": e.error['code'],
        "code": e.status_code,
        "message": e.error['description'],
    }), e.status_code
