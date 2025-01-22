## Description: To integrate modular components into the main application using blueprints 
##              App object is created to initialize the application
## Author: Mahalakshmi Ullas

from flask import Flask  
from .update_endpoint import update_ep
from .insert_endpoint import insert_ep

def create_app():
    app = Flask(__name__)

    ## Registering Blueprints
    app.register_blueprint(update_ep)
    app.register_blueprint(insert_ep)

    return app