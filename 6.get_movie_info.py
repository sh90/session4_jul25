# https://rapidapi.com/octopusteam-octopusteam-default/api/imdb236/playground/apiendpoint_ac5596dc-0e15-48b2-b8de-04ab775280cc
#pip install requests
import requests

headers = {
    'x-rapidapi-host': 'imdb236.p.rapidapi.com',
    'x-rapidapi-key': '766ea387a6msh84ff46479ed9b4bp18b495jsna547d73e1ef5'
}

params = {'query': "matrix"}


IMDB_API_URL = "https://imdb236.p.rapidapi.com/api/imdb/autocomplete"
response = requests.get(IMDB_API_URL, headers=headers, params=params)
print(response.json())
print("Hi")
