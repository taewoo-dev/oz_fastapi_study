from fastapi import FastAPI, UploadFile
from users.router import router as u_router

app = FastAPI()

app.include_router(router=u_router)


@app.post("/file")
def upload_file_handler(file: UploadFile):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
    }
