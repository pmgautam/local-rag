import glob

import pdfplumber
from tqdm import tqdm


class PDFTextChunker:
    def __init__(self, max_chunk_size=1000, overlap=50):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def __chunk_text(self, text):
        chunks = []
        start_index = 0

        while start_index < len(text):
            end_index = min(start_index + self.max_chunk_size, len(text))
            chunk = text[start_index:end_index].strip()

            if chunk:
                chunks.append(chunk)

            start_index = max(
                start_index + self.max_chunk_size - self.overlap, end_index
            )

        return chunks

    def chunk_pdf_files(self, file_path):
        chunks = []
        pdf_files = glob.glob(f"{file_path}/**/*.pdf", recursive=True)

        for pdf_file in tqdm(
            pdf_files, total=len(pdf_files), leave=False, desc="Chunking files"
        ):
            content = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    content += page.extract_text(x_tolerance=1)

            file_chunks = self.__chunk_text(text=content)
            chunks.extend(file_chunks)

        return chunks
