from pydantic import BaseModel, Field
from typing import Optional, Literal, Annotated

# Annotated:
# Annotated[str,Field(max_length=18,min_length=17)] equal to Optional[str]=Field(None, max_length=18,min_length=17) and it is equal to str = Field(..., max_length=18,min_length=17) 

# Users
class UserBody(BaseModel):
    first_name: str
    last_name: str
    team_name: str
    email: str = Field(pattern= r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$") # email validation
    user_password: str = Field(min_length=8) # password validation
    phone_number: str 
    user_role: Literal['admin', 'employee', 'manager']
    user_status: Literal['active', 'inactive'] = 'active'
    value: float = Field(le=1,ge=0)


class UserFilter(BaseModel):
    user_role: Optional[list[Literal['admin', 'employee', 'manager']]] = None
    user_status: Optional[list[Literal['active', 'inactive']]] = None
    team_name: Optional[list[str]] = None


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    team_name: str
    email: str
    phone_number: str
    user_role: Literal['admin', 'employee', 'manager']
    user_status: Literal['active', 'inactive']
    created_date: str

class AllUsersResposne(BaseModel):
    counter_users: int 
    pages: int
    users_response: list[UserResponse]    

#Teams
class TeamBody(BaseModel):
    team_name: str

class TeamResponse(BaseModel):
    id: int
    team_name: str
    created_date: str

class AllTeamsResposne(BaseModel):
    counter_teams: int 
    pages: int
    teams_response: list[TeamResponse]    





