from fastapi import FastAPI, File, UploadFile
from transformers import pipeline
import torch
import tempfile
import shutil

app = FastAPI()

# Load model (on CPU or GPU)
pipe = pipeline("automatic-speech-recognition", model="tarteel-ai/whisper-base-ar-quran", device=0 if torch.cuda.is_available() else -1)

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    result = pipe(tmp_path)
    return {"text": result["text"]}
