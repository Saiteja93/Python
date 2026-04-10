from fastapi import APIRouter

router = APIRouter()




@router.get("/auth")
async def get_inf():
    return {"This is router info"}