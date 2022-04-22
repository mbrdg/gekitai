import numpy as np
from copy import deepcopy

from src.logic.state import GameState
from src.logic.operators import move


class MCTSNode:
    """ Node representation for the Monte Carlo Tree Search Algorithm """

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = None
        self.wins = 0
        self.visits = 0

    def ucb1(self, ci):
        if self.visits == 0:
            return np.inf

        root = self.root()
        return (self.wins / self.visits) + ci * np.sqrt(np.log(root.visits) / self.visits)

    def root(self):
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def is_expanded(self):
        return self.children is not None

    def expand(self):
        actions = self.state.actions()
        self.children = np.empty(shape=actions.shape[0], dtype=MCTSNode)

        for i, action in enumerate(actions):
            child = deepcopy(self.state)
            self.children[i] = MCTSNode(move(child, action), parent=self)

    def best_child(self, ci):
        values = np.empty(shape=self.children.shape[0], dtype=np.float32)
        for i, child in enumerate(self.children):
            values[i] = child.ucb1(ci)

        return self.children[np.argmax(values)]

    def simulate(self):
        game = deepcopy(self.state)

        while True:
            is_over, winner = game.is_over()
            if is_over:
                return int(winner == self.root().state.curr_player)

            actions = game.actions()
            random_move = np.random.randint(0, actions.shape[0], dtype=np.uint8)
            game = move(game, actions[random_move])

    def propagate(self, value):
        self.wins += value
        self.visits += 1

        p = self.parent
        while p is not None:
            p.wins += value
            p.visits += 1
            p = p.parent


def mcts(game: GameState, *, iterations=1024, ci=2.0):
    """
    A very basic Monte Carlo Tree Search Algorithm Implementation
    The value of the nodes is based in wins and visits ratio
    ---
    :param game: Current game state
    :param iterations: Number of iterations to run the algorithm
    :param ci: Exploration parameter for UCB1
    :return: Most promising move according to the algorith
    """

    root = MCTSNode(game)
    for _ in range(iterations):
        current = root

        # Selection
        while current.is_expanded():
            current = current.best_child(ci)

        # Expansion
        if current.visits > 0:
            current.expand()
            current = current.best_child(ci)

        # Simulation and back propagation
        value = current.simulate()
        current.propagate(value)

    return root.best_child(ci).state.last_move
