from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import os

app = FastAPI()

# Montar carpeta estática para servir medios
app.mount("/media", StaticFiles(directory="app/static/media"), name="media")

@app.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    urls = []
    for upload in files:
        # 1. Calculamos la extensión (.jpg, .mp4, etc.)
        ext = os.path.splitext(upload.filename)[1]
        # 2. Generamos un nombre único con UUID
        filename = f"{uuid4().hex}{ext}"
        # 3. Definimos la ruta donde lo vamos a guardar en tu VPS
        save_path = os.path.join("app/static/media", filename)
        # 4. Abrimos (o creamos) ese archivo en modo binario y escribimos su contenido
        with open(save_path, "wb") as f:
            content = await upload.read()  # leemos todos los bytes que enviaste
            f.write(content)               # los volcamos al disco
        # 5. Construimos la URL pública que devolverá FastAPI
        urls.append(f"https://tudominio.com/media/{filename}")
    return {"urls": urls}


