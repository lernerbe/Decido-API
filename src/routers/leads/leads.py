from fastapi import APIRouter,Body,HTTPException,Response,status,Depends,Query,Path,UploadFile
import pandas as pd #to remove
from typing import Annotated
from src.models.users import UserBody,UserResponse,AllUsersResposne,TeamBody,TeamResponse,UserFilter,AllTeamsResposne
from src.routers.auth import get_current_user



router = APIRouter(prefix="/leads", tags=["leads"])

################################## LEADS ####################################

# Upload new Leads via CSV file
@router.post("/upload")
async def get_users(user:Annotated[dict,Depends(get_current_user)], file: UploadFile): 
    from io import StringIO

    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="The file is not CSV! the system support only CSV file")
    try:
        print(file.filename)
        file = await file.read() 
        csv_string = file.decode('utf-8')
        # Use StringIO to create a file-like object from the string
        csv_file_like = StringIO(csv_string)
        # Read the CSV into a Pandas DataFrame
        df = pd.read_csv(csv_file_like)
        print(df.columns)
        if df.columns[0] != "leads":
            first_row_df = pd.DataFrame([{"leads": df.columns[0]}])   
            df.rename(columns={df.columns[0]:"leads"},inplace=True)
            df = pd.concat([first_row_df,df], ignore_index=True)

        print(df)



    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in get_users: {e}"
            ) 
