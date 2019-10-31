from flask import render_template, session, request

from route_helper import simple_route

GAME_HEADER = """
"""
name = """
"""
def subtract_attempt(world:dict)-> str:
    """
    Subtracts one from the current amount of attempts stored in the world dictionary
    :param world:
    :return: world:
    """
    for item in world:
        if item["name"] == "quiz attempts":
            o_attempts = item["attempts"]
            n_attempts = o_attempts - 1
            item["attempts"] = n_attempts
        return world

def attempt_check(world:dict)-> str:
    """
    :param world:
    :return: bool:
    """
    for item in world:
        if item["name"] == "quiz attempts" and item["attempts"] == 0:
            return True
    return False

@simple_route('/')
def hello(world: dict) -> str:
    """
    Initial view: Outside the Haunted House
    :param world:
    :return: index.html: world
    """
    return render_template("index.html", world=world)


@simple_route('/room_1/')
def house(world: dict) -> str:
    """
    First room of the witch's lair
    :param world:
    :return: Witch_lair.html: world
    """
    return render_template("Witch_lair.html", world = world)


@simple_route('/witch/')
def witch(world: dict) -> str:
    """
    Witch appears, option to take witch's quiz
    :param world:
    :return: Witch.html, world
    """
    return render_template("Witch.html", world = world)

@simple_route("/witch_hat/")
def hat(world: dict) -> str:
    """
    Witch's Quiz, subtracts 1 from total attempts remaining
    :param world:
    :return: Witch_hat.html: world
    """
    subtract_attempt(world)
    return render_template("Witch_hat.html", world = world)

@simple_route("/save_witch/")
def witch_save(world: dict, *args)->str:
    """
    Saves witch's quiz information. Determines if the user passed the quiz or not.
    :param world:
    :param args:
    :return: witch-win.html: witch_lose.html: world
    """

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
    """
    Checks if the player is out of attempts. Option to take skeleton quiz.
    :param world:
    :param args:
    :return: out_attempts.html: skeleton_room.html: world
    """
    if attempt_check(world):
        return render_template("out_attempts.html", world=world)
    return render_template("skeleton_room.html", world = world)


@simple_route("/skeleton_party/")
def dance_party(world:dict, *args) -> str:
    """
    Skeleton's quiz page, removes 1 from total attempts
    :param world:
    :param args:
    :return: skeleton_party.html world
    """
    subtract_attempt(world)
    return render_template("skeleton_party.html", world = world)


@simple_route("/save_skeleton/")
def save_skeleton(world:dict, *args) -> str:
    """
    Saves skeleton quiz information. Determine if player passed the quiz or not
    :param world:
    :param args:
    :return: skeleton_win.html: skeleton_lose.html: world
    """
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
    """
    Checks if the user is out of attempts
    :param world:
    :return: out_attempts.html: Vampire_coffin.html: world
    """
    for item in world:
        if item["name"] == "cape" and item["own"] == False:
            if attempt_check(world):
                return render_template("out_attempts.html", world=world)
    return render_template("Vampire_coffin.html", world = world)


@simple_route("/vampire/")
def vampire(world:dict, *args) -> str:
    """
    Vampire's quiz, calls subtract_attempt()
    :param world:
    :param args:
    :return: Vampire.html: world = world
    """
    subtract_attempt(world)
    return render_template("Vampire.html", world = world)


@simple_route("/save_vampire/")
def save_vampire(world:dict, *args) -> str:
    """
    Saves vampire quiz answers. Determines if the user passed the quiz or not.
    :param world:
    :param args:
    :return:
    """
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
    """
    Renders door.html template
    :param world:
    :return: Door.html: world
    """
    return render_template("Door.html", world = world)


@simple_route("/ghost/")
def ghost(world:dict) -> str:
    """
    Renders ghost template
    :param world:
    :return:
    """
    return render_template("Ghost.html", world = world)


@simple_route("/exit/")
def exit(world:dict, *args) -> str:
    """
    Determines how many prizes the user collected, displays the right award for the items collected
    :param world:
    :param args:
    :return: collect_all.html: Not_enough.html: hat_cape_win.html: hat_hand_win.html: cape_hand_win.html: world
    """
    final_items = []
    for item in world:
        bool_test = item.get("own")
        if bool_test:
            final_items.append(item["name"])
    if len(final_items) == 3:
        return render_template("collect_all.html", world = world)
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
    """
    Displays all the users final answers and correct answers in a table
    :param world:
    :param args:
    :return: result_table.html: world
    """
    return render_template("result_table.html", world =world)



