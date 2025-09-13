from numpy import ndarray
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from psycopg2 import connect, extensions, sql
from psycopg2.extensions import cursor
from pgvector.psycopg2 import register_vector
from pgvector import Vector

try:
    connection: extensions.connection = connect(
        host=DB_HOST,   
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    register_vector(connection)
    
    cursor: extensions.cursor = connection.cursor()
    
    # Add pgvector extension
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    connection.commit()
except Exception as e:
    raise Exception(f"Error while connecting to database: {e}")
finally:
    cursor.close()
    
    
def create_table(table_name: str, *columns: str):
    if not table_name or not columns:
        raise ValueError("Table name and at least one column definition are required.")

    columns_definition: str = ", ".join(columns)

    try:
        cursor: extensions.cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});")
        connection.commit()
    except Exception as e:
        raise Exception(f"Error while creating table '{table_name}': {e}")
    finally:
        cursor.close()
       
 
def insert_a_value(table: str, column: str, value):
    if not isinstance(table, str):
        raise TypeError("table must be a string")
    
    if not isinstance(column, str):
        raise TypeError("column must be a string")
    
    
    if isinstance(value, list):
        value: str = f"ARRAY{value}" 
    
    try:
        cursor: extensions.cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {table} ({column}) VALUES ({value})")
        connection.commit()
    except Exception as e:
        raise Exception(f"Error while inserting value {value} into table '{table}';, column '{column}': {e}")
    finally:
        cursor.close()
        

def insert_embedding(table: str, columns: list[str], values: list):
    if not isinstance(table, str):
        raise TypeError("table must be a string")
    
    if not isinstance(columns, list) or not all(isinstance(col, str) for col in columns):
        raise TypeError("columns must be a list of strings")
    
    if not isinstance(values, list):
        raise TypeError("values must be a list")

    processed_values = []
    for val in values:
        if isinstance(val, ndarray):
            processed_values.append(Vector(val.astype(float).tolist()))
        else:
            processed_values.append(val)
    
    try:
        cursor: extensions.cursor = connection.cursor()
        
        columns_sql = sql.SQL(', ').join([sql.Identifier(col) for col in columns])
        placeholders = sql.SQL(', ').join(sql.Placeholder() * len(columns))
        
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({placeholders})").format(
            table=sql.Identifier(table),
            columns=columns_sql,
            placeholders=placeholders
        )
        cursor.execute(query, processed_values)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise Exception(f"Error while inserting values {values} into table '{table}', columns '{columns}': {e}")
    finally:
        if cursor:
            cursor.close()
    