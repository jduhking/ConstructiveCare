from typing import Union

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.post("/uploadaudio")
async def parse_audio(audio_file: UploadFile):

    return {"filename": audio_file.filename}