# authenticate_and_content_retrieval

Run docker-compose up and it should install below : 
- DynamoDB Local | runs on port 8000
- Flask Application server | runs on port 5000

Then run below Curl commands to perform CRUD Operations:

1: Create (POST): To create a new user, you can send a POST request with the user's credentials to the /create endpoint.

Example using curl:

curl -X POST -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}' http://localhost:5000/create


2: Read (GET): To retrieve user information, you can send a GET request to the /user/<username> endpoint.

Example using curl:

curl http://localhost:5000/user/user1

3: Update (PUT): To update a user's password, you can send a PUT request with the updated password to the /update/<username> endpoint.

Example using curl:

curl -X PUT -H "Content-Type: application/json" -d '{"password": "newpassword"}' http://localhost:5000/update/user1

4: Delete (DELETE): To delete a user, you can send a DELETE request to the /delete/<username> endpoint.

Example using curl:

curl -X DELETE http://localhost:5000/delete/user1


