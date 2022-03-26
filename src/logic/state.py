Player = bool
Position = tuple[int, int]


class State:
    """Represents the state of the 'gekitai' game"""

    def __init__(self):
        self.board: list[list[Player | None]] = [[None for _ in range(6)] for _ in range(6)]
        self.player: Player = False
        self.markers: tuple[int, int] = 8, 8
        self.last_move: Position | None = None

    def actions(self) -> list[Position]:
        return [(i, j) for i, ln in enumerate(self.board) for j, elem in enumerate(ln) if elem is None]

    def is_over(self) -> bool:
        if not self.markers[self.player]:
            return True

        placed_markers = [(i, j) for i, ln in enumerate(self.board) for j, elem in enumerate(ln) if elem is self.player]
        for marker_position in placed_markers:
            if self._position_has_win(marker_position):
                return True
        return False

    def _position_has_win(self, position: Position) -> bool:
        masks = {'N': (-1, 0, -2, 0), 'E': (0, 1, 0, 2), 'S': (1, 0, 2, 0), 'W': (0, -1, 0, -2),
                 'NE': (-1, 1, -2, 2), 'SE': (1, 1, 2, 2), 'SW': (1, -1, 2, -2), 'NW': (-1, -1, -2, -2)}

        for mask in masks.values():
            if self._check_position_against_mask(position, mask):
                return True
        return False

    def _check_position_against_mask(self, position: Position, mask: tuple[int, int, int, int]) -> bool:
        i, j = position
        i0, j0, i1, j1 = mask

        try:
            if not (0 <= i+i0 < 6 and 0 <= j+j0 < 6 and 0 <= i+i1 < 6 and 0 <= j+j1 < 6):
                raise IndexError
            return self.board[i][j] == self.board[i+i0][j+j0] == self.board[i+i1][j+j1]
        except IndexError:
            return False


def move(state: State, position: Position) -> State:
    i, j = position

    if state.board[i][j] is not None:
        return state     # Invalid move

    state.last_move = position
    state.board[i][j] = state.player
    state.markers[state.player] -= 1
    state.player = not state.player
    return _push_pieces(state, position)


def _push_pieces(state: State, position: Position) -> State:
    return NotImplemented
