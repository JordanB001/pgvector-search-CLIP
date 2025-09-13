from typing import Any
from config import table_name, path_to_folder
from model import model, vector_size
from utils import encode_text, get_all_file_paths_from_folder, encode_image

from psycopg2 import extensions
from numpy import ndarray
from db import connection, create_table, insert_embedding
from similarity_search import similarity_search

if __name__ == "__main__":
    try:
        cursor: extensions.cursor = connection.cursor()

        create_table(table_name, "path VARCHAR(255) PRIMARY KEY", f"embedding vector({vector_size})")
        
        # Get all pictures from a folder
        picture_paths: list[str] = get_all_file_paths_from_folder(path_to_folder=path_to_folder)
        
        # Insert picture into Database
        for picture_path in picture_paths:
            embedding: ndarray = encode_image(image_path=picture_path)
            try:
                insert_embedding(table=table_name, columns=["path", "embedding"], values=[picture_path, embedding])
            except Exception as e:
                if "duplicate key value" not in str(e).lower() and "already exists" not in str(e).lower():
                    raise Exception(f"Error while inserting embedding into table {table_name}: {e}")
        
        # Search
        while True:
            query: str = input("Enter a description (press Ctrl+C to exit): ")
            rows: list[tuple[Any]] = similarity_search(table=table_name, column="embedding", vector=encode_text(query=query), limit=10)  
            
            for row in rows:
                print(f"distance: {round(row[2], 2)}", "path:", row[0])
                
                
        
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
    finally:
        connection.close()
    