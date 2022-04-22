import sys


def start():
    print(f"\nWelcome to the gekitai game")
    print(f"This is part of the first project from the IA course of LEIC@FEUP")

    print(f"\nMain menu")
    print(f"[1] Play\n"
          f"[2] Rules\n"
          f"Press any other key to exit...")

    option = int(input('> '))
    if option not in range(1, 3):
        sys.exit(0)

    if option == 2:
        rules()
        sys.exit(0)

    if option == 1:
        return _play()


def rules():
    print("\nGekitai™ (Repel or Push Away) is a 3-in-a-row game played on a 6x6 grid.\n\n"
          "Each player has eight colored markers and takes turns placing them anywhere\n"
          "on any open space on the board.When placed, a marker pushes all adjacent pieces\n"
          "outwards one space if there is an open space for it to move to (or off the board).\n\n"
          "Pieces shoved off the board are returned to the player.\n"
          "If there is not an open space on the opposite side of the pushed piece,\n"
          "it does not push (a newly played piece cannot push two or more other lined-up pieces).\n\n"
          "The first player to either line up three of their color in a row at the end of their\n"
          "turn (after pushing) OR have all eight of their markers on the board (also after pushing) wins.")


def _play():
    print(f"\nPlay menu")
    print(f"[1] Player vs. PLayer\n"
          f"[2] Player vs. Computer\n"
          f"[3] Computer vs. Player\n"
          f"[4] Computer vs. Computer\n"
          f"Press any other key to exit...")

    option = int(input('>> '))
    if option not in range(1, 5):
        sys.exit(0)

    p1, p2 = dict(), dict()
    if option == 1:
        p1['is_pc'] = p2['is_pc'] = False
    elif option == 2:
        p1['is_pc'], p2['is_pc'] = False, True
    elif option == 3:
        p1['is_pc'], p2['is_pc'] = True, False
    elif option == 4:
        p1['is_pc'] = p2['is_pc'] = True

    return _algorithm_selection(p1, p2)


def _algorithm_selection(p1, p2):

    def algo(p):
        print(f"\nChoose the algorithm for player {p}:")
        print(f"[1] Minimax (Default)\n"
              f"[2] Monte Carlo Tree Search")

        option = int(input('>>> '))
        return 'Minimax' if not (option - 1) else 'MCTS'

    p1['algo'], p2['algo'] = algo(1), algo(2)
    return p1, p2
