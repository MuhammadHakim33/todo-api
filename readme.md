## Getting Started

### Prerequisites
This project uses mongodb as database system. You can create new database and add your connection string into .env file at ``DB_HOST`` variable.

### Installation
1. Clone this repository
    ```sh
    git clone https://github.com/MuhammadHakim33/todo-api.git
    ```
2. Create virtual environments
    ```sh
    python -m venv .venv
    ```
3. Install all dependencies
    ```sh
    pip install -r requirements.txt
    ```
4. Create new database and add your connection string into .env file and add to ``DB_HOST`` variable.
5. Create random secret key to sign the JWT tokens. Add this secret key into .env file and add to ``SECRET_KEY`` variable. You can use this command
    ```sh
    openssl rand -hex 32
    ```
6. Start the server
    ```sh
    uvicorn main:app --reload
    ```
7. To access, I recommend you to use Postman or Insomnia

### Learning Outcomes
1. Python web dev
2. Document Database (NoSQL)
3. Restapi
4. JWT