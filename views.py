from flask import render_template, session

from route_helper import simple_route

GAME_HEADER = """
"""
name = """
"""


@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    return render_template("index.html")
    

ENCOUNTER_MONSTER = """
<!-- Curly braces let us inject values into the string -->
You are in {}. You found a monster!<br>

<!-- Image taken from site that generates random Corgi pictures-->
<img src="http://placecorgi.com/260/180" /><br>
    
What is its name?

<!-- Form allows you to have more text entry -->    
<form action="/save/name/">
    <input type="text" name="player"><br>
    <input type="submit" value="Submit"><br>
</form>
"""


@simple_route('/room_1/')
def house(world:dict) -> str:
    return render_template("Game_header.html",world = world) + render_template("Witch_lair.html")


@simple_route('/witch/')
def witch(world: dict) -> str:
    return render_template("Game_header.html",world = world) + render_template("Witch.html")


@simple_route('/skeleton_room/')
def room_2(world:dict) -> str:
    return render_template("Game_header.html",world = world ) + render_template("skeleton_room.html")


@simple_route("/skeleton_party/")
def dance_party(world:dict) -> str:
    return render_template("Game_header.html",world = world) + render_template("skeleton_party.html")


@simple_route("/vampire_coffin/")
def vampire_coffin(world:dict) -> str:
    return render_template("Game_header.html",world = world) + render_template("Vampire_coffin.html")


@simple_route("/vampire/")
def vampire(world:dict) -> str:
    world["cape"] = True
    print(world)
    return render_template("Game_header.html", world = world) + render_template("Vampire.html")


@simple_route("/door/")
def door(world:dict) -> str:
    return render_template("Game_header.html", world=world) + render_template("Door.html")


@simple_route("/ghost/")
def ghost(world:dict) -> str:
    return render_template("Game_header.html", world = world) + render_template("Ghost.html")

@simple_route("/exit/")
def exit(world:dict) -> str:
    return render_template("Game_header.html", world = world) + render_template("Exit.html")

@simple_route('/goto/<where>/')
def open_door(world: dict, where: str) -> str:
    """
    Update the player location and encounter a monster, prompting the player
    to give them a name.

    :param world: The current world
    :param where: The new location to move to
    :return: The HTML to show the player
    """
    world['location'] = where
    return GAME_HEADER+ENCOUNTER_MONSTER.format(where)


@simple_route("/save/name/")
def save_name(world: dict, monsters_name: str) -> str:
    """
    Update the name of the monster.

    :param world: The current world
    :param monsters_name:
    :return:
    """
    world['name'] = monsters_name

    return GAME_HEADER+"""You are in {where}, and you are nearby {monster_name}
    <br><br>
    <a href='/'>Return to the start</a>
    """.format(where=world['location'], monster_name=world['name'])
