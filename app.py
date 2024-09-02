from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database  import Database
from pymongo.collection  import Collection
from bson import ObjectId
import os 
load_dotenv()
connection_string: str = os.environ.get("CONNECTION_STRING")
mongo_client = MongoClient(connection_string)
database = mongo_client.get_database("blog")
users_collection = database.get_collection("users")




app = Flask(__name__)




app.config["MONGO_URI"] = "mongodb+srv://admin:admin@blog.gpgebis.mongodb.net/blog"
mongo = PyMongo(app).db


@app.route("/users")
def show_users():
    try:
        mongo_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    users = users_collection.find()
    return render_template("users.html", users=users)



# CRUD operace pro kolekci Users
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    return jsonify(user_list)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.users.find_one_or_404({'_id': ObjectId(user_id)})
    user['_id'] = str(user['_id'])
    return jsonify(user)

@app.route('/users', methods=['POST'])
def add_user():
    user_data = request.json
    user_id = mongo.db.users.insert_one(user_data).inserted_id
    user_id = mongo.db
    return jsonify(str(user_id)), 201

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    update_data = request.json
    mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'message': 'User deleted successfully'})

# CRUD operace pro kolekci Articles (podobně jako pro kolekci Users)

# CRUD operace pro kolekci Comments (podobně jako pro kolekci Users)

if __name__ == '__main__':
    app.run(debug=True)
