from flask import Flask,render_template,request
import json
app = Flask(__name__)
import poke

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pokedex')
def pokedex():
    pokedex = poke.pokedex()
    return pokedex

@app.route('/legendary')
def legends():
    legend = poke.legends()
    return legend

@app.route('/strength')
def powers():
    pokemon = request.form.get("Name")
    pokemon_stats = poke.stats(pokemon)
    return pokemon_stats

@app.route('/compare')
def compare():
    poke1 = request.args.get('poke1')
    poke2 = request.args.get('poke2')
    stats1 = poke.stats(poke1)
    stats2 = poke.stats(poke2)
    return {'poke1': stats1, 'poke2': stats2}

@app.route('/evolution/<name>')
def evolution_chain(name):
    chain = poke.evolution_chain(name)
    return chain

@app.route('/weakness/<name>')
def weakness(name):
    weaknesses, counters = poke.weakness_and_counters(name) 
    return {
        'weaknesses': weaknesses,
        'counter_pokemons': counters
    }

@app.route('/leaderboard/<stat>')
def leaderboard(stat):
    top_pokemon = poke.leaderboard(stat)  # Should return a list/dict of top Pokémon
    return top_pokemon

app.run(debug=True)