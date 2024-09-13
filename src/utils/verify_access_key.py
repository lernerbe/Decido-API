import os

from typing import Annotated
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

def verify_access_key(app_access_key: Annotated[str, Header()]):
    if app_access_key != os.environ.get("APP_ACCESS_KEY"):
        raise HTTPException(
            status_code=400, detail="app-access-key header invalid")
