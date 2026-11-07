FastAPI Hello World
A simple FastAPI application with two API endpoints:

/ - Returns a welcome message.
/greet/{name} - Returns a personalized greeting.
Project Structure
.
├── main.py
└── README.md
Requirements
Python 3.8+
FastAPI
Uvicorn
Installation
Create a virtual environment and install dependencies:

pip install fastapi uvicorn
Code
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
Running the Application
Start the server:

uvicorn main:app --reload
API Endpoints
Home
GET /

Response:

{
  "message": "Hello, FastAPI!"
}
Greeting
GET /greet/{name}

Example:

/greet/Anto
Response:

{
  "message": "Hello, Anto!"
}
Interactive API Documentation
After starting the server, open:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
Author
Beni