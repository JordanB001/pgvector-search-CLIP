from typing import Any
from numpy import ndarray
from sympy.functions.combinatorial.numbers import nD
from db import connection
from psycopg2 import extensions


def similarity_search(table: str, column: str, vector: list | ndarray, limit: int=10) -> list[tuple[Any]]:
    if not isinstance(table, str):
        raise TypeError("table must be a string")
    
    if not isinstance(column, str):
        raise TypeError("column must be a string")
    
    if not isinstance(vector, (list, ndarray)):
        raise TypeError("vector must be a list")
    
    if not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 1:
        raise ValueError("limit must be greater than 0")
    
    
    if isinstance(vector, ndarray):
        vector: list = vector.tolist()
    
    try:
        cursor: extensions.cursor = connection.cursor()
        # Include similarity score in results
        cursor.execute(f"SELECT *, {column} <-> ARRAY{vector}::vector AS distance FROM {table} ORDER BY {column} <-> ARRAY{vector}::vector LIMIT {limit};")
        results: list[tuple[Any]] = cursor.fetchall()
        return results
    except Exception as e:
        raise Exception(f"Error during similarity search: {e}")
    finally:
        cursor.close()
