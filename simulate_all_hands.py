import json
import sys
import sqlite3

from mittmcts import MCTS
from euchre.euchre import EuchreGame

unprocessed_hands = []
conn = sqlite3.connect('euchre.db')
c = conn.cursor()


def main():
    while True:
        hands = c.execute('select rowid, * from hands where populated = 0 order by random() limit 1')
        if not hands:
            sys.exit(0)
        for hand in hands:
            rowid = hand[0]
            c.execute('update hands set populated = 1 where rowid = ?', [rowid])
            hand = json.loads(hand[1])
            state = EuchreGame.initial_state(hand, trump='h')
            result = (MCTS(EuchreGame, state)
                      .get_simulation_result(10000, get_leaf_nodes=True))
            children = {
                child.move: {'ucb': child.ucb1(0),
                             'visits': child.visits,
                             'wins': child.wins_by_player[0]}
                for child in result.root.children}
            c.execute('update hands set populated = 1, result = ? where rowid = ?',
                      [json.dumps(children), rowid])
            print(json.dumps(children))
            conn.commit()

if __name__ == '__main__':
    main()
    conn.close()
