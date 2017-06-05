from itertools import repeat
import sqlite3

from flask import Flask, render_template, request
app = Flask(__name__)


conn = sqlite3.connect('euchre.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


@app.route('/')
def best_first_card():
    cards = request.args.getlist('card')[:5]
    cards += list(repeat('', 5 - len(cards)))
    query_cards = ['%%%s%%' % card for card in cards]
    results = c.execute("select card as card, rank as rank, count(*) as count, "
                        "avg(ucb) as average_ucb, sum(wins) * 1.0 / sum(visits) "
                        "as win_percentage, sum(wins) as wins, sum(visits) as "
                        "visits from hand_cards where hands_by_card_id in "
                        "(select rowid from hands_with_cards where cards like "
                        "? and cards like ? and cards like ? "
                        "and cards like ? and cards like ?) "
                        "group by card, rank order by rank, count(*) desc "
                        "limit 5",
                        query_cards)
    return render_template('index.html',
                           cards=cards,
                           results=map(dict, results))
