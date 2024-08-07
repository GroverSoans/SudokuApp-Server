from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')  # This will enable CORS for all routes

@app.route("/api/users", methods = ['GET'])
def users():
    return jsonify(
                   {
                       "users": [
                           'grover',
                           'ben',
                           'enigma'
                       ]
                       
                   }
                )

if __name__ == '__main__':
    app.run(debug=True, port=8080)
