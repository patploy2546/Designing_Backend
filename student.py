from flask import Flask, jsonify, request, Response
from pymongo import MongoClient, errors
from bson import ObjectId
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = '6530300392'
app.config['BASIC_AUTH_PASSWORD'] = 'Ploy2546'
basic_auth = BasicAuth(app)

client = MongoClient("mongodb+srv://6530300392:Ploy2546@student.kdwblfn.mongodb.net/")
db = client["students"]
std_info_collection = db["std_info"]

@app.route("/")
def greet():
    return "Welcome to Student Management API"

@app.route("/students", methods=["GET"])
@basic_auth.required
def get_all_students():
    students = std_info_collection.find()
    return jsonify([student for student in students])

@app.route("/students/<string:_id>", methods=["GET"])
@basic_auth.required
def get_student(_id):
    student = std_info_collection.find_one({'_id': _id})
    if student:
        return jsonify(student)
    else:
        return jsonify({"error":"Student not found"}), 404

@app.route("/students", methods=["POST"])
@basic_auth.required
def create_student():
    data = request.get_json()
    existing_student = std_info_collection.find_one({'_id': data['_id']})
    if existing_student:
        return jsonify({"error": "Cannot create new student"}), 500
    result = std_info_collection.insert_one(data)

    if result.inserted_id:
        student = std_info_collection.find_one({'_id': data['_id']})
        return jsonify(student), 200

@app.route("/students/<string:_id>", methods=["PUT"])
@basic_auth.required
def update_student(_id):
    data = request.get_json()
    result = std_info_collection.update_one({'_id': _id}, {'$set': data})
    if result.matched_count:
        student = std_info_collection.find_one({'_id': _id})
        return jsonify(student), 200
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<string:_id>", methods=["DELETE"])
@basic_auth.required
def delete_student(_id):
    result = std_info_collection.delete_one({'_id': _id})
    if result.deleted_count:
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
