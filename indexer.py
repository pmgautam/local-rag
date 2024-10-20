import click

from src.chunking import PDFTextChunker
from src.embedding import TextEncoder
from src.vector_db import QdrantDocument, QdrantPoint, VectorDB


@click.command()
@click.option("--folder", "-f", required=True, help="Folder location to index")
@click.option("--collection", "-c", required=True, help="Name of the collection")
def main(folder, collection):
    print("Running chunking")
    pdf_chunker = PDFTextChunker(max_chunk_size=1024, overlap=256)
    text_chunks = pdf_chunker.chunk_pdf_files(folder)

    print("Running embedding")
    encoder = TextEncoder()
    embeddings = encoder.encode_text(text_chunks)

    print("Upserting points to vector db")
    vector_db = VectorDB()
    docs = []
    for text_chunk, embedding in zip(text_chunks, embeddings):
        doc = QdrantPoint(embedding=embedding, text=text_chunk)
        docs.append(doc)

    qdoc = QdrantDocument(qdrant_points=docs, collection_name=collection)
    vector_db.upsert_documents(qdoc)
    print("Indexing complete")

if __name__ == "__main__":
    main()
