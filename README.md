# Pokédx API
A Flask-based REST API for retrieving Pokémon data, built as a learning project for API development with Flask.

## Description
This is a sample project created for learning and practicing API development using Flask. The API provides endpoints to retrieve Pokémon information from a CSV dataset, making it easy to search and access Pokémon data programmatically.

## Features
- RESTful API endpoints for Pokémon data retrieval
- Search functionality for finding specific Pokémon
- JSON responses for easy integration
- Clean and simple Flask application structure
- Data sourced from comprehensive Pokémon dataset

## Project Structure
```
pokedex-api/
├── main.py           # Main Flask application
├── poke.py           # Pokémon data handling logic
├── All_Pokemon.csv   # Pokémon dataset
├── pokemon.ipynb     # Jupyter notebook for data exploration
└── __pycache__/      # Python cache files
```

## Prerequisites
- Python 3.x
- Flask
- pandas (for CSV data handling)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/FateboundSage/pokedex-api.git
   cd pokedex-api
   ```
2. Install required dependencies:
   ```bash
   pip install flask pandas
   ```

## Usage
1. Start the Flask development server:
   ```bash
   python main.py
   ```
2. The API will be available at `http://localhost:5000`

## API Endpoints

### Base URL
`http://localhost:5000`

### Available Endpoints

**GET /pokedex** - Retrieve all Pokémon data
- Returns: JSON string with all Pokémon including Name, Type 1, Type 2, Abilities, Generation, Final Evolution, Catch Rate, Legendary status, and Mega Evolution info
- Example: `GET /pokedex`

**GET /legendary** - Retrieve all legendary Pokémon
- Returns: JSON string with all legendary Pokémon data
- Example: `GET /legendary`

**GET /strength** - Get Pokémon stats (currently returns all Pokémon stats)
- Query Parameters: Name (form parameter)
- Returns: JSON string with Name, Abilities, HP, Attack, Special Attack, Speed, Base Stat Total, and Mean stats for all Pokémon
- Example: `GET /strength?Name=Pikachu` 
- **Note**: This endpoint uses `request.form.get()` to extract the Name parameter from form data. 

**GET /compare** - Compare two Pokémon stats
- Query Parameters: 
  - poke1 (string) - Name of first Pokémon to compare
  - poke2 (string) - Name of second Pokémon to compare
- Returns: JSON object with stats for both Pokémon
- Example: `GET /compare?poke1=Pikachu&poke2=Charizard`
- **Note**: This endpoint uses query parameters (`request.args.get()`)

**GET /evolution/<name>** - Get evolution chain for a Pokémon
- Path Parameters: name (string) - Pokémon name
- Returns: JSON string with evolution family information
- Example: `GET /evolution/Pikachu`

**GET /weakness/<name>** - Get weaknesses and counter Pokémon
- Path Parameters: name (string) - Pokémon name (from URL path)
- Query Parameters: name (string) - Pokémon name (from query string)
- Returns: JSON string with weaknesses and counter Pokémon suggestions
- Example: `GET /weakness/Pikachu?name=Pikachu`
- **Note**: This endpoint has both path and query parameters for the name. The query parameter (`request.args.get('name')`) is used in the function, overriding the path parameter.

**GET /leaderboard/<stat>** - Get Pokémon leaderboard
- Path Parameters: stat (string) - Stat type for ranking
- Returns: JSON string with Pokémon ranked by Mean stat (descending order)
- Example: `GET /leaderboard/attack` or `GET /leaderboard/any-stat`
- **Note**: The stat parameter in the URL path is currently ignored. The leaderboard always ranks Pokémon by their 'Mean' stat in descending order regardless of the stat parameter provided.

### Response Format
All endpoints return JSON responses. The format varies by endpoint:
- Most endpoints return JSON strings (using `.to_json(orient='records')`)
- `/compare` returns a JSON object with poke1 and poke2 keys
- `/weakness/<name>` returns a JSON string with weaknesses and counter_pokemons
- `/evolution/<name>` returns a JSON string with evolution_family data

### Parameter Notes
- **Query vs Form Parameters**: The `/strength` endpoint incorrectly uses `request.form.get()` instead of `request.args.get()` for query parameters
- **Parameter Usage**: Some endpoints extract parameters but don't use them for filtering (like `/strength` and `/leaderboard/<stat>`)
- **Duplicate Parameters**: The `/weakness/<name>` endpoint has both path and query parameters for the same data

### Example Responses

**Pokémon Data Structure** (from /pokedex):
```json
[
  {
    "Name": "Bulbasaur",
    "Type 1": "Grass",
    "Type 2": "Poison",
    "Abilities": "Overgrow",
    "Generation": 1,
    "Final Evolution": "Venusaur",
    "Catch Rate": 45,
    "Legendary": 0,
    "Mega Evolution": 0
  }
]
```

**Compare Response** (from /compare):
```json
{
  "poke1": "[{\"Name\":\"Pikachu\",\"Abilities\":\"Static\",\"HP\":35,...}]",
  "poke2": "[{\"Name\":\"Charizard\",\"Abilities\":\"Blaze\",\"HP\":78,...}]"
}
```

## Dataset
The project uses a comprehensive Pokémon dataset (`All_Pokemon.csv`) containing information about various Pokémon including stats, types, and other attributes.

## Development Notes
This project serves as a hands-on learning experience for:
- Flask framework basics
- RESTful API design principles
- Data handling with pandas
- JSON response formatting
- API endpoint structuring

## Contributing
This is a learning project, but suggestions and improvements are welcome!

## License
This project is for educational purposes.

## Acknowledgments
- Built as part of learning Flask API development
- Pokémon data used for educational demonstration purposes
