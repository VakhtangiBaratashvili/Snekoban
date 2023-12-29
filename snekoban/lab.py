"""
6.1010 Lab 4: 
Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board.

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.

    Parameters:
    - level_description (list): A list of lists of lists of strs, representing the
      locations of the objects on the board.

    Returns:
    - dict: A dictionary representing the game state.
    """

    # ლექსიკონის ინიცირება თამაშის მდგომარეობის შესანახად
    dct_representation = {
        "target": set(),  # სამიზნე პოზიციები
        "computer": set(),  # კომპიუტერის პოზიცია
        "wall": set(),  # კედლის პოზიცია
    }

    # იტერაცია თითოეული სტრიქონზე level_description-ში
    for row_num, row in enumerate(level_description):
        # იტერაზია მიმდინარე მწკრივის თითოეული სვეტიზე
        for col_num, block in enumerate(row):

            # შემოწმება არის თუ არა მოთამაშე მიმდინარე ბლოკში
            if "player" in block:
                # მოთამაშის პოზიციის ლექსიკონში შენახვა
                dct_representation["player"] = (row_num, col_num)

            # შემოწმება არის თუ არა სამიზნე მიმდინარე ბლოკში
            if "target" in block:
                # სამიზნე პოზიციის დამატება ნაკრებში
                dct_representation["target"].add((row_num, col_num))

            # შემოწმება არის თუ არა კომპიუტერი მიმდინარე ბლოკში
            if "computer" in block:
                # კომპიუტერის პოზიციის დამატება კომპლექტში
                dct_representation["computer"].add((row_num, col_num))

            # შემოწმება არის თუ არა კედელი მიმდინარე ბლოკში
            if "wall" in block:
                # კედლის პოზიციის დამატება კომპლექტში
                dct_representation["wall"].add((row_num, col_num))

    # თამაშის დაფაზე რიგებისა და სვეტების რაოდენობის შენახვა
    dct_representation["row_num_stored"] = row_num + 1
    dct_representation["col_num_stored"] = col_num + 1

    # ფინალური თამაშის მდგომარეობის დაბრუნება
    return dct_representation


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.

    Parameters:
    - game (dict): A dictionary representing the game state.

    Returns:
    - bool: True if the game satisfies the victory condition, False otherwise.
    """

    # დარჩენილი სამიზნეების შემოწმება
    if len(game["target"]) == 0:
        return False

    # არის თუ არა დარჩენილი სამიზნეების რაოდენობა კომპიუტერების რაოდენობაზე მეტის შემოწმება
    if len(game["target"]) > len(game["computer"]):
        return False

    # ყველა კომპიუტერი სამიზნე პოზიციებზე ყოფნის შემოწმება
    for item in game["computer"]:
        if item not in game["target"]:
            return False

    # გამარჯვების ყველა პირობა დაკმაყოფილებულია
    return True


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game. The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.

    Parameters:
    - game (dict): A dictionary representing the current game state.
    - direction (str): The direction in which the player wants to move ('up', 'down', 'left', 'right').

    Returns:
    - dict: A new dictionary representing the updated game state after one step of the game.
    """

    # კომპიუტერის ნაკრების ასლის შექმნა შეყვანის მუტაციის თავიდან ასაცილებლად
    new_computer_set = game["computer"].copy()

    # მოთამაშის მიმდინარე პოზიციის მიღება
    player_r, player_c = game["player"]

    # მოძრაობის ვექტორის მიღება მიმართულებიდან გამომდინარე
    drow, dcol = direction_vector[direction]

    # ახალი მოთამაშის პოზიციის გამოთვლა
    r, c = player_r + drow, player_c + dcol

    # შემდეგი პოზიციის გამოთვლა ახალი მოთამაშის პოზიციის შემდეგ
    r2, c2 = r + drow, c + dcol

    # გაანგარიშება არის თუ არა ახალი პოზიცია კედელი და თუ ასეა, დააბრუნეთ თამაშის მიმდინარე მდგომარეობა
    if (r, c) in game["wall"]:
        return game

    # გამოთვლა აქვს თუ არა ახალ პოზიციას კომპიუტერი
    if (r, c) in game["computer"]:
        # შემოწმება ახალი მოთამაშის პოზიციის შემდეგ შემდეგი პოზიცია ცარიელია თუ აქვს სხვა კომპიუტერი
        if (r2, c2) in game["computer"] or (r2, c2) in game["wall"]:
            return game

        # მოთამაშის პოზიციის განახლება და კომპიუტერის შემდეგ პოზიციაზე გადატანა
        new_player = (r, c)
        new_computer_set.remove((r, c))
        new_computer_set.add((r2, c2))

        # თამაშის განახლებული მდგომარეობის დაბრუნება
        return {
            "player": new_player,
            "target": game["target"],
            "computer": new_computer_set,
            "wall": game["wall"],
            "row_num_stored": game["row_num_stored"],
            "col_num_stored": game["col_num_stored"],
        }

    # თუ ახალ პოზიციას არ აქვს კომპიუტერი, მოთამაშის პოზიციის განახლება
    return {
        "player": (r, c),
        "target": game["target"],
        "computer": game["computer"],
        "wall": game["wall"],
        "row_num_stored": game["row_num_stored"],
        "col_num_stored": game["col_num_stored"],
    }


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.

    Parameters:
    - game (dict): A dictionary representing the current game state.

    Returns:
    - list: A list of lists of lists of strings, suitable as input to new_game.
    """

    # ცარიელი სიის შექმნა თამაშის მდგომარეობის გამოსაჩენად
    game_to_return = []

    # იტერაცია თამაშის რიგის თითოეულ მწკრივზე
    for row in range(game["row_num_stored"]):
        game_to_return.append([])

        # იტერაცია მიმდინარე მწკრივის თითოეულ სვეტზე
        for col in range(game["col_num_stored"]):
            game_to_return[row].append([])

    # კომპიუტერების დამატება თამაშის მდგომარეობის სიაში
    for tup in game["computer"]:
        row = tup[0]
        col = tup[1]
        game_to_return[row][col].append("computer")

    # მიზნების დამატება თამაშის მდგომარეობის სიაში
    for tup in game["target"]:
        row = tup[0]
        col = tup[1]
        game_to_return[row][col].append("target")

    # მოთამაშის დამატება თამაშის მდგომარეობის სიაში
    player_tup = game["player"]
    game_to_return[player_tup[0]][player_tup[1]].append("player")

    # კედლების დამატება თამაშის მდგომარეობის სიაში
    for tup in game["wall"]:
        row = tup[0]
        col = tup[1]
        game_to_return[row][col].append("wall")

    # ფინალური თამაშის მდგომარეობის დაბრუნება
    return game_to_return


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.

    Parameters:
    - game (dict): A dictionary representing the current game state.

    Returns:
    - list or None: A list of strings representing the shortest sequence of moves if the level is solvable,
      or None if the level cannot be solved.
    """

    # დუბლიკატების თავიდან აცილების მიზნით მცდელობის ბილიკების შესანახად set-ის დაყენება
    attempted_paths = set()

    # კანდიდატის ბილიკების სია, ინიციალიზებული საწყისი მდგომარეობით
    candidate_paths = [([], game)]

    while candidate_paths:

        # შესაძლო სვლები პრიორიტეტის მიხედვით
        moves = ["left", "right", "up", "down"]

        # შემდეგი გზის მიღება კანდიდატის ბილიკებიდან
        path = candidate_paths.pop(0)

        # შემოწმება, შესრულებულია თუ არა გამარჯვების პირობა
        if victory_check(path[1]):
            return path[0]

        # მიმდინარე თამაშის მდგომარეობის hashable რეპრეზენტაციის შექმნა
        game_state = (path[1]["player"], frozenset(path[1]["computer"]))

        # თამაშის მიმდინარე მდგომარეობის attempted_paths-ში არსებობის შემოწმება
        if game_state not in attempted_paths:
            attempted_paths.add(game_state)

            # შესაძლო ნაბიჯები შესწავლა და მათი candidate_paths-ში დამატება
            for move in moves:
                candidate_paths.append((path[0] + [move], step_game(path[1], move)))

    # სოლუშენი არ არსებობს
    return None


if __name__ == "__main__":
    pass
