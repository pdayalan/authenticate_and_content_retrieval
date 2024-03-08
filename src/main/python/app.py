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
    """
    Creates a DynamoDB table named 'Users' if it doesn't exist.
    """
    table_name = 'Users'
    try:
        dynamodb.describe_table(TableName=table_name)
    except dynamodb.exceptions.ResourceNotFoundException:
        dynamodb.create_table(
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
    """
    Hashes the given password using SHA-256 algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

# CRUD Operations
def create_user(username, password):
    """
    Creates a new user in the DynamoDB 'Users' table.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        dict: Response from DynamoDB put_item operation.
    """
    hashed_password = hash_password(password)
    response = dynamodb.put_item(
        TableName='Users',
        Item={'username': {'S': username}, 'password': {'S': hashed_password}}
    )
    return response

def get_user(username):
    """
    Retrieves user information from the DynamoDB 'Users' table.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        dict: User information if found, else None.
    """
    response = dynamodb.get_item(
        TableName='Users',
        Key={'username': {'S': username}}
    )
    return response.get('Item')

def update_user(username, password):
    """
    Updates the password of an existing user in the DynamoDB 'Users' table.

    Args:
        username (str): The username of the user.
        password (str): The new password of the user.

    Returns:
        dict: Response from DynamoDB update_item operation.
    """
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
    """
    Deletes a user from the DynamoDB 'Users' table.

    Args:
        username (str): The username of the user to delete.

    Returns:
        dict: Response from DynamoDB delete_item operation.
    """
    response = dynamodb.delete_item(
        TableName='Users',
        Key={'username': {'S': username}}
    )
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    GET: Returns a message indicating that a GET request was received.
    POST: Attempts to authenticate the user. Returns success message if authentication succeeds,
    otherwise returns an error message.
    """
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = get_user(username)
        if user and user.get('password', {}).get('S') == hash_password(password):
            return jsonify({"message": "Login successful"})
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({"message": "GET request received"})

@app.route('/users', methods=['POST'])
def create_new_user():
    """
    Creates a new user.

    Expects JSON payload with 'username' and 'password'.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    response = create_user(username, password)
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        return jsonify({"message": "User created successfully"})
    return jsonify({"message": "Failed to create user"}), 500

@app.route('/users/<username>', methods=['GET'])
def get_user_info(username):
    """
    Retrieves information about a user.

    Args:
        username (str): The username of the user to retrieve.
    """
    user = get_user(username)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route('/users/<username>', methods=['PUT'])
def update_user_info(username):
    """
    Updates the password of an existing user.

    Args:
        username (str): The username of the user.
    """
    data = request.get_json()
    password = data.get('password')
    response = update_user(username, password)
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "Failed to update user"}), 500

@app.route('/users/<username>', methods=['DELETE'])
def delete_user_info(username):
    """
    Deletes an existing user.

    Args:
        username (str): The username of the user to delete.
    """
    response = delete_user(username)
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "Failed to delete user"}), 500

@app.route('/content', methods=['GET'])
def get_content():
    """
    Returns sample content.
    """
    return jsonify({"content": "This is some sample content"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
