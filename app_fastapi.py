from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, UploadFile, File, Form, Request
from typing import List
import shutil
import os

from retriever.retriever import PDFRetrievalPipeline
from generator.generator import LLMGenerator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")
pipeline = None
generator = LLMGenerator()

@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    global pipeline
    # Create a temp directory for files if your pipeline needs paths
    os.makedirs("temp_pdfs", exist_ok=True)
    file_paths = []
    
    for file in files:
        path = f"temp_pdfs/{file.filename}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(path)
    
    pipeline = PDFRetrievalPipeline()
    pipeline.ingest_pdfs(file_paths)
    return {"status": "success", "message": "PDFs indexed Sucessfully! ✅"}

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    if pipeline is None:
        return {"answer": "❌ Error: System offline. Please upload PDFs first."}
    
    context = pipeline.retrieve(query)
    answer = generator.generate_answer(query, context)
    return {"answer": answer}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
