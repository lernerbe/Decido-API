from fastapi import APIRouter,Body,HTTPException,Response,status,Depends,Query,Path
import pandas as pd #to remove
from typing import Annotated
from src.models.users import UserBody,UserResponse,AllUsersResposne,TeamBody,TeamResponse,UserFilter,AllTeamsResposne
from src.routers.auth import get_current_user
from src.services.users.crud_user import User
from src.services.teams.crud_team import Team


router = APIRouter(prefix="/leads", tags=["leads_statuses_and_types"])

################################## STATUSES ####################################

# Get all users with pagination
@router.post("/statuses")
def get_users(user:Annotated[dict,Depends(get_current_user)], page: int = Query(default=1,ge=1), limit: int = Query(default=10,ge=5,le=50),search:str=None,filter:UserFilter=None) -> AllUsersResposne | list[UserResponse]: 
    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:
        from src.services.users.get_all_users import get_users_by_search_and_filter,get_counter_users_by_search_and_filter

        users_response = get_users_by_search_and_filter(page,limit,search,filter)

        if page == 1:
            counter_users = int(get_counter_users_by_search_and_filter(search,filter))
            print(counter_users)
            return {
                "counter_users": counter_users,
                "pages": int(counter_users/limit) + (1 if (counter_users%limit > 0) else 0),
                "users_response": users_response.to_dict(orient='records') }
        else:
            return users_response.to_dict(orient='records') 

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in get_users: {e}"
            ) 


# Get user by id
@router.get("/statuses/{user_id}")
def get_user(user:Annotated[dict,Depends(get_current_user)],user_id: int) -> UserResponse: 

    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:
        return User.get_user_by_id(user_id)
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in get_user: {e}"
            ) 

# Create new user
@router.post("/statuses/add_status")
def create_user(user:Annotated[dict,Depends(get_current_user)],new_user_body: UserBody) -> UserResponse: 

    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:
        return User.create_new_user(new_user_body)
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in create user: {e}"
            ) 

# Update user by id
@router.put("/statuses/edit_status/{status_id}")
def update_user(user:Annotated[dict,Depends(get_current_user)],status_id: int,user_update_body: UserBody) -> UserResponse: 

    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:     
        return User.udpate_user_by_id(status_id,user_update_body)
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in update user: {e}"
            ) 

# Delete user by id
@router.delete("/statuses/delete_status/{status_id}")
def delete_user(user:Annotated[dict,Depends(get_current_user)],status_id: int) -> str: 

    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:     
        return User.delete_user_by_id(status_id)
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in delete user: {e}"
            ) 



################################## TYPES ####################################


# Get all teams with pagination
@router.get("/types")
def get_teams(user:Annotated[dict,Depends(get_current_user)], page: int = Query(default=1,ge=1), limit: int = Query(default=10,ge=5,le=50),search:str=None) : 
    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:
        from src.services.teams.get_all_teams import get_teams_by_search,get_counter_teams_by_search

        teams_response = get_teams_by_search(page,limit,search)
        print(teams_response)

        if page == 1:
            counter_teams = int(get_counter_teams_by_search(search))
            print(counter_teams)
            return {
                "counter_teams": counter_teams,
                "pages": int(counter_teams/limit) + (1 if (counter_teams%limit > 0) else 0),
                "teams_response": teams_response.to_dict(orient='records') }
        else:
            return teams_response.to_dict(orient='records') 

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in get_teams: {e}"
            ) 

# Get team by id
@router.get("/types/{type_id}")
def get_team(user:Annotated[dict,Depends(get_current_user)],type_id: int) -> TeamResponse: 
    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:
        return Team.get_team_by_id(type_id)
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in get_team: {e}"
            ) 


# Create new team
@router.post("/types/add_type")
def create_team(user:Annotated[dict,Depends(get_current_user)],team: TeamBody) -> TeamResponse: 
    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:
        return Team.create_new_team(team)
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in create_new_team: {e}"
            ) 

# Update team by id
@router.put("/types/edit_type/{type_id}")
def update_team(user:Annotated[dict,Depends(get_current_user)],type_id: int,team: TeamBody) -> TeamResponse: 
    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:
        return Team.udpate_team_by_id(type_id,team)
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in edit_team: {e}"
            ) 

# Delete team by id
@router.delete("/types/delete_type/{type_id}")
def delete_team(user:Annotated[dict,Depends(get_current_user)],type_id: int) -> Response: 
    print(user)
    if user is None or user.get("user_role") not in ["manager","admin"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials make sure you have admin permisson")
    try:
        return Team.delete_team_by_id(type_id)
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in delete_team: {e}"
            ) 