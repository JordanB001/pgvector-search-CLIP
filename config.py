from dotenv import load_dotenv
from os import getenv


load_dotenv()

DB_NAME: str = getenv("DB_NAME")
DB_USER: str = getenv("DB_USER")
DB_HOST: str = getenv("DB_HOST")
DB_PORT: str = getenv("DB_PORT", "5432")
DB_PASSWORD: str = getenv("DB_PASSWORD")

path_to_folder: str = "pictures"

table_name: str = "pictures"

model_name: str = "clip-ViT-B-32"


### TEST ###
if not DB_NAME:
    raise ValueError("Missing required environment variable: DB_NAME")
if not isinstance(DB_NAME, str):
    raise TypeError("DB_NAME must be a string")

if not DB_USER:
    raise ValueError("Missing required environment variable: DB_USER")
if not isinstance(DB_USER, str):
    raise TypeError("DB_USER must be a string")

if not DB_HOST:
    raise ValueError("Missing required environment variable: DB_HOST")
if not isinstance(DB_HOST, str):
    raise TypeError("DB_HOST must be a string")

if not DB_PORT:
    raise ValueError("Missing required environment variable: DB_PORT")
if not isinstance(DB_PORT, str):
    raise TypeError("DB_PORT must be a string")

if not DB_PASSWORD:
    raise ValueError("Missing required environment variable: DB_PASSWORD")
if not isinstance(DB_PASSWORD, str):
    raise TypeError("DB_PASSWORD must be a string")

if not isinstance(path_to_folder, str):
    raise TypeError("path_to_folder must be a string")

if not isinstance(table_name, str):
    raise TypeError("table_name must be a string")

if not isinstance(model_name, str):
    raise TypeError("model_name must be a string")


############ 