import pandas as pd 
import json
data = pd.read_csv('d:/vs code/ml/projects/project_2/All_Pokemon.csv')

def pokedex():
    pokedex = data[['Name','Type 1','Type 2','Abilities','Generation','Final Evolution','Catch Rate','Legendary','Mega Evolution']]
    return pokedex.to_json(orient='records')

def legends():
    pokedex = data[['Name','Type 1','Type 2','Abilities','Generation','Final Evolution','Catch Rate','Legendary','Mega Evolution'] ]
    legendary = pokedex[data['Legendary']==1]
    return legendary.to_json(orient='records')

def stats(pokemon):
    pokemon_stats = data[['Name','Abilities','HP','Att','Spa','Spd','BST','Mean']]
    pokemon_stats['pokemon']
    pokemon_stats.set_index('Name')
    return pokemon_stats.to_json(orient='records')

def leaderboard():
    pokemon_stats = data[['Name','Abilities','HP','Att','Spa','Spd','BST','Mean']]

    leaderboard = pokemon_stats.sort_values(by="Mean" , ascending=False)
    return leaderboard.to_json(orient='records')

