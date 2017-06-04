import sqlite3

from flask import Flask, jsonify
app = Flask(__name__)


conn = sqlite3.connect('euchre.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


@app.route('/')
def hello_world():
    result = c.execute("select card as card, rank as rank, count(*) as count, "
                       "avg(ucb) as average_ucb, sum(wins) * 1.0 / sum(visits) "
                       "as win_percentage, sum(wins) as wins, sum(visits) as "
                       "visits from hand_cards where hands_by_card_id in "
                       "(select rowid from hands_with_cards where cards like "
                       "'%jd%' and cards like '%jh%' and cards like '%0s%' "
                       "and cards like '%9s%' and cards like '%js%') "
                       "group by card, rank order by rank, count(*) desc;")
    return jsonify(map(dict, result.fetchall()))
