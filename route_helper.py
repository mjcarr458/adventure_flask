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
    #Dict 0
    {"name": "quiz attempts", "attempts": 3},
    #Dict 1
    {"name": "cape", "own": False},
    #Dict 2
    {"name": "hat", "own": False},
    #Dict 3
    {"name": "hand", "own": False},
    #Dict 4
    {"name": "witch quiz", "question 1": None,"question 2": None, "question 3": None},
    #Dict 5
    {"name": "skeleton quiz", "question 1": None, "question 2" : None, "question 3": None},
    #Dict 6
    {"name": "vampire quiz", "question 1": None, "question 2": None, "question 3": None},
    #Dict 7
    {"name": "witch answers", "answer 1": "Their bats flew away!", "answer 2": "Broom mates!", "answer 3": "A broom-erang!"},
    #Dict 8
    {"name": "skeleton answers", "answer 1": "Because they don't have any guts!", "answer 2": "Sherlock Bones!","answer 3": "Spare 'ribs'!"},
   #Dict 9
    {"name": "vampire answers", "answer 1": "'Blood' hound!", "answer 2": "Love at first 'byte'!", "answer 3": "Because his Bach was worse than his bite!"},
    #Dict 10
    {"name": "witch questions",
     "question 1": "Why did they witches' team lose the baseball game?",
     "question 2": "What do you call two witches who live together?",
     "question 3": "What do witches in Australia ride?"},
    #Dict 11
    {"name": "skeleton questions",
     "question 1": "Why aren't skeletons brave?",
     "question 2": "Who was the most famous skeleton detective?",
     "question 3": "What is a skeleton's favorite food?"},
    #Dict 12
    {"name": "vampire questions",
     "question 1": "What's a vampire's favorite type of dog?",
     "question 2": "What do you get if you cross a vampire with a laptop?",
     "question 3": "Why did the vampire torture his victims with music?"
     }
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

