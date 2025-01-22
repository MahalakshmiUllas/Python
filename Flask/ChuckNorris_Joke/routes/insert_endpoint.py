## Description: 1. Endpoint to create joke locally(POST)
##              2. Free text search endpoint consiering local and remote search results(GET)
## Author: Mahalakshmi Ullas

from flask import Blueprint
from flask import request, jsonify  
import requests
import json

## Create a Blueprint
insert_ep = Blueprint('insert', __name__)

## Local json file path
jokes_file = 'local_jokes.json'

## Loading jokes locally from json file
with open(jokes_file, 'r') as file1:
    local_jokes = json.load(file1) 

## Function to save jokes to the JSON file
def save_jokes(jokes):
    with open(jokes_file, 'w') as f:
        json.dump(jokes, f, indent=4)

## Loading jokes into memory 
newjokes = local_jokes
## Endpoint to add a new joke and give JSON data with 'newjoke' key
@insert_ep.route('/api/jokes', methods=['POST'])
def create_newjoke():
    data = request.json
    ## Validating is there any data and contains 'newjoke' key 
    if not data or 'newjoke' not in data:
        return jsonify({"error": "Not valid input. 'newjoke' key have to be given."}), 400
    
    joke_text = data['newjoke']
    ## Checking if any duplicates is present
    for joke in newjokes:
        ## Checks if the query string exists within the lowercase version of the joke text
        if joke['joke'].lower() == joke_text.lower(): 
            return jsonify({"error": "The joke trying to insert already exists!!"}), 409
    ## Generating new id in incremental way and saving new jokes to the file 
    joke_id = len(newjokes) + 1  
    cnjoke = {"id": joke_id, "joke": joke_text}
    newjokes.append(cnjoke)
    save_jokes(newjokes)  
    ## Returns the last updated version
    return jsonify({"note": "Hurray! You have added a new joke successfully!", "joke": cnjoke}), 201

## Endpoint to get all jokes which are stored
@insert_ep.route('/api/jokes', methods=['GET'])
def getting_newjokes():
    return jsonify({"jokes": newjokes}), 200


## Function to search local jokes
def search_locally(query):
    query = query.lower()
    ## iterates through local_jokes, checks is there joke key and 
    ## checks if the query string exists within the lowercase version of the joke text
    return [joke for joke in local_jokes if query in joke["joke"].lower()]

## Function to search remote jokes
def search_remotely(query):
    ## f-string because it allows embedding expressions inside string literals using curly braces {}
    url = f"https://api.chucknorris.io/jokes/search?query={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            ## get("result",[]) retrieves the value associated with result, if not return empty list
            return response.json().get("result", [])
        else:
            return []
    except Exception as e:
        print(f"Error while fetching remote jokes: {e}")
        return []

## Route for searching jokes
@insert_ep.route('/search', methods=['GET'])
def search_jokes():
    ## request.args contains query parameters(key:value pair) after ?
    ## get('query', '') tries to retrieve the query parameter from URL, if not will return default value as empty string(bzc it will raise keyerror)
    ## .strip() because it removes any leading and trailing whitespace from string 
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    ## Performing both the searches
    local_search_results = search_locally(query)
    remote_search_results = search_remotely(query)

## Used this because we need to look for duplicate 
## Combine the values of both search results using id and return inside a list
    ## here id values become keys, joke dictionary becomes values
    ## extracts only the values from the dictionary
    combined_results = {joke["id"]: joke for joke in local_search_results + remote_search_results}.values()
    return jsonify({"query": query, "results": list(combined_results)})


