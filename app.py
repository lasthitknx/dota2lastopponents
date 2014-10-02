import bottle
import app_fnc

app = bottle.Bottle()

@app.route('/id=<id>')
def index(id):
    return bottle.template('index.html', data=app_fnc.get_last_match_enemies_stats(id), id=id)

app.run()
