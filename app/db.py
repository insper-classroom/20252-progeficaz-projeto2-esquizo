import pymysql
import os
from dotenv import load_dotenv

load_dotenv()  # carrega variáveis do .env

def get_connection():  # dados do banco de dados
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )
