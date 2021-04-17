# API_Demo
Creating an API in Python to provide data back to a user.

This is based on the tutorials at 
https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

## Base URL
This will display the home page. 
http://127.0.0.1:5000/

## All Books
This will provide the three test books in our catalogue, in JSON.
Path: api/v1/resources/books/all
Parameters:
Example: http://127.0.0.1:5000/api/v1/resources/books/all

## Return a specific book, in JSON.
Path: /api/v1/resources/books
Parameters: id (used to provide the id of the book you want to return)
Example: http://127.0.0.1:5000/api/v1/resources/books?id=1 (this will return the book with id 1)