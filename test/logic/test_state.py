from unittest import TestCase
from src.logic.state import *


class Test(TestCase):
    def test_move(self):
        state = State()

        state = move(state, (2, 2))
        state = move(state, (3, 4))
        state = move(state, (0, 0))
        state = move(state, (5, 0))

        expected_board = [[False, None, None, None, None, None],
                          [None, None, None, None, None, None],
                          [None, None, False, None, None, None],
                          [None, None, None, None, True, None],
                          [None, None, None, None, None, None],
                          [True, None, None, None, None, None]]
        self.assertEqual(state.board, expected_board)
        self.assertFalse(state.player)

    def test_move_with_push(self):
        state = State()

        state = move(state, (2, 2))
        state = move(state, (2, 3))
        state = move(state, (3, 3))
        state = move(state, (3, 4))
        state = move(state, (2, 4))

        expected_board = [[None, None, True, None, None, None],
                          [None, None, None, None, None, None],
                          [None, False, None, None, False, None],
                          [None, None, False, None, None, None],
                          [None, None, None, None, True, None],
                          [None, None, None, None, None, None]]
        self.assertEqual(state.board, expected_board)
        self.assertEqual(state.markers, [5, 6])
        self.assertTrue(state.player)

    def test_move_with_block_push(self):
        state = State()

        state = move(state, (1, 4))
        state = move(state, (3, 4))
        state = move(state, (4, 4))
        state = move(state, (3, 4))

        expected_board = [[None, None, None, None, None, None],
                          [None, None, None, None, False, None],
                          [None, None, None, None, True, None],
                          [None, None, None, None, True, None],
                          [None, None, None, None, None, None],
                          [None, None, None, None, False, None]]

        self.assertEqual(state.board, expected_board)
        self.assertEqual(state.markers, [6, 6])
        self.assertFalse(state.player)

    def test_move_with_push_and_dropping_top_left(self):
        state = State()

        state = move(state, (0, 0))
        state = move(state, (0, 2))
        state = move(state, (0, 3))
        state = move(state, (2, 0))
        state = move(state, (3, 0))

        expected_board = [[False, True, None, False, None, None],
                          [True, None, None, None, None, None],
                          [None, None, None, None, None, None],
                          [False, None, None, None, None, None],
                          [None, None, None, None, None, None],
                          [None, None, None, None, None, None]]

        self.assertEqual(state.board, expected_board)
        self.assertEqual(state.markers, [5, 6])
        self.assertTrue(state.player)

        state = move(state, (1, 1))

        expected_board = [[None, None, None, False, None, None],
                          [None, True, None, None, None, None],
                          [None, None, None, None, None, None],
                          [False, None, None, None, None, None],
                          [None, None, None, None, None, None],
                          [None, None, None, None, None, None]]

        self.assertEqual(state.board, expected_board)
        self.assertEqual(state.markers, [6, 7])
        self.assertFalse(state.player)

    def test_move_with_push_and_dropping_bottom_right(self):
        state = State()

        state = move(state, (5, 5))
        state = move(state, (5, 3))
        state = move(state, (5, 2))
        state = move(state, (3, 5))
        state = move(state, (2, 5))

        expected_board = [[None, None, None, None, None, None],
                          [None, None, None, None, None, None],
                          [None, None, None, None, None, False],
                          [None, None, None, None, None, None],
                          [None, None, None, None, None, True],
                          [None, None, False, None, True, False]]

        self.assertEqual(state.board, expected_board)
        self.assertEqual(state.markers, [5, 6])
        self.assertTrue(state.player)

        state = move(state, (4, 4))

        expected_board = [[None, None, None, None, None, None],
                          [None, None, None, None, None, None],
                          [None, None, None, None, None, False],
                          [None, None, None, None, None, None],
                          [None, None, None, None, True, None],
                          [None, None, False, None, None, None]]

        self.assertEqual(state.board, expected_board)
        self.assertEqual(state.markers, [6, 7])
        self.assertFalse(state.player)

    def test_actions(self):
        initial_state = State()
        expected_actions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                            (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
                            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]

        initial_actions = actions(initial_state)
        self.assertEqual(initial_actions, expected_actions)

        next_state = move(initial_state, (3, 4))
        expected_actions.remove((3, 4))
        next_state = move(next_state, (1, 1))
        expected_actions.remove((1, 1))

        possible_actions = actions(next_state)
        self.assertEqual(possible_actions, expected_actions)

    def test_is_over_trivial(self):
        state = State()
        self.assertFalse(is_over(state))

    def test_is_over_all_markers_placed(self):
        state = State()
        state.markers = [1, 0]
        state.board = [[True, False, True, False, None, True],
                       [None, False, None, None, None, True],
                       [True, None, True, False, None, None],
                       [None, None, True, None, None, True],
                       [None, None, False, None, None, None],
                       [False, None, None, None, False, None]]
        self.assertTrue(is_over(state))

    def test_is_over_diagonal_down(self):
        state = State()
        state.player = True
        state.board = [[None, None, None, None, None, None],
                       [None, None, True, None, None, None],
                       [None, False, True, False, None, None],
                       [None, None, False, True, None, None],
                       [None, None, None, False, None, None],
                       [None, None, None, None, None, None]]

        self.assertTrue(is_over(state))

    def test_is_over_diagonal_up(self):
        state = State()
        state.board = [[None, None, None, None, True, None],
                       [None, None, True, True, None, None],
                       [None, False, True, False, None, None],
                       [None, None, False, True, None, None],
                       [None, None, None, None, None, None],
                       [None, None, None, None, None, None]]

        self.assertTrue(is_over(state))

    def test_is_over_horizontal(self):
        state = State()
        state.player = True
        state.board = [[None, None, None, None, True, None],
                       [None, None, None, None, None, None],
                       [None, False, False, False, None, None],
                       [None, None, True, True, None, None],
                       [None, None, None, None, None, None],
                       [None, None, None, None, None, None]]

        self.assertTrue(is_over(state))

    def test_is_over_vertical(self):
        state = State()
        state.board = [[None, None, None, None, True, None],
                       [None, None, None, None, None, None],
                       [None, False, True, False, None, None],
                       [None, None, True, True, None, None],
                       [None, None, True, None, None, None],
                       [None, None, None, None, None, None]]

        self.assertTrue(is_over(state))

    def test_is_over_not_over(self):
        state = State()
        state.board = [[None, None, None, None, True, None],
                       [None, None, None, None, None, None],
                       [None, False, None, False, None, None],
                       [None, None, True, True, None, None],
                       [None, None, True, None, None, None],
                       [None, None, None, None, None, None]]

        self.assertFalse(is_over(state))
