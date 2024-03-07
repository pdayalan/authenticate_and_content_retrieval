# authenticate_and_content_retrieval

Run docker-compose up and it should install below : (Make sure docker service is running)
- DynamoDB Local | runs on port 8000
- Flask Application server | runs on port 5100

Then run below Curl commands to perform CRUD Operations:

1: Create (POST): To create a new user, you can send a POST request with the user's credentials to the /create endpoint.

Example using curl:

curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user", "password": "password123"}' http://127.0.0.1:5000/create_user


2: Read (GET): To retrieve user information, you can send a GET request to the /user/<username> endpoint.

Example using curl:

curl http://localhost:5000/get_user?username=new_user


3: Update (PUT): To update a user's password, you can send a PUT request with the updated password to the /update/<username> endpoint.

Example using curl:

curl -X PUT -H "Content-Type: application/json" -d '{"password": "new_password"}' http://localhost:5000/update_user/username


4: Delete (DELETE): To delete a user, you can send a DELETE request to the /delete/<username> endpoint.

Example using curl:

curl -X DELETE http://localhost:5000/delete/username



