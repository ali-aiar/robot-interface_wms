import os
from dotenv import load_dotenv

# Load the environment variables from .env

load_dotenv()
# Database URL
DATABASE_URL = os.getenv('DATABASE_URL')
# Server host and port
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

# SQL account
USER = os.getenv('USER')
PASS = os.getenv('PASS')

# SQL DB and Table
DB = os.getenv('DATABASE')
TABLE = os.getenv('TABLE')

# Robot port
ROBOT_PORT = os.getenv('ROBOT_PORT')

# # Secret key for Flask app
# SECRET_KEY = os.environ["SECRET_KEY"]

# # Other settings
# DEBUG = os.environ["DEBUG"] == "True"
