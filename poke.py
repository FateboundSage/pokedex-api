import pandas as pd 
import json
data = pd.read_csv('d:/vs code/ml/projects/project_2/All_Pokemon.csv')
evolution_data = pd.read_csv('d:/vs code/ml/projects/project_2/Pokemon_Evolution_Database.csv')

def pokedex():
    pokedex = data[['Name','Type 1','Type 2','Abilities','Generation','Final Evolution','Catch Rate','Legendary','Mega Evolution']]
    return pokedex.to_json(orient='records')

def legends():
    pokedex = data[['Name','Type 1','Type 2','Abilities','Generation','Final Evolution','Catch Rate','Legendary','Mega Evolution'] ]
    legendary = pokedex[data['Legendary']==1]
    return legendary.to_json(orient='records')

def stats(pokemon: str):
    pokemon_stats = data[['Name','Abilities','HP','Att','Spa','Spd','BST','Mean']]
    
    row = pokemon_stats[pokemon_stats['Name'].str.lower() == pokemon.lower()]
    if row.empty:
        return None
    # else return a single record as dictionary
    return row.iloc[0].to_dict()

def leaderboard():
    pokemon_stats = data[['Name','Abilities','HP','Att','Spa','Spd','BST','Mean']]

    leaderboard = pokemon_stats.sort_values(by="Mean" , ascending=False)
    return leaderboard.to_json(orient='records')

def weakness_and_counters(name, threshold=2.0, counters_per_type=2):
    pokedex = data
    against_cols = [
    'Against Normal', 'Against Fire', 'Against Water', 'Against Electric',
    'Against Grass', 'Against Ice', 'Against Fighting', 'Against Poison',
    'Against Ground', 'Against Flying', 'Against Psychic', 'Against Bug',
    'Against Rock', 'Against Ghost', 'Against Dragon', 'Against Dark',
    'Against Steel', 'Against Fairy'
    ]
    type_map = {c: c.replace('Against ', '') for c in against_cols}
    # type_map just cleans the names: "Against Fire" → "Fire"
    # 1. Find the Pokémon row
    mask = pokedex['Name'].str.lower() == name.lower()
    if not mask.any():
        return {"weaknesses": [], "counter_pokemons": []}
    row = pokedex.loc[mask].iloc[0]
    
    # 2. List all types with effectiveness >= threshold
    weaknesses = [
        {"Type": type_map[c], "Effectiveness": float(row[c])}
        for c in against_cols if row[c] >= threshold
    ]
    
    # 3. Find Pokémon whose Type 1 or Type 2 matches any weakness type
    weak_types = set(d["Type"] for d in weaknesses)
    counters = []
    for t in weak_types:
        counter_rows = pokedex[
            (pokedex["Type 1"] == t) | (pokedex["Type 2"] == t)
        ][["Name", "Type 1", "Type 2"]].drop_duplicates()
        for idx, counter_row in counter_rows.head(counters_per_type).iterrows():
            counters.append({
                "Name": counter_row["Name"],
                "Type 1": counter_row["Type 1"],
                "Type 2": counter_row["Type 2"] if pd.notna(counter_row["Type 2"]) else None
            })
    poke_weakness= {
        "weaknesses": weaknesses,
        "counter_pokemons": counters
    }
    return poke_weakness

def evolution_chain(name):
    poke_data = evolution_data[evolution_data['Name'].str.lower() == name.lower()]
    if poke_data.empty:
        return None
    return poke_data.iloc[0].to_dict()

def get_image_url(name):
    search = name.lower().strip().replace('-',' ')
    matches = data[data['Name'].str.lower() == search]

    if not matches.empty:
        number = matches.iloc[0]['Number']
        # as the pokeAPI uses the National Dex number
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{number}.png"
        return url
    return None