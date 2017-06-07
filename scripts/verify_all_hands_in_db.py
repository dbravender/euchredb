from __future__ import print_function
from itertools import combinations
import json
import sqlite3


suits = ['h', 'd', 'c', 's']
values = ['a', 'k', 'q', 'j', '0', '9']

cards = [value + suit for suit in suits for value in values]


conn = sqlite3.connect('euchre.db')
c = conn.cursor()

for hand in combinations(cards, 5):
    rows = c.execute('select result from hands where hand = ?',
                     [json.dumps(hand)])
    print('.', end='')
    assert(rows)

conn.close()
