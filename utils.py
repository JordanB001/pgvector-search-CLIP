from os.path import exists, isfile, join
from os import listdir
from PIL import Image
from numpy import ndarray, float32
from model import model

def get_all_file_paths_from_folder(path_to_folder: str) -> list[str]:
    if not isinstance(path_to_folder, str):
        raise TypeError("path_to_folder must be a string")
    if not exists(path_to_folder):
        raise FileNotFoundError(f"The file '{path_to_folder}' does not exist") 


    file_paths: list[str] = []
    for entry in listdir(path_to_folder):
        full_path: str = join(path_to_folder, entry)
        
        if isfile(full_path):
            file_paths.append(full_path)
            
    return file_paths
    

def encode_image(image_path: str) -> ndarray:
    if not isinstance(image_path, str):
        raise TypeError("image_path must be a string")
    
    if not exists(image_path):
        raise FileNotFoundError(f"image_path {image_path} not found")
    
    try:
        with Image.open(image_path) as image:
            image: Image = image.convert("RGB")

            embedding: ndarray = model.encode([image], convert_to_numpy=True, normalize_embeddings=True)[0].astype(float32)
    except Exception as e:
        raise Exception(f"Error while encoding image: {e}")
            
    return embedding


def encode_text(query: str) -> ndarray:
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    
    embedding: ndarray = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0].astype(float32)
    return embedding



