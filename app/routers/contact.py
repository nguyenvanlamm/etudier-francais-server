from fastapi import APIRouter, Depends
from app.schemas.exam import ContactRequest

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("")
def submit_contact(
    request: ContactRequest,
    db=None
):
    return {
        "message": "Contact form submitted successfully",
        "data": {
            "name": request.name,
            "email": request.email,
            "subject": request.subject,
            "message": request.message
        }
    }