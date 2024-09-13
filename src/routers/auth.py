#Authentication & Authorization

from fastapi import APIRouter,Depends,Body,HTTPException,Response,status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer 
from typing import Annotated
from fastapi import APIRouter,Body,HTTPException,Response,status
from src.utils.postgres_connector import PostgresConnector
from dotenv import load_dotenv
import jwt
import pendulum
import os
load_dotenv() 
app_access_key = os.environ.get("APP_ACCESS_KEY")
oauth2_barear = OAuth2PasswordBearer(tokenUrl="/auth/token")


router = APIRouter(prefix="/auth", tags=["authentication & authorization"])

def create_access_token(user_id: int, user_first_name: str, user_last_name: str, user_role: str):
    
    payload_encode = {
        "id": user_id,
        "sub": f"{user_first_name} {user_last_name}",
        "user_role": user_role,
        "exp": pendulum.now().add(hours=10).timestamp()
    }
    return jwt.encode(payload_encode, app_access_key, algorithm="HS256")


def authenticate_user(username: str, password: str):
    db_connector = PostgresConnector()
    result = db_connector.select_query(
        """                               
            SELECT * FROM issac_app.users
            WHERE email = %(username)s AND user_password = %(password)s
        """,{"username": username, "password": password})
    db_connector.close_connection()

    if len(result) == 1 :
        return result.iloc[0].to_dict()
    return False

def get_current_user(token: Annotated[str, Depends(oauth2_barear)]):
    try: 
        payload = jwt.decode(token, app_access_key, algorithms=["HS256"])
        user_name = payload.get("sub")
        user_role = payload.get("user_role")
        user_id = int(payload.get("id"))
        if user_name is None or user_role is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")
        return {"user_name": user_name, "user_role": user_role, "user_id": user_id}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    


@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]) -> dict:

    user = authenticate_user(form_data.username,form_data.password)
    if user is not False:
        access_token = create_access_token(user['id'],user['first_name'],user['last_name'],user['user_role'])
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")

 

