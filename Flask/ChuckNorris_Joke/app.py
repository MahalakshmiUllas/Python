## Description: Entry point for running the Flask application
##              This logic to run the Flask app using the create_app() function defined in __init__.py
## Author: Mahalakshmi Ullas

from routes import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
