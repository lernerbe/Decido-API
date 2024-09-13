def hello_world():
    return {"message":"Hello World"}




def testinsert_query():
    from utils.postgres_connector import PostgresConnector

    db_connector = PostgresConnector()
    # result = db_connector.insert_query_regular(schema="updater_service",table="updater_service_traffic_sources",coulmns=["traffic_source_name"],insert_values=[["Twitter"],["google"]])
    
    team_id = db_connector.select_query('SELECT id FROM issac_app.teams WHERE team_name = %(team_name)s',{"team_name":'Barak'})


    new_user = db_connector.insert_query_regular(
        ['first_name', 'last_name', 'email', 'user_password', 'phone_number', 'user_role', 'user_status', 'team_id'],
['yuval', 'maoz', 'yuval.maoz@gmail.com', 'Yuval123', '050-7518599', 'employee', 'active', 2])


    # result = db_connector.update_query(schema="updater_service",table="updater_service_traffic_sources",update_values={"traffic_source_name":"test"},update_condition="id IN (22,23)")
   
    print(team_id)
    db_connector.close_connection()
    print(team_id)
    # print(f"Inserted {len(df_fb_updater_logs)} rows to facebook_ciq.fb_updater_service_logs") # log

# testinsert_query()

import os
import sys
print(sys.path)
# testinsert_query()

# from src.routers.auth import create_access_token

# token = create_access_token(15,"test","test","test")
# print(token)


def clinet_conn_test():
    from src.utils.postgres_connector_new import exec_query 

    print(exec_query(sql="SELECT * FROM issac_app.teams",commit=True,return_data=True))


clinet_conn_test()
