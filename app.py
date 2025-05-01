import os
from flask import Flask, jsonify, request
from models import setup_db, Person, db # models.py greift auf DATABASE_URL zu
from flask_cors import CORS
from dotenv import load_dotenv # <<<--- 1. Importieren


load_dotenv()

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app) # Kann jetzt die geladene DATABASE_URL nutzen
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ.get('EXCITED', 'false')
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    

    @app.route('/get-people')
    def get_people():
        try:
            people_query = Person.query.all()
            formatted_people = [person.format() for person in people_query]

            return jsonify({"people": formatted_people}), 200
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred while fetching people."}), 500


    @app.route('/get-people/<int:person_id>')
    def get_person(person_id):
        try:
            person = Person.query.get(person_id)
            if person is None:
                return jsonify({"error": "Person not found."}), 404

            return jsonify({"person": person.format()}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred while fetching hthe person."}), 500

 
    @app.route('/get-people/<int:person_id>/catchphrase')
    def get_person_catchphrase(person_id):
        try:
            person = Person.query.get(person_id)
            if person is None:
                return jsonify({"error": "Person not found."}), 404

            return jsonify({"catchphrase": person.catchphrase}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred while fetching the person's catchphrase."}), 500
        

    @app.route('/add-people', methods=['POST'])
    def add_people():
        try:
            data = request.get_json()
            name = data.get('name')
            catchphrase = data.get('catchphrase', '')

            if not name:
                return jsonify({"error": "Name is required."}), 400

            new_person = Person(name=name, catchphrase=catchphrase)
            db.session.add(new_person)
            db.session.commit()

            return jsonify({"person": new_person.format()}), 201

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred while adding the person."}), 500
        
    return app   
    

app = create_app()

if __name__ == '__main__':
    app.run()