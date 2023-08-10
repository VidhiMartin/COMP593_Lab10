'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_into() function
    # Use breakpoints to view returned dictionary
    pokemon_info = get_pokemon_info("Rockruff")
    pokemon_names = get_pokemon_names()
    download_pokemon_artwork("rockruff", "rockruff_artwork.png")
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success!')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

#Define function that gets a list of all Pokemon names from the PokeAPI
def get_pokemon_names():
    print('Getting list of all Pokemon names...', end='')
    resp_msg = requests.get(POKE_API_URL)
    
    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success!')
        data = resp_msg.json()
        pokemon_names = [pokemon['name'] for pokemon in data['results']]
        return pokemon_names
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')


#Define function that downloads and saves Pokemon artwork
def download_pokemon_artwork(pokemon, filename):
    print(f'Downloading artwork for {pokemon.capitalize()}...', end='')
    url = f"{POKE_API_URL}{pokemon}/"
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        data = resp_msg.json()
        artwork_url = data['sprites']['other']['official-artwork']['front_default']
            
        image_data = requests.get(artwork_url).content
        with open(filename, 'wb') as image_file:
            image_file.write(image_data)
        print('success!')
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')


if __name__ == '__main__':
    main()