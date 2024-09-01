## Pyzam API
Developers can leverage Pyzam to build a backend API to perform music identification.

### Dependencies
Pyzam APi requires fastapi
```bash
$ pip install fastapi

```

### Usage
```bash
# Initiate the API
fastapi dev main.py
```
```bash
# Get request using an audio URL
http://127.0.0.1:8000/identify?url=https://archive.org/download/09-hold-me-in-your-arms/02%20-%20Never%20Gonna%20Give%20You%20Up.mp3
```