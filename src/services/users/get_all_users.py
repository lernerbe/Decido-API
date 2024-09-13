from src.models.users import UserFilter
from src.utils.utils import create_filter_query,create_search_query
from src.utils.postgres_connector import PostgresConnector

def get_users_by_search_and_filter(page:int,limit:int,search:str=None,filter:UserFilter=None):
    try:
        bind_object = {"limit":limit, "offset":(page-1)*limit}

        main_query = """
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
        """

        if search is not None:
            serach_columns_list = ["first_name","last_name","email","phone_number"]
            main_query,bind_object = create_search_query(search,serach_columns_list,main_query,bind_object)

        if filter is not None: 
            print(filter)
            filter_dict = filter.model_dump(mode="unchanged")
            main_query,bind_object = create_filter_query(filter_dict,main_query,bind_object)


        db_connector = PostgresConnector()
        result = db_connector.select_query(f"{main_query} LIMIT %(limit)s  OFFSET %(offset)s ",bind_object)
        db_connector.close_connection()

        #Normalize date to string
        result["created_date"] = result["created_date"].astype(str)

        return result
    except Exception as e:
        db_connector.close_connection()
        print(e)
        raise Exception(f"Error in services/users/get_users_by_search_and_filter.py: \n {e}")
    


def get_counter_users_by_search_and_filter(search,filter):

    try:
        bind_object = {}

        main_query = """
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
        """

        if search is not None:
            serach_columns_list = ["first_name","last_name","email","phone_number"]
            main_query,bind_object = create_search_query(search,serach_columns_list,main_query,bind_object)

        if filter is not None: 
            print(filter)
            filter_dict = filter.model_dump(mode="unchanged")
            main_query,bind_object = create_filter_query(filter_dict,main_query,bind_object)


        db_connector = PostgresConnector()
        result = db_connector.select_query(f"SELECT COUNT(*) FROM ({main_query}) AS count_users",bind_object)
        db_connector.close_connection()

       
        return result.to_dict(orient='records')[0]["count"]
    except Exception as e:
        db_connector.close_connection()
        print(e)
        raise Exception(f"Error in services/users/get_counter_userss_by_search_and_filter.py: \n {e}")