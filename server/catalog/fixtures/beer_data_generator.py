import json
import random
import uuid

# Lists of possible data for generating random beers
countries_cities = [
    "Kaedwen",
    "Redania",
    "Novigrad",
    "Rivia",
    "Temeria",
    "Skellige",
    "Baldur's Gate",
    "Waterdeep",
    "Neverwinter",
    "Amn",
    "Candlekeep",
]

beer_styles = [
    "Stout",
    "Ale",
    "Wheat Beer",
    "Lager",
    "Mead",
    "Bitter",
    "Cider",
    "Porter",
    "Pilsner",
    "Saison",
]

breweries = [
    "The Silver Salamander Inn",
    "The Royal Rooster Brewery",
    "Brewer's Haven Tavern",
    "Temerian Brewcrafters Guild",
    "Skellige Mead Hall",
    "The Blade and Stars Brewery",
    "Mirt's Mellow Ales",
    "Neverwinter Brewmasters",
    "Amn Alesmiths",
    "Candlekeep Cellars",
]

# Adjectives for generating random descriptions
adjectives = [
    "dark",
    "classic",
    "refreshing",
    "powerful",
    "mystical",
    "legendary",
    "enchanting",
    "bold",
    "unique",
    "traditional",
]

# Generate a list of random beer entries
num_beers = 100000  # Number of random beers to generate
random_beers = []

for _ in range(num_beers):
    beer_id = str(uuid.uuid4())
    country_city = random.choice(countries_cities)
    style = random.choice(beer_styles)
    adjective = random.choice(adjectives)
    description = f"{adjective.title()} {style.lower()} from {country_city}."
    beer = {
        "model": "catalog.Beer",
        "fields": {
            "name": f"{country_city} {adjective} {style}",
            "country": country_city,
            "description": description,
            "id": beer_id,
            "points": random.randint(50, 100),
            "price": round(random.uniform(3.0, 10.0), 2),
            "style": style,
            "brewery": random.choice(breweries),
        },
    }
    random_beers.append(beer)

# Convert the list of random beers to a JSON string with pretty formatting
beers_json = json.dumps(random_beers, indent=4)

file_path = "random_beers.json"
with open(file_path, "w") as json_file:
    json_file.write(beers_json)

print(f"Generated random beer data and saved it to '{file_path}'.")
