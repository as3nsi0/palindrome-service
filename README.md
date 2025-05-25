# Palindrome service
Service based on REST API with JSON that will allow to detect palindromes. A palindrome is considered when a sentence
contains exactly the same letters reading from left to right as from right to left. 

## REST API Endpoints

This service offers the possibility to manage the detections of palindromes based on the following exposed endpoints:

| Method | Endpoint               | Description                                                                 |
|--------|------------------------|-----------------------------------------------------------------------------|
| POST   | `/detections/`         | Detects whether a given text is a palindrome based on the specified language. |
| GET    | `/detections/`         | Lists all palindrome detections. Supports optional filters by date and language. |
| GET    | `/detections/{id}`     | Retrieves the result of a specific palindrome detection by its ID.         |
| DELETE | `/detections/{id}`     | Deletes a specific palindrome detection by its ID.                         |

## Documentation 
Access to the documentation through:

`http://127.0.0.1:8000/docs`


## Test
In order to run the tests, run the following line:

`pytest --cov=app tests/`
