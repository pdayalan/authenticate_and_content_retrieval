import time
import hashlib
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize Boto3 client for DynamoDB
region = 'ap-south-1'  # Replace 'your_region' with your AWS region
dynamodb = boto3.client('dynamodb', region_name=region)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'Users'
table_arn = 'arn:aws:dynamodb:ap-south-1:123630172817:table/Users' + table_name 
table = dynamodb.Table(table_name)

# Create table if not exists
def create_table():
    if not dynamodb.Table(table_name).table_status == 'ACTIVE':
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
        while dynamodb.Table(table_name).table_status != 'ACTIVE':
            time.sleep(1)
        print("Table created successfully.")

create_table()  # Call the function to create the table

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# CRUD Operations
def create_user(username, password):
    hashed_password = hash_password(password)
    response = table.put_item(Item={'username': username, 'password': hashed_password})
    return response

def get_user(username):
    response = table.get_item(Key={'username': username})
    return response.get('Item')

def update_user(username, password):
    hashed_password = hash_password(password)
    response = table.update_item(
        Key={'username': username},
        UpdateExpression='SET password = :val1',
        ExpressionAttributeValues={':val1': hashed_password},
        ReturnValues='UPDATED_NEW'
    )
    return response

def delete_user(username):
    response = table.delete_item(Key={'username': username})
    return response

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = get_user(username)
    if user and user.get('password') == hash_password(password):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/content', methods=['GET'])
def get_content():
    # Authentication logic can be added here
    return jsonify({"content": "This is some sample content"})

if __name__ == '__main__':
    app.run(debug=True)
