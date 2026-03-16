from fastapi import APIRouter, HTTPException
from app.models.user_model import User
from app.services.auth_service import register_user,get_user,verify_password
from app.core.security import create_access_token, create_refresh_token,SECRET_KEY,ALGORITHM
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from jose import jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register")
def register(user: User):

    new_user = register_user(user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Username exists")

    return {"message": "user registered"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db_user = get_user(form_data.username)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": form_data.username})
    refresh_token = create_refresh_token({"sub": form_data.username})

    return {"access_token": access_token, "refresh_token": refresh_token,"token_type": "bearer"}

@router.post("/refresh")
def refresh_token(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        token_type = payload.get("type")

        if username is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token({"sub": username})

        return {"access_token": new_access_token}

    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")