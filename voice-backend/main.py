from typing import Union

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def read_root():
    return { "message" : "Hello world!"}
@app.get("/audio")
def send_audio():
    audio_path = "./shout.mp3"

    return FileResponse(audio_path, media_type="audio/mpeg", filename="shout.mp3")
@app.post("/uploadaudio")
async def parse_audio(audio_file: UploadFile):

    return {"filename": audio_file.filename}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)