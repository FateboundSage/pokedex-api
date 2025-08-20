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
    return json.dumps(poke_weakness)

def evolution_chain(name):
    # Normalize name for search
    name = name.lower()
    # Find entry for queried pokemon
    poke_row = data[data['Name'].str.lower() == name]
    if poke_row.empty:
        return {"error": "Pokémon not found"}

    number = poke_row['Number'].iloc[0]

    # Find all Pokémon with this number (forms)
    forms = data[data['Number'] == number]
    
    # Now, try to get pre-evo and next-evo by searching for consecutive numbers
    pre_evo = data[data['Number'] == number-1]
    evo = data[data['Number'] == number+1]

    # Build output: previous stage(s), forms, next stage(s)
    chain = []
    for _, row in pre_evo.iterrows():
        chain.append({"Name": row['Name'], "Form": row.get('Form', 'Normal')})
    for _, row in forms.iterrows():
        chain.append({"Name": row['Name'], "Form": row.get('Form', 'Normal')})
    for _, row in evo.iterrows():
        chain.append({"Name": row['Name'], "Form": row.get('Form', 'Normal')})
    evolution = {"evolution_family": chain}
    return json.dumps(evolution)
