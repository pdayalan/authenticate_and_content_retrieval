import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Disable AWS credentials check
# os.environ['AWS_ACCESS_KEY_ID'] = ''
# os.environ['AWS_SECRET_ACCESS_KEY'] = ''

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='', endpoint_url='http://127.0.0.1:8000', aws_access_key_id='dummy', aws_secret_access_key='dummy')
# dynamodb = boto3.resource('dynamodb', region_name='', endpoint_url='http://127.0.0.1:8000')
table_name = 'Users'
table = dynamodb.Table(table_name)

# Create table if not exists
if not dynamodb.Table(table_name).table_status == 'ACTIVE':
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

# CRUD Operations
def create_user(username, password):
    response = table.put_item(Item={'username': username, 'password': password})
    return response

def get_user(username):
    response = table.get_item(Key={'username': username})
    return response.get('Item')

def update_user(username, password):
    response = table.update_item(
        Key={'username': username},
        UpdateExpression='SET password = :val1',
        ExpressionAttributeValues={':val1': password},
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
    if user and user.get('password') == password:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/content', methods=['GET'])
def get_content():
    # Authentication logic can be added here
    return jsonify({"content": "This is some sample content"})

if __name__ == '__main__':
    app.run(debug=True)
