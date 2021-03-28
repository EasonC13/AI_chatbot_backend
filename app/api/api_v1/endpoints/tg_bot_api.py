
from fastapi import APIRouter
router = APIRouter()



@router.get("/test")
async def test():
    print("HIHI")
    return "Hi Hi"