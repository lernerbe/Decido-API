from src.utils.utils import create_search_query
from src.utils.postgres_connector import PostgresConnector

def get_teams_by_search(page:int,limit:int,search:str=None):
    try:
        bind_object = {"limit":limit, "offset":(page-1)*limit}

        main_query = """
            SELECT
                teams.id,
                teams.team_name,
                teams.created_date
            FROM issac_app.teams teams
            WHERE 
                1=1       
        """

        if search is not None:
            serach_columns_list = ["team_name"]
            main_query,bind_object = create_search_query(search,serach_columns_list,main_query,bind_object)

        db_connector = PostgresConnector()
        result = db_connector.select_query(f"{main_query} LIMIT %(limit)s  OFFSET %(offset)s ",bind_object)
        db_connector.close_connection()

        #Normalize date to string
        result["created_date"] = result["created_date"].astype(str)

        return result
    except Exception as e:
        db_connector.close_connection()
        print(e)
        raise Exception(f"Error in services/teams/get_teams_by_search.py: \n {e}")
    


def get_counter_teams_by_search(search):

    try:
        bind_object = {}

        main_query = """
            SELECT
                teams.id,
                teams.team_name,
                teams.created_date
            FROM issac_app.teams teams
            WHERE 
                1=1       
        """

        if search is not None:
            serach_columns_list = ["team_name"]
            main_query,bind_object = create_search_query(search,serach_columns_list,main_query,bind_object)


        db_connector = PostgresConnector()
        result = db_connector.select_query(f"SELECT COUNT(*) FROM ({main_query}) AS count_teams",bind_object)
        db_connector.close_connection()

       
        return result.to_dict(orient='records')[0]["count"]
    except Exception as e:
        db_connector.close_connection()
        print(e)
        raise Exception(f"Error in services/teams/get_counter_teamss_by_search_and_filter.py: \n {e}")
    
