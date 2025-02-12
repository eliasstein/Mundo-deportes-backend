from fastapi import APIRouter
from fastapi.responses import Response,JSONResponse
from models import usermodel
from services import firebaseService as fb

router = APIRouter()

@router.post()
def check_valid_cookie():
    return {"Hola":"mundo"}