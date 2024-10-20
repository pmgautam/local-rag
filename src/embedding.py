# Load model directly
from typing import List

from sentence_transformers import SentenceTransformer


class TextEncoder:
    def __init__(self, model_name: str = "Snowflake/snowflake-arctic-embed-m-v1.5"):
        self.model = SentenceTransformer(model_name, trust_remote_code=True)

    def encode_text(self, input_data: str | List[str]):
        encoding = self.model.encode(input_data)
        encoding_list = encoding.tolist()

        return encoding_list
