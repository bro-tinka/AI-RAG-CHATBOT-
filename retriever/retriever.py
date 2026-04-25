import fitz
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from collections import deque
import os

###
# Objective : Ingest, Chunk, Retreive 
# 1 ) Ingest the pdf 
# 2 ) Chunk it & store in vectore store
# 2 ) Retrieve the chunks from vector Store using similarity Search

class PDFRetrievalPipeline:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.history_query = deque(maxlen=2)


    def ingest_pdfs(self, pdf_files, chunk_size=100, overlap=25): #10:1.5
        chunks = []
        for pdf in pdf_files:
            # Read file byte & Handle all cases safely ---
            if isinstance(pdf, str):
                file_bytes = open(pdf, "rb").read()
            elif hasattr(pdf, "name"):  # NamedString
                file_bytes = open(pdf.name, "rb").read()
            elif hasattr(pdf, "file"):  # FastAPI UploadFile
                file_bytes = pdf.file.read()
                pdf.file.seek(0)
            else:  # file-like (TemporaryFileWrapper)
                file_bytes = pdf.read()
                pdf.seek(0)

            # Open PDF from memory
            doc = fitz.open(stream=file_bytes, filetype="pdf")

            for page in doc:
                words = page.get_text("text").split()
                for i in range(0, len(words), chunk_size - overlap):
                    chunk = " ".join(words[i:i + chunk_size])
                    if chunk.strip():
                        chunks.append(chunk)

        self.chunks = chunks
        embeddings = self.model.encode(chunks).astype("float32")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        
    def retrieve(self, query, top_k=3):
        self.history_query.append(query)

        # decide whether to use history
        if len(query.strip().split()) <= 2:
            query = " ".join(self.history_query)

        queryE = self.model.encode([query]).astype("float32")
        _, idx = self.index.search(queryE, top_k)   # FAISS expects shape (1, dim)

        # retrieved_chunks 
        return "\n\n".join(self.chunks[i] for i in idx[0])

        


