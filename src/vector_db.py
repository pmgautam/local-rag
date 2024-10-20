import json
import uuid
from typing import List

from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, PointStruct, VectorParams

from prompts import system_prompt, user_prompt
from src.embedding import TextEncoder
from src.llm import get_streaming_response


class QdrantPoint(BaseModel):
    embedding: List[float]
    text: str


class QdrantDocument(BaseModel):
    qdrant_points: List[QdrantPoint]
    collection_name: str


class VectorDB:
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.client = QdrantClient(host, port=port)
        self.encoder = TextEncoder()

    def list_collections(self):
        collection_names = self.client.get_collections()
        return [x.name for x in collection_names.collections]

    def create_collection(self, collection_name: str):
        if not self.client.collection_exists(collection_name=collection_name):
            try:
                return self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                )
            except Exception as e:
                return f"Index creation error: {e}"
        return True

    def upsert_documents(self, documents: QdrantDocument):
        col_name = documents.collection_name
        qdrant_points = documents.qdrant_points

        if not self.client.collection_exists(col_name):
            self.create_collection(col_name)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=point.embedding,
                payload={"text": point.text},
            )
            for point in qdrant_points
        ]

        return self.client.upsert(collection_name=col_name, points=points)

    def __retrieve_context(self, query: str, collection_name: str):
        embedding = self.encoder.encode_text(query)
        context = self.client.query_points(
            query=embedding, collection_name=collection_name, limit=4
        )
        return context

    def query(self, query: str, collection_name: str):
        try:
            context = self.__retrieve_context(
                query=query, collection_name=collection_name
            )
            context = "\n\n".join([x.payload["text"] for x in context.points])
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt.format(question=query, context=context),
                },
            ]
            yield from get_streaming_response(messages, stream=True)
        except UnexpectedResponse as e:
            yield {"message": {"content": json.loads(e.content)["status"]["error"]}}
        except Exception:
            yield {"message": {"content": "An error occurred"}}
