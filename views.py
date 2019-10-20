from flask import render_template, session, request

from route_helper import simple_route

GAME_HEADER = """
"""
name = """
"""
def subtract_attempt(world:dict)-> str:
    for item in world:
        if item["name"] == "quiz attempts":
            o_attempts = item["attempts"]
            n_attempts = o_attempts - 1
            item["attempts"] = n_attempts
        return world

def attempt_check(world:dict)-> str:
    for item in world:
        if item["name"] == "quiz attempts" and item["attempts"] == 0:
            return True
    return False

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
    subtract_attempt(world)
    return render_template("witch_hat.html", world = world)

@simple_route("/save_witch/")
def witch_save(world: dict, *args)->str:
    q1 = request.values.get("question_1")
    q2 = request.values.get("question_2")
    q3 = request.values.get("question_3")
    for item in world:
        if item["name"] == "witch quiz":
            item["question 1"] = q1
            item["question 2"] = q2
            item["question 3"] = q3
    for item in world:
        if item["name"] == "witch answers":
            if q1 == item["answer 1"] and q2 == item["answer 2"] and q3 == item["answer 3"]:
                for item in world:
                    if item["name"] == "hat":
                        item["own"] = True
                return render_template("witch_win.html", world = world)
            else:
                return render_template("witch_lose.html", world = world)


@simple_route('/skeleton_room/')
def room_2(world:dict, *args) -> str:
    if attempt_check(world):
        return render_template("out_attempts.html", world=world)
    return render_template("skeleton_room.html", world = world)


@simple_route("/skeleton_party/")
def dance_party(world:dict, *args) -> str:
    subtract_attempt(world)
    return render_template("skeleton_party.html", world = world)

@simple_route("/save_skeleton/")
def save_skeleton(world:dict, *args) -> str:
    q1 = request.values.get("question_1")
    q2 = request.values.get("question_2")
    q3 = request.values.get("question_3")
    for item in world:
        if item["name"] == "skeleton quiz":
            item["question 1"] = q1
            item["question 2"] = q2
            item["question 3"] = q3
    for item in world:
        if item["name"] == "skeleton answers":
            if q1 == item["answer 1"] and q2 == item["answer 2"] and q3 == item["answer 3"]:
                for item in world:
                    if item["name"] == "hand":
                        item["own"] = True
                return render_template("skeleton_win.html",world = world)
            else:
                return render_template("skeleton_lose.html", world = world)




@simple_route("/vampire_coffin/")
def vampire_coffin(world:dict) -> str:
    for item in world:
        if item["name"] == "cape" and item["own"] == False:
            if attempt_check(world):
                return render_template("out_attempts.html", world=world)
    return render_template("Vampire_coffin.html", world = world)


@simple_route("/vampire/")
def vampire(world:dict, *args) -> str:
    subtract_attempt(world)
    return render_template("Vampire.html", world = world)

@simple_route("/save_vampire/")
def save_vampire(world:dict, *args) -> str:
    q1 = request.values.get("question_1")
    q2 = request.values.get("question_2")
    q3 = request.values.get("question_3")
    for item in world:
        if item["name"] == "vampire quiz":
            item["question 1"] = q1
            item["question 2"] = q2
            item["question 3"] = q3
    for item in world:
        if item["name"] == "vampire answers":
            if q1 == item["answer 1"] and q2 == item["answer 2"] and q3 == item["answer 3"]:
                for item in world:
                    if item["name"] == "cape":
                        item["own"] = True
                return render_template("vampire_win.html", world = world)
            else:
                return render_template("vampire_lose.html", world = world)

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
    if len(final_items) == 3:
        return render_template("collect_all.html")
    if len(final_items) < 2:
        return render_template("Not_enough.html",world = world )
    if "hat" in final_items and "cape" in final_items:
        return render_template("hat_cape_win.html", world = world)
    elif "hat" in final_items and "hand" in final_items:
        return render_template("hat_hand_win.html", world = world )
    elif "cape" in final_items and "hand" in final_items:
        return render_template("cape_hand_win.html", world = world )
@simple_route("/result_table/")
def results(world:dict, *args)-> str:
    return render_template("result_table.html", world =world)

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
