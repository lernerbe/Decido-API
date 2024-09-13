from src.models.users import TeamBody,TeamResponse
from src.utils.postgres_connector import PostgresConnector

class Team:

    @staticmethod
    def get_team_by_id(team_id:int) -> TeamResponse:
        try:
            db_connector = PostgresConnector()
            result = db_connector.select_query("""          
                SELECT
                    teams.id,
                    teams.team_name,
                    teams.created_date
                FROM issac_app.teams teams
                WHERE 
                    1=1     
                AND teams.id=  %(team_id)s""",{"team_id":team_id})
            db_connector.close_connection()

            if result.empty:
                raise Exception(f"Error team_id {team_id} doesn't exist")

            #Normalize date to string
            result["created_date"] = result["created_date"].astype(str)
            return result.to_dict(orient='records')[0]

        except Exception as e:
            db_connector.close_connection()
            print(e)
            raise Exception(f"Error in services/teams/get_team_by_id.py: \n {e}")
        

    @staticmethod
    def create_new_team(team_body:TeamBody) -> TeamResponse:      
        try: 
            team_name = team_body.model_dump(mode="unchanged")["team_name"]
            db_connector = PostgresConnector()

            new_team_body = db_connector.insert_query_regular("issac_app","teams",coulmns=["team_name"],insert_values=[[team_name]])
            db_connector.close_connection


            new_team_body["created_date"] = new_team_body["created_date"].astype(str)
            print(new_team_body)
            return new_team_body.to_dict(orient='records')[0]


        except Exception as e:
            db_connector.close_connection()
            print(e)
            raise Exception(f"Error in services/teams/create_new_team.py: \n {e}")
        
    @staticmethod 
    def udpate_team_by_id(team_id:int,team_body:TeamBody)-> TeamResponse:
        try:   
            new_team_name = team_body.model_dump(mode="unchanged")["team_name"]
            db_connector = PostgresConnector()
            update_team_body = db_connector.update_query("issac_app","teams",{"team_name":new_team_name},f"id = {team_id}")

            db_connector.close_connection()

            #Normalized df before response
            update_team_body["created_date"] = update_team_body["created_date"].astype(str)

            print(update_team_body)
            return update_team_body.to_dict(orient='records')[0]


        except Exception as e:
            db_connector.close_connection()
            print(e)
            raise Exception(f"Error in services/teams/udpate_team_by_id.py: \n {e}")
    
    @staticmethod
    def delete_team_by_id(team_id:int):
        try:       
            db_connector = PostgresConnector()
            db_connector.execute_query("DELETE FROM issac_app.teams WHERE id = %(team_id)s",{"team_id":team_id},commit=True)
            db_connector.close_connection()
            print(f"team {team_id} deleted successfully")
            return f"team {team_id} deleted successfully"
        except Exception as e:
            db_connector.close_connection()
            print(e)
            raise Exception(f"Error in services/team/delete_team_by_id.py: \n {e}")