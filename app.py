from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

users = {}  # A dictionary to store user data temporarily

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    users[username] = password
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if users.get(username) != password:
        return jsonify({"message": "Invalid username or password"}), 401

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"token": token})

@app.route('/get-jwt', methods=['GET'])
def get_jwt():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"message": "Token is missing!"}), 401
    
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({"user": data['username']})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 401

@app.route('/set-jwt', methods=['POST'])
def set_jwt():
    data = request.json
    username = data.get('username')

    if username not in users:
        return jsonify({"message": "User does not exist"}), 404

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(debug=True)
