from pydantic import BaseModel, Field
from typing import Optional, Literal, Annotated

# Annotated:
# Annotated[str,Field(max_length=18,min_length=17)] equal to Optional[str]=Field(None, max_length=18,min_length=17) and it is equal to str = Field(..., max_length=18,min_length=17) 

# Leads
class LeadBody(BaseModel):
    id: str
    lead_status: str
    lead_type: str
    lead_message: Optional[str] = None
    user_id: Optional[int] = None

class LeadsFilter(BaseModel):
    lead_type: Optional[list[str]] = None
    lead_status: Optional[list[str]] = None

class LeadResponse(BaseModel):
    id: str
    lead_status: str
    lead_type: str
    lead_message: Optional[str] = None
    user_id: Optional[int] = None
    created_date: str
    updated_date: str

class AllLeadsResposne(BaseModel):
    counter_leads: int 
    pages: int
    leads_response: list[LeadResponse]    

#Statuses
class StatusBody(BaseModel):
    status_name: str

class StatusResponse(BaseModel):
    id: int
    status_name: str
    created_date: str

class AllStatusResposne(BaseModel):
    counter_teams: int 
    pages: int
    statuses_response: list[StatusResponse]    

#Types
class TypeBody(BaseModel):
    type_name: str

class TypeResponse(BaseModel):
    id: int
    type_name: str
    created_date: str

class AllTypesResposne(BaseModel):
    counter_teams: int 
    pages: int
    types_response: list[TypeResponse]    





