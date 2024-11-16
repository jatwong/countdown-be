from os import path
from environ import Env

# Initialize the environ object
env = Env()

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
ENV_FILE = f"{BASE_DIR}/.env"

if path.exists(ENV_FILE):
    env.read_env(ENV_FILE)

# Try reading a variable
SECRET_KEY = env.str("SECRET_KEY", default="not-so-secret")
print(f"SECRET_KEY: {SECRET_KEY}")