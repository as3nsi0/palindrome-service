# Palindrome service
Service based on REST API with JSON that will allow to detect palindromes. A palindrome is considered when a sentence
contains exactly the same letters reading from left to right as from right to left. 

## Dependencies
To run the test through make, you must have installed the following packages:

`sudo apt install postgresql`  
`sudo apt install make`

## Start the service
1. `make setup`: Installs automatically the dependencies from the `pyproject.toml` and it will generate a version based on 
the version that you have in pyproject.toml.   
[ONLY DOCKER]: If you do not want to run the service in local, you can just run `make build-image` 
2. To run the service you must create a .env file which contains the following parameters:
`POSTGRES_USER=palindrome_user`  
`POSTGRES_PASSWORD=password`  
`POSTGRES_DB=detections`  
You can directly run `make create-env-file` which will create a .env file.
3. It is compulsory as well to replace the version in the docker-compose.prod.yml as:  
`image: palindrome:v0`
4. `make enable-production`: Runs the solution and start the service.


## Documentation 
Access to the documentation through:

`http://127.0.0.1:8000/docs`

### REST API Endpoints

This service offers the possibility to manage the detections of palindromes based on the following exposed endpoints:

| Method | Endpoint               | Description                                                                 |
|--------|------------------------|-----------------------------------------------------------------------------|
| POST   | `/detections/`         | Detects whether a given text is a palindrome based on the specified language. |
| GET    | `/detections/`         | Lists all palindrome detections. Supports optional filters by date and language. |
| GET    | `/detections/{id}`     | Retrieves the result of a specific palindrome detection by its ID.         |
| DELETE | `/detections/{id}`     | Deletes a specific palindrome detection by its ID.                         |

## Test
In order to run the tests, run the following line:  
`make test-all`

### Coverage tests results
`coverage: platform linux, python 3.12.3-final-0`

| Name                         | Stmts | Miss | Cover |
|------------------------------|-------|------|-------|
| app/__init__.py              | 0     | 0    | 100%  |
| app/crud.py                  | 31    | 0    | 100%  |
| app/database.py              | 13    | 2    | 85%   |
| app/main.py                  | 14    | 4    | 71%   |
| app/models.py                | 10    | 0    | 100%  |
| app/palindrome.py            | 10    | 0    | 100%  |
| app/routes/detection.py      | 32    | 0    | 100%  |
| app/schemas.py               | 12    | 0    | 100%  |
| app/utils/logger_config.py   | 10    | 0    | 100%  |
| **TOTAL**                    | **132**| **6**| **95%** |
