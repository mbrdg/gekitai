from logic import *
from pprint import pprint

if __name__ == '__main__':
    st = [State()]

    st.append(move(st[-1], position=(3, 3)))
    pprint(st[-1].board)
    st.append(move(st[-1], position=(0, 0)))
    pprint(st[-1].board)

    next_state = move(st[-1], position=(3, 2))
    pprint(st[-1].board)
    pprint(st[-1].markers)
