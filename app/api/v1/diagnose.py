from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.diagnostic_schema import DiagnoseTextRequest
from app.services.ai_service import analyze_text, analyze_image_text
from datetime import datetime
import uuid

router = APIRouter(prefix="/diagnose", tags=["Diagnostic"])

@router.post("/text")
async def diagnose_text(req: DiagnoseTextRequest):
    try:
        result = await analyze_text(req.text, req.lang, req.mode)
        result["id"] = str(uuid.uuid4())
        result["is_offline"] = False
        result["created_at"] = datetime.utcnow().isoformat()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image")
async def diagnose_image(
    file: UploadFile = File(...),
    lang: str = Form("fr"),
    mode: str = Form("beginner")
):
    try:
        contents = await file.read()
        import pytesseract
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(contents))
        ocr_text = pytesseract.image_to_string(img)
        if not ocr_text.strip():
            raise HTTPException(status_code=400, detail="Aucun texte detecte dans l image")
        result = await analyze_image_text(ocr_text, lang)
        result["id"] = str(uuid.uuid4())
        result["ocr_text"] = ocr_text
        result["is_offline"] = False
        result["created_at"] = datetime.utcnow().isoformat()
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))