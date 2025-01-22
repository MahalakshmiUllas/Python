## Description: 1. Endpoint to fetch joke locally and remotely by unique id(GET)
##              2. Endpoint to update joke and store it locally(PUT)
##              3. Endpoint to detete joke and update it locally(DELETE)
## Author: Mahalakshmi Ullas

import json
import requests
from flask import jsonify, request, render_template
from flask import Blueprint

## Create a Blueprint
update_ep = Blueprint('update', __name__, template_folder='templates/update')

## Local json file path
local_file = 'localjokes_file.json'

## Loading jokes locally from json file
with open(local_file, 'r') as file:
    local_cnjokes = json.load(file)

## Function to save jokes to the JSON file
def save_jokes_locally(jokes):
    with open(local_file, 'w') as file:
        json.dump(jokes, file, indent=4)

## Serve the single HTML file
@update_ep.route('/')
def home():
    return render_template('index.html')

## Endpoint to get jokes by unique id
@update_ep.route('/jokes/<joke_id>', methods=['GET'])
def get_joke(joke_id):
    ## Retrives joke locally, else fetches remote joke
    ## joke_id are stored as strings in JSON
    joke = local_cnjokes.get(str(joke_id))  
    if joke is not None:
        return jsonify({"id": joke_id, "joke": joke}), 200

    ## Fetching a remote joke by unique id
    ## f-string because it allows embedding expressions inside string literals using curly braces {}
    remote_api_url = f"https://api.chucknorris.io/jokes/{joke_id}"
    try:
        get_response = requests.get(remote_api_url)
        if get_response.status_code == 200:
            remote_joke = get_response.json().get('value', 'Jokes not found.')
            return jsonify({"id": joke_id, "joke": remote_joke}), 200
        elif get_response.status_code == 404:
            return jsonify({"error": "Jokes not found remotely."}), 404
        else:
            return jsonify({"error": "Could not retrieve remote joke."}), 502
    ## Returns meaningful error response during the HTTP requests are caught and handled 
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Remote joke service is not available.", "message": str(e)}), 503

## Endpoint to update joke by unique id
@update_ep.route('/jokes/<joke_id>', methods=['PUT'])
def update_joke_locally(joke_id):
    ## If the joke ID does not exist locally, return 404 
    if str(joke_id) not in local_cnjokes:
        return jsonify({"error": "Joke not found"}), 404

    ## Parse request JSON for the updated joke
    data = request.get_json()
    if not data or 'joke' not in data:
        return jsonify({"error": "Invalid input"}), 400

    updated_joke = data['joke']
    ## Update joke in the dictionary and saving updated jokes to the file
    local_cnjokes[str(joke_id)] = updated_joke  
    save_jokes_locally(local_cnjokes)  
    ## Returns the last updated version
    return jsonify({"id": joke_id, "joke": updated_joke}), 200

## Endpoint to delete joke by unique id
@update_ep.route('/jokes/<joke_id>', methods=['DELETE'])
def delete_joke_locally(joke_id):
    ## If the joke ID does not exist locally, return 404 
    if str(joke_id) not in local_cnjokes:
        return jsonify({"error": "Joke not found"}), 404

    ## Deleting the joke from the dictionary and saving updated jokes to the file
    del local_cnjokes[str(joke_id)]  
    save_jokes_locally(local_cnjokes)  
    ## Returns the last deleted joke with its unique id
    return jsonify({"message": f"Joke with ID {joke_id} deleted successfully."}), 200

