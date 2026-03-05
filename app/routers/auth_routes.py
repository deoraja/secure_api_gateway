from fastapi import APIRouter, HTTPException
from app.models.user_model import User, UserLogin
from app.services.auth_service import register_user, authenticate_user,get_user,verify_password
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register")
def register(user: User):

    new_user = register_user(user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Username exists")

    return {"message": "user registered"}


from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db_user = get_user(form_data.username)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username})

    return {"access_token": token, "token_type": "bearer"}