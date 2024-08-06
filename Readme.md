# Book Library API

## Remarks

- Each book replica has its own serial Id in order to track the loans for each specific replica.
- Client cannot loan the same book replica in the same day.
- In loan route there is option to add past loan with start and end loan dates.
- The client unique identifier is Email (It can be change according to other requirements).
- When adding new book to the app number of replicas being created in order to track and assign each copy to a different serial.

## Pre Installations

- Python version: 3.12

## Installation

- extract or clone this repository
- open terminal
- create new virtual env with the command `python -m venv venv`
- run the virtual env- windows `.\venv\Scripts\activate` or in mac `source venv/bin/activate`
- make sure you run the next commands inside the venv
- install the libraries `pip install -r requirements.txt`
- run migrations before run the app `alembic upgrade head`

## Run the App

- `uvicorn app.main:app`
- open browser in the url - http://127.0.0.1:8000/docs for documentation of the api and use also the api through this url

## Design

- FastApi Framework:
  - Routes Layer
    - This layer handles the HTTP requests and responses.
    - It defines the endpoints for the API and maps them to the appropriate service functions.
    - Uses FastAPI to create and manage routes.
  - Service Layer
    - This layer contains the business logic of the application.
    - It processes the data received from the routes and interacts with the CRUD layer to perform database operations.
    - Ensures that the business rules are enforced, such as preventing a client from loaning the same book replica on the same day.
  - Crud Layer
    - This layer interacts directly with the database.
    - It contains functions to create, read, update, and delete records in the database.
    - Uses SQLAlchemy to manage database operations.
- Sqlite
