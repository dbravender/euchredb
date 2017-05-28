from __future__ import print_function
from itertools import combinations
import json
import sqlite3


suits = ['h', 'd', 'c', 's']
values = ['a', 'k', 'q', 'j', '0', '9']

cards = [value + suit for suit in suits for value in values]

hands = {}

conn = sqlite3.connect('euchre.db')
c = conn.cursor()
c.execute('create table hands (hand text unique, populated integer default 0, '
          'result text);')

for hand in combinations(cards, 5):
    trump_cards = tuple(sorted([card for card in hand if card.endswith('h')]))
    same_color_cards = tuple(sorted([card for card in hand if card.endswith('d')]))
    clubs = tuple(sorted([card[0] for card in hand if card.endswith('c')]))
    spades = tuple(sorted([card[0] for card in hand if card.endswith('s')]))
    off_cards = tuple(sorted([clubs, spades]))
    hand_index = (trump_cards, same_color_cards, off_cards)
    if hand_index not in hands:
        c.execute('insert into hands (hand) values (?)', [json.dumps(hand)])
        hands[hand_index] = True

conn.commit()
conn.close()
print(len(hands))
