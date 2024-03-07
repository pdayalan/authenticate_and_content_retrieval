# authenticate_and_content_retrieval

Run docker-compose up and it should install below : (Make sure docker service is running)
- DynamoDB Local | runs on port 8000
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




