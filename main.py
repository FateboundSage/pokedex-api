from flask import Flask,render_template,request,jsonify
import json
app = Flask(__name__)
import poke

@app.route('/pokedex')
def pokedex():
    pokedex = poke.pokedex()
    return pokedex

@app.route('/legendary')
def legends():
    legend = poke.legends()
    return legend

@app.route('/strength/<pokemon>')
def powers(pokemon):
    if not pokemon:
        return jsonify({'error': "Missing 'Name' query parameter"}), 400
    result = poke.stats(pokemon)
    if result is None:
        return jsonify({'error':f"Pokemon '{pokemon} not found"}),404
    return jsonify(result), 200


@app.route('/compare/<poke1>/<poke2>')
def compare(poke1,poke2):
    stats1 = poke.stats(poke1)
    stats2 = poke.stats(poke2)
    return {'poke1': stats1, 'poke2': stats2}

@app.route('/evolution/<name>')
def evolution_chain(name):
    chain = poke.evolution_chain(name)
    if not chain:
        return({'error':'Pokemon not found','chain':[]}), 404
    return jsonify(chain), 200

@app.route('/weakness/<name>')
def weakness(name):
    result = poke.weakness_and_counters(name)
    return jsonify(result)
    

@app.route('/leaderboard/')
def leaderboard():
    top_pokemon = poke.leaderboard()
    return top_pokemon

@app.route('/pokemon/<name>/image')
def get_pokemon_image(name):
    url = poke.get_image_url(name)
    return jsonify({'name':name,'image_url':url})
app.run(debug=True)