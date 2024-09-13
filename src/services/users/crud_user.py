from src.models.users import UserBody
from src.utils.postgres_connector import PostgresConnector
import pandas as pd

class User:

    @staticmethod
    def get_user_by_id(user_id:int):
        try:
            db_connector = PostgresConnector()
            result = db_connector.select_query("""          
                    SELECT
                        users.id,
                        users.first_name,
                        users.last_name,
                        teams.team_name,
                        users.email,
                        users.phone_number,
                        users.user_role,
                        users.user_status,
                        users.created_date
                    FROM issac_app.users users
                    LEFT JOIN issac_app.teams teams ON users.team_id = teams.id
                    WHERE 
                        1=1  
                    AND users.id=  %(user_id)s""",{"user_id":user_id})
            db_connector.close_connection()

            if result.empty:
                raise Exception(f"Error user_id {user_id} doesn't exist")

            #Normalize date to string
            result["created_date"] = result["created_date"].astype(str)
            return result.to_dict(orient='records')[0]

        except Exception as e:
            db_connector.close_connection()
            print(e)
            raise Exception(f"Error in services/users/get_user_by_id.py: \n {e}")
        

    @staticmethod
    def create_new_user(userBody:UserBody):      
        try: 
            user_df =  pd.DataFrame([userBody.model_dump(mode="unchanged")])
            db_connector = PostgresConnector()

            #get the team_id based on the team name
            team_id = db_connector.select_query("SELECT id FROM issac_app.teams WHERE team_name = %(team_name)s",{"team_name":user_df["team_name"].iloc[0]})
            if team_id.empty:
                raise Exception(f"Error team_name {user_df['team_name'].iloc[0]} doesn't exist")
            team_name = user_df["team_name"] #save team_name for the response body
            user_df.drop(columns=["team_name"],inplace=True)
            user_df['team_id'] = team_id['id']

            new_user_body = db_connector.insert_query_regular("issac_app","users",list(user_df.columns),[list(user_df.iloc[0])])
            db_connector.close_connection

            #Normalized df before response
            new_user_body.drop(columns=["team_id","user_password"],inplace=True)
            new_user_body["created_date"] = new_user_body["created_date"].astype(str)
            new_user_body['team_name'] = team_name

            print(new_user_body)
            return new_user_body.to_dict(orient='records')[0]


        except Exception as e:
            db_connector.close_connection()
            print(e)
            raise Exception(f"Error in services/users/create_new_user.py: \n {e}")
        
    @staticmethod 
    def udpate_user_by_id(user_id:int,userBody:UserBody):
        try:        
            user_df =  pd.DataFrame([userBody.model_dump(mode="unchanged")])
            db_connector = PostgresConnector()

            #get the team_id based on the team name
            team_id = db_connector.select_query("SELECT id FROM issac_app.teams WHERE team_name = %(team_name)s",{"team_name":user_df["team_name"].iloc[0]})
            if team_id.empty:
                raise Exception(f"Error team_name {user_df['team_name'].iloc[0]} doesn't exist")
            team_name = user_df["team_name"] #save team_name for the response body
            user_df.drop(columns=["team_name"],inplace=True)
            user_df['team_id'] = team_id['id']
            user_dict = user_df.to_dict(orient='records')[0]

            update_user_body = db_connector.update_query("issac_app","users",user_dict,f"id = {user_id}")

            db_connector.close_connection()

            #Normalized df before response
            update_user_body.drop(columns=["team_id","user_password"],inplace=True)
            update_user_body["created_date"] = update_user_body["created_date"].astype(str)
            update_user_body['team_name'] = team_name

            print(update_user_body)
            return update_user_body.to_dict(orient='records')[0]


        except Exception as e:
            db_connector.close_connection()
            print(e)
            raise Exception(f"Error in services/users/udpate_user_by_id.py: \n {e}")
    
    @staticmethod
    def delete_user_by_id(user_id:int):
        try:       
            db_connector = PostgresConnector()
            db_connector.execute_query("DELETE FROM issac_app.users WHERE id = %(user_id)s",{"user_id":user_id},commit=True)
            db_connector.close_connection()
            print(f"user {user_id} deleted successfully")
            return f"user {user_id} deleted successfully"
        except Exception as e:
            db_connector.close_connection()
            print(e)
            raise Exception(f"Error in services/users/delete_user_by_id.py: \n {e}")