from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any, Dict
from bill_extractor import extract_bill_info_from_url


# ------------------------------------------------------------
# Initialize application
# ------------------------------------------------------------
# FastAPI app acts as the main HTTP interface for external clients.
app = FastAPI(
    title="Bill OCR Extraction API",
    description="API that extracts structured invoice details from an image URL",
    version="1.0.0"
)


# ------------------------------------------------------------
# Request schema using Pydantic
# ------------------------------------------------------------
class ExtractionRequest(BaseModel):
    """
    Data model for incoming POST request.
    'image_link' refers to the URL pointing to the bill image.
    """
    image_link: str = Field(..., description="Public URL pointing to an invoice or bill image.")


# ------------------------------------------------------------
# Route handler for OCR extraction
# ------------------------------------------------------------
@app.post("/extract-bill-data", tags=["OCR"])
async def handle_bill_extraction(payload: ExtractionRequest) -> Dict[str, Any]:
    """
    Main API route:
    ----------------
    - Accepts JSON with key 'image_link'
    - Passes URL to OCR extraction engine
    - Returns structured bill data (items, totals, etc.)
    
    Exception safety:
    - Any unexpected failure is caught
    - Returned in a clean JSON error structure
    """
    try:
        # Delegate OCR + parsing logic to external module
        processed_output = extract_bill_info_from_url(payload.image_link)
        return processed_output

    except Exception as error:
        # Return formatted error instead of crashing API
        return {
            "is_success": False,
            "data": None,
            "error_message": str(error)
        }