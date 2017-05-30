from __future__ import print_function
from itertools import combinations
import json
import sqlite3


suits = ['h', 'd', 'c', 's']
values = ['a', 'k', 'q', 'j', '0', '9']

cards = [value + suit for suit in suits for value in values]

total_hands = 0
fixed_hands = 0
hands = {}

conn = sqlite3.connect('euchre.db')
c = conn.cursor()

for hand in combinations(cards, 5):
    total_hands += 1
    trump_cards = tuple(sorted([card for card in hand if card.endswith('h')]))
    same_color_cards = tuple(sorted([card for card in hand if card.endswith('d')]))
    clubs = tuple(sorted([card[0] for card in hand if card.endswith('c')]))
    spades = tuple(sorted([card[0] for card in hand if card.endswith('s')]))
    off_cards = tuple(sorted([clubs, spades]))
    hand_index = (trump_cards, same_color_cards, off_cards)
    if hand_index in hands:
        rows = c.execute('select result from hands where hand = ?',
                         [json.dumps(hands[hand_index])])
        new_result = {}
        for row in rows:
            result = json.loads(row[0])
            for card, result in result.iteritems():
                if card.endswith('c'):
                    new_result[card[0] + 's'] = result
                if card.endswith('s'):
                    new_result[card[0] + 'c'] = result
            fixed_hands += 1
        print(hand)
        print(new_result)
        c.execute('insert into hands (hand, result, was_duplicate) '
                  'values (?, ?, 1)',
                  [json.dumps(hand), json.dumps(new_result)])
    hands[hand_index] = hand

conn.commit()
conn.close()
print(total_hands)
print(fixed_hands)
