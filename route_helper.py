"""
The simple_route decorator allows us to quickly make routes that have proper
state being passed in and manipulated.

This file also establishes the reset route, with the idea that everyone
would like to be able to reset their game.
"""

import json
from functools import wraps

from flask import request, session, redirect

from app import app

INITIAL_WORLD = \
[
    {"name": "quiz attempts", "attempts": 3},
    {"name": "cape", "own": False},
    {"name": "hat", "own": False},
    {"name": "hand", "own": False},
    {"name": "witch quiz", "question 1": None,"question 2": None, "question 3": None},
    {"name": "skeleton quiz", "question 1": None, "question 2" : None, "question 3": None},
    {"name": "vampire quiz", "question 1": None, "question 2": None, "question 3": None},
    {"name": "witch answers", "answer 1": "Their bats flew away!", "answer 2": "Broom mates!", "answer 3": "A broom-erang!"},
    {"name": "skeleton answers", "answer 1": "Because they don't have any guts!", "answer 2": "Sherlock Bones!","answer 3": "Spare 'ribs'!"},
    {"name": "vampire answers", "answer 1": "'Blood' hound!", "answer 2": "Love at first 'byte'!", "answer 3": "Because his Bach was worse than his bite!"}


]



def simple_route(path: str, **options):
    """
    Creates a new route for the URL endpoint `path`. This decorator wraps
    the View endpoint to pass in the current `world` (deserialized from session data
    upon function entrance and serialized back into session once the function is
    done), any URL parameters, and then any request parameters (sorted by key name).

    :param path: The URL endpoint to use
    :type path: str
    :param options: Options to pass along to Flask's app.route. Usually you can ignore this.
    :return: Decorated function
    """
    def decorator(f):
        @app.route(path, **options)
        @wraps(f)
        def decorated_function(*args, **kwargs):
            world = json.loads(session.get('world', json.dumps(INITIAL_WORLD)))
            values = [v for k, v in sorted(request.values.items())]
            result = f(world, *args, *values, **kwargs)
            session['world'] = json.dumps(world)
            return result
        return decorated_function
    return decorator


@app.route("/reset/")
def reset():
    """
    Resets the game's world state (stored in session) and redirects to
    the root page.
    :return: Redirection to '/'
    """
    session['world'] = json.dumps(INITIAL_WORLD)
    return redirect('/')

