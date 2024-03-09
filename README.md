# authenticate_and_content_retrieval

This is a Flask application for user management with DynamoDB integration. Let's break down the key components and functionality:

Dependencies and Imports: The application uses Flask for web development and boto3 for interaction with AWS DynamoDB. It also handles necessary imports and error handling for missing modules.

Initialization: The DynamoDB client is initialized with the specified region. The table creation function is called, ensuring that the 'Users' table exists in DynamoDB.

Table Creation: The create_table() function checks if the 'Users' table exists in DynamoDB. If not, it creates it with specified key schema, attributes, and provisioned throughput.

Password Hashing: The hash_password() function hashes passwords using the SHA-256 algorithm for security.

CRUD Operations: Functions for creating, retrieving, updating, and deleting user records in DynamoDB are defined.

API Routes:

/login: Handles user login. It supports both GET and POST methods. For POST requests, it authenticates the user by checking the username and hashed password against stored values in DynamoDB.

/users: Supports creating new users via POST requests. Expects JSON payload with 'username' and 'password'.

/users/<username>: Supports GET, PUT, and DELETE methods for retrieving, updating, and deleting user information respectively.

/content: Provides sample content. This route is likely for testing purposes.

Run the Application: The Flask application is run with debug mode enabled and set to listen on all network interfaces.

Overall, this application provides a basic user management system with secure password storage using DynamoDB as the backend database.

*************************

Run docker-compose up and it should install below : (Make sure docker service is running)
- Flask Application server | runs on port 5100

Then run below Curl commands to perform CRUD Operations:

1: Create (POST): To create a new user, you can send a POST request with the user's credentials to the /create endpoint.

Example using curl:

curl -X POST \
  http://localhost:5100/users \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "auppal",
    "password": "admin"
}'




