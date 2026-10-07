#from http.client import HTTPException
from .. import schemas,database,models
from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.schemas import TokenData
from sqlalchemy.orm import Session
from ..config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})

    jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token:str,credentials_exception):
    try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
            id : str = payload.get("user_id")

            if id is None:
                 raise  credentials_exception

            token_data = schemas.TokenData(id=id)

    except     JWTError:
        raise credentials_exception

    return token_data
    #return credentials_exception


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id == token_data.id).first()


    if user is None:
        raise credentials_exception

    return user
   # return verify_access_token(token,credentials_exception)
    #return token_data

def require_admin(
    current_user:models.User=Depends(get_current_user)):

    if current_user.role !="admin":
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,detail="Admin access required")

    return current_user




  #  user = db.query(models.User).filter(
   #     models.User.id == current_user.id
    #).first()

    #if not user:
     #   raise HTTPException(
      #      status_code=status.HTTP_401_UNAUTHORIZED,
       #     detail="User not found"
        #)

  #  if user.role != "admin":
   #     raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
     #       detail="Admin access required"
      #  )

    #return user