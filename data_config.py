import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd


def get_mailchimp_data():
    api_key = st.secrets['API_KEY']
    data_center = api_key.split('-')[-1]

    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
        "server": data_center
    })

    try:
        campaign_id = "6948b8f083"  # Example campaign ID
        response = client.reports.get_campaign_report(campaign_id)
        opens_metrics = response['opens']
        emails_sent = response['emails_sent']
        bounces = response['bounces']
        clicks = response['clicks']
    except ApiClientError as error:
        st.error(f"Error fetching campaign data: {error.text}")
        return None, None, None , None

    try:
        list_id = "e8f8d15f9f"  # Example list ID
        response1 = client.lists.get_list(list_id)
        stats = response1['stats']
    except ApiClientError as error:
        st.error(f"Error fetching list data: {error.text}")
        return opens_metrics, emails_sent, bounces, clicks, None

    return opens_metrics, emails_sent, bounces, clicks, stats,

def refresh_data():
    return get_mailchimp_data()

# def get_landing_info():
#     connection = None
#     cursor = None
#     try:
#         # Establishing the connection
#         connection = mysql.connector.connect(
#             host=st.secrets['HOST'],
#             port=3306,
#             database=st.secrets['DATABASE'],
#             user=st.secrets['USER'],
#             password= st.secrets['PASSWORD']
#         )

#         # Executing the query
#         if connection.is_connected():
#             query = "SELECT * FROM ecomondo_landing_page;"
#             cursor = connection.cursor()
#             cursor.execute(query)
#             rows = cursor.fetchall()
#             column_names = [desc[0] for desc in cursor.description]

#             # Creating DataFrame from the fetched data
#             df = pd.DataFrame(rows, columns=column_names)
#             return df

#     except Error as e:
#         print("Error while connecting to MySQL", str(e))
#         return pd.DataFrame() # Returns an empty DataFrame in case of error

#     finally:
#         # Closing cursor and connection
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

def get_landing_info() -> pd.DataFrame:
    """Fetch landing page data from the database"""
    
    with mysql.connector.connect(
        host= '143.255.58.210',
        database = 'hfmexico_micrositios',
        user = 'hfmexico_micrositios',
        password = 'El]D.cE}?Yht',
        # ... other config      
    ) as connection:
        with connection.cursor() as cursor:
            query = "SELECT * FROM ecomondo_landing_page;"        
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                return pd.DataFrame(rows)  
            except mysql.connector.Error as e:
                logger.error("Error fetching data: %s", str(e))
                return pd.DataFrame() # empty DataFrame on failure
