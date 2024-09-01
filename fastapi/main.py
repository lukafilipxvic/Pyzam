from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

@app.get("/identify/")
async def identify_song(url: str):
    command = [
        "pyzam",
        "--url", str(url),
        "--json"  # Use JSON mode
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return "\n".join(result.stdout.splitlines()[1:])  # Return everything after the first line
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")