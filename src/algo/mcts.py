import numpy as np
from copy import deepcopy

from src.logic.state import move


class Node:

    C = 2  # Constant for calculating UCB1

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.t = 0
        self.n = 0
        self.children = None

    def ucb1(self):
        """Upper confidence value of a state -- UCB1"""
        if self.n == 0:
            return np.inf

        root = self.get_root()
        return (self.t / self.n) + Node.C * np.sqrt(np.log(root.n) / self.n)

    def get_root(self):
        node = self
        while node.parent is not None:
            node = self.parent
        return node

    def is_expanded(self):
        return bool(self.children)

    def expand(self):
        actions = self.state.actions()
        self.children = np.empty(shape=(1, len(actions)), dtype=object)

        for i, action in enumerate(actions):
            child = deepcopy(self.state)
            self.children[i] = Node(move(child, action), self)

    def best_child(self):
        values = np.empty(shape=self.children.shape, dtype=np.float32)
        for i, child in enumerate(self.children):
            values[i] = child.ucb1()

        return self.children[np.argmax(values)[0]]

    def rollout(self, evaluator):
        game = deepcopy(self.state)
        while not game.is_over():
            random_move = np.random.choice(game.actions(), size=1)
            game = move(game, random_move)
        return evaluator(game, is_over=True, is_max=True)

    def back_propagate(self, value):
        p = self

        while True:
            p.t = value
            p.n += 1
            if p.parent is None:
                break


def mcts(game, evaluator, iterations=100):
    root = Node(game)

    for _ in range(iterations):
        current = root

        while current.is_expanded():
            current = current.best_child()

        if current.n:
            current.expand()
            current = current.best_child()

        value = current.rollout(evaluator)
        current.back_propagate(value)

    return root.best_child().state.last_move
