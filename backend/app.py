import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# get the environment variables
mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('MONGO_DB_NAME')
collection_name = os.getenv('MONGO_COLLECTION_NAME')

# Initialize Flask app with custom template folder path
app = Flask(__name__)

########################################################
# Get the absolute path to data.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

@app.route('/api')
def get_data():
    with open(DATA_FILE) as f:
        return jsonify(json.load(f))
    

########################################################
# MongoDB Connection
########################################################
# MongoDB connection setup using the MONGO_URL environment variable
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]


# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Expecting JSON data, not form data
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({'error': 'Name and age are required'}), 400

    # Redirect to the success page after successful submission
    collection.insert_one({'name': name, 'age': age})
    return jsonify({'message': 'Data inserted successfully'}), 200


if __name__ == '__main__':
    app.run(port=3000,debug=True)
    
