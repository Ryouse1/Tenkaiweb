from fastapi import FastAPI, UploadFile, Depends
from fastapi.responses import StreamingResponse
from app.utils import extract_archive_to_memory
from app.oauth import get_current_user
from app.drive import upload_to_drive

app = FastAPI()

@app.post("/upload/")
async def upload(file: UploadFile, user=Depends(get_current_user)):
    data = await file.read()
    
    # メモリ上で展開
    try:
        extracted_zip = extract_archive_to_memory(file.filename, data)
    except Exception as e:
        return {"error": f"展開できません: {str(e)}"}
    
    # Google Drive 保存希望なら
    if user.drive_token:
        await upload_to_drive(user, extracted_zip, "extracted.zip")
    
    # ブラウザに直接返す
    return StreamingResponse(
        extracted_zip,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=extracted.zip"}
    )
