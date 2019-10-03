from route_helper import simple_route

GAME_HEADER = """
<h1>Welcome to the Haunted House!</h1>
<p>At any time you can <a href='/reset/'>exit</a> the house if you get too scared!</p>
"""


@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    return GAME_HEADER+"""You are in front of the haunted house.<br>
    <img src='/static/house_front.png'><br>
    <a href="/room_1/">Click here if you dare to enter</a><br>
"""

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
def house(world:dict)->str:
    return """
    <img src='/static/witch_lair.jpg'><br>
    <a href="/witch/">Do you want to keep investigating the room?</a><br>
    <a href="/room_2/">Do you want to move into the next room?</a>
"""

@simple_route('/witch/')
def witch(world:dict)->str:
    return """
    <h1> The Witch has appeared!<h1><br>
    <img src='/static/witch.jpg'><br>
    <a href="/room_2/">Quick run away!</a>
    """

@simple_route('/room_2/')
def room_2(world:dict)->str:
    return """"
    <h1>You've interrupted the skeletons' dance party!</h1><br>
    <img src='/static/dancing_skeletons.gif'><br>
    """

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
