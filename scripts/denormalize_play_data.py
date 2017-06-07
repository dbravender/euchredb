from __future__ import print_function
import json
import sqlite3

conn = sqlite3.connect('euchre.db')
c = conn.cursor()

c.execute('create virtual table hands_with_cards using fts3 (cards text)')
c.execute('create table hand_cards (hands_by_card_id integer, card text, '
          'visits integer, wins integer, ucb integer, rank integer)')

rows = c.execute('select rowid, hand, result from hands')
for row in rows:
    rowid = row[0]
    hand = json.loads(row[1])
    result = json.loads(row[2])
    c2 = conn.cursor()
    c2.execute('insert into hands_with_cards values (?)', [' '.join(hand)])
    rowid = c2.lastrowid
    ranks = set()
    for card, outcome in result.items():
        ranks.add(outcome['visits'])
    ranks = sorted(list(ranks), reverse=True)
    for card, outcome in result.items():
        c2.execute('insert into hand_cards '
                   '(hands_by_card_id, card, visits, wins, ucb, rank) '
                   'values (?, ?, ?, ?, ?, ?)',
                   [rowid, card, outcome['visits'], outcome['wins'],
                    outcome['ucb'], ranks.index(outcome['visits'])])

c.execute('create index hand_cards_by_card_id_idx on hand_cards '
          '(hands_by_card_id)')
conn.commit()
conn.close()
