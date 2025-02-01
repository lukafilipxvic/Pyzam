from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import uuid
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/identify/url/")
async def identify_song(url: str):
    command = [
        "pyzam",
        "--url", str(url),
        "--json"  # Use JSON mode
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return JSONResponse(content=json.loads(result.stdout))
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")

@app.post("/identify/file")
async def upload_file(file: UploadFile = File(...)):
    # Ensure the temp directory exists
    os.makedirs("temp", exist_ok=True)
    
    file_location = f"temp/{uuid.uuid4()}.wav"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    command = [
        "pyzam",
        "--input", str(file_location),
        "--json"  # Use JSON mode
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return JSONResponse(content=json.loads(result.stdout))
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")
    finally:
        # Clean up the temporary file
        os.remove(file_location)