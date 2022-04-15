import numpy as np
from copy import deepcopy

from src.logic.state import move


class MCTSNode:
    """ Node representation for the Monte Carlo Tree Search Algorithm """

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.t = 0  # no. of wins
        self.n = 0  # no. of visits
        self.children = None

    def ucb1(self, c=2):
        if self.n == 0:
            return np.inf

        root = self.get_root()
        return (self.t / self.n) + c * np.sqrt(np.log(root.n) / self.n)

    def get_root(self):
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
            self.children[i] = MCTSNode(move(child, action), self)

    def best_child(self):
        values = np.empty(shape=self.children.shape[0], dtype=np.float32)
        for i, child in enumerate(self.children):
            values[i] = child.ucb1()

        return self.children[np.argmax(values)]

    def simulate(self):
        game = deepcopy(self.state)

        while True:
            is_over, winner = game.is_over()
            if is_over:
                return int(winner == self.get_root().state.curr_player)

            actions = game.actions()
            random_move = np.random.randint(0, actions.shape[0], dtype=np.uint8)
            game = move(game, actions[random_move])

    def propagate(self, value):
        self.t += value
        self.n += 1

        p = self.parent
        while p is not None:
            p.t += value
            p.n += 1
            p = p.parent


def mcts(game, iterations=1000):
    """
    A very basic Monte Carlo Tree Search Algorithm Implementation
    ---
    :param game: Current game state
    :param iterations: Number of iterations to run the algorithm
    :return: Most promising move according to the algorith
    """

    root = MCTSNode(game)
    for _ in range(iterations):
        current = root

        # Selection
        while current.is_expanded():
            current = current.best_child()

        # Expansion
        if current.n:
            current.expand()
            current = current.best_child()

        # Simulation and back propagation
        value = current.simulate()
        current.propagate(value)

    return root.best_child().state.last_move
