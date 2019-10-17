from flask import render_template, session, request

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
    return render_template("index.html", world = world)
    

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
    return render_template("Witch_lair.html", world = world)


@simple_route('/witch/')
def witch(world: dict) -> str:
    return render_template("Witch.html", world = world)

@simple_route("/witch_hat/")
def hat(world: dict) -> str:
    for item in world:
        if item["name"] == "inventory spaces":
            o_spots = item.get("spots")
            n_spots = o_spots - 1
            item["spots"] = n_spots
    for item in world:
        if item["name"] == "hat":
            item["own"] = True
    return render_template("witch_hat.html", world = world)

@simple_route("/save_witch/")
def witch_save(world: dict, *args)->str:
    color = request.values.get("c_value")
    for item in world:
        if item["name"] == "hat":
            item["color"] = color
    print(request.form)
    return render_template("skeleton_room.html", world = world)


@simple_route('/skeleton_room/')
def room_2(world:dict) -> str:
    return render_template("skeleton_room.html", world = world)


@simple_route("/skeleton_party/")
def dance_party(world:dict) -> str:
    for item in world:
        if item["name"] == "inventory spaces":
            o_spots = item.get('spots')
            n_spots = o_spots - 1
            item["spots"] = n_spots
    for item in world:
        if item["name"] == "hand":
            item["own"] = True
    return render_template("skeleton_party.html", world = world)


@simple_route("/vampire_coffin/")
def vampire_coffin(world:dict) -> str:
    return render_template("Vampire_coffin.html", world = world)


@simple_route("/vampire/")
def vampire(world:dict) -> str:
    for item in world:
        if item["name"] == "inventory spaces":
            o_spots = item.get("spots")
            n_spots = o_spots - 1
            item["spots"] = n_spots
    for item in world:
        if item["name"] == "cape":
            item["own"] = True
    return render_template("Vampire.html", world = world)


@simple_route("/door/")
def door(world:dict) -> str:
    return render_template("Door.html", world = world)


@simple_route("/ghost/")
def ghost(world:dict) -> str:
    return render_template("Ghost.html", world = world)

@simple_route("/exit/")
def exit(world:dict) -> str:
    final_items = []
    for item in world:
        bool_test = item.get("own")
        if bool_test:
            final_items.append(item["name"])
    if len(final_items) < 2:
        return render_template("Not_enough.html")
    if "hat" in final_items and "cape" in final_items:
        return render_template("hat_cape_win.html")
    elif "hat" in final_items and "hand" in final_items:
        return render_template("hat_hand_win.html")
    elif "cape" in final_items and "hand" in final_items:
        return render_template("cape_hand_win.html")

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
