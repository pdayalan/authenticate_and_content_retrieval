import time
import hashlib
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize Boto3 client for DynamoDB
REGION = 'ap-south-1'  # Replace 'your_region' with your AWS region
dynamodb = boto3.client('dynamodb', region_name=REGION)

# Create table if not exists
def create_table():
    table_name = 'Users'
    try:
        dynamodb.describe_table(TableName=table_name)
    except dynamodb.exceptions.ResourceNotFoundException:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'password',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'password',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait for table to become active
        while dynamodb.describe_table(TableName=table_name).get('Table', {}).get('TableStatus') != 'ACTIVE':
            time.sleep(1)
        print("Table created successfully.")

create_table()  # Call the function to create the table

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# CRUD Operations
def create_user(username, password):
    hashed_password = hash_password(password)
    response = dynamodb.put_item(
        TableName='Users',
        Item={'username': {'S': username}, 'password': {'S': hashed_password}}
    )
    return response

def get_user(username):
    response = dynamodb.get_item(
        TableName='Users',
        Key={'username': {'S': username}}
    )
    return response.get('Item')

def update_user(username, password):
    hashed_password = hash_password(password)
    response = dynamodb.update_item(
        TableName='Users',
        Key={'username': {'S': username}},
        UpdateExpression='SET password = :val1',
        ExpressionAttributeValues={':val1': {'S': hashed_password}},
        ReturnValues='UPDATED_NEW'
    )
    return response

def delete_user(username):
    response = dynamodb.delete_item(
        TableName='Users',
        Key={'username': {'S': username}}
    )
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = get_user(username)
        if user and user.get('password', {}).get('S') == hash_password(password):
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        # Handle GET request, if needed
        return jsonify({"message": "GET request received"})

@app.route('/users', methods=['POST'])
def create_new_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    response = create_user(username, password)
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        return jsonify({"message": "User created successfully"})
    else:
        return jsonify({"message": "Failed to create user"}), 500

@app.route('/users/<username>', methods=['GET'])
def get_user_info(username):
    user = get_user(username)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/users/<username>', methods=['PUT'])
def update_user_info(username):
    data = request.get_json()
    password = data.get('password')
    response = update_user(username, password)
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"message": "Failed to update user"}), 500

@app.route('/users/<username>', methods=['DELETE'])
def delete_user_info(username):
    response = delete_user(username)
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"message": "Failed to delete user"}), 500

@app.route('/content', methods=['GET'])
def get_content():
    # Authentication logic can be added here
    return jsonify({"content": "This is some sample content"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
