# midtrans-merchant-server
Implementing midtrans payment gateway on server or backend using python Flask framework

## Installation
After cloning, create a virtual environment and install the requirements:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

## Database
Database using Sqlalchemy, so create database migration first. use the following command:

    (venv) $ flask db init
    (venv) $ flask db upgrade

## Running
To run the server use the following command:

    (venv) $ python main.py
     * Serving Flask app "app" (lazy loading)
     * Environment: development
     * Debug mode: on
     * Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
