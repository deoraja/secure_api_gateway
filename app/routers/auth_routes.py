from fastapi import APIRouter, HTTPException
from app.models.user_model import User
from app.models.refresh_model import RefreshRequest
from app.services.auth_service import register_user,get_user, store_refresh_token,verify_password, verify_refresh_token
from app.core.security import create_access_token, create_refresh_token,SECRET_KEY,ALGORITHM
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from jose import jwt,JWTError

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

    new_access_token = create_access_token({"sub": form_data.username,"type": "access"})

    new_refresh_token = create_refresh_token({"sub": form_data.username, "type":"refresh"})

    store_refresh_token(form_data.username, new_refresh_token)

    return {"access_token": new_access_token, "refresh_token": new_refresh_token,"token_type": "bearer"}

@router.post("/refresh")
def refresh_token(request: RefreshRequest):
    
    token = request.refresh_token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        token_type = payload.get("type")

        if username is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        if not verify_refresh_token(username, token):
         raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        new_access_token = create_access_token({"sub": username,"type":"access"})

        new_refresh_token =create_refresh_token({"sub": username,"type": "refresh"})
       
        store_refresh_token(username, new_refresh_token)

        return {"access_token": new_access_token,"refresh_token": new_refresh_token,"token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")

    store_refresh_token(username, None)  

    return {"message": "Logged out"}