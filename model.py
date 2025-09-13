from config import model_name
from sentence_transformers import SentenceTransformer
from PIL import Image
from numpy import ones, uint8
from torch.cuda import is_available

device: str = "cuda" if is_available() else "cpu"

model: SentenceTransformer = SentenceTransformer(model_name, device=device)

vector_size: int = model.get_sentence_embedding_dimension()

if not vector_size:
    vector_size: int = model.encode(Image.fromarray(ones((224, 224, 3), dtype=uint8) * 255)).shape[0]