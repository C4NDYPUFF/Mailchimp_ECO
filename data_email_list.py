import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import streamlit as st
import pandas as pd 

def email_list_data():
    api_key = st.secrets['API_KEY']
    data_center = api_key.split('-')[-1]

    client = MailchimpMarketing.Client()
    client.set_config({
    "api_key": api_key,
    "server": data_center
    })

    try:
        campaign_id = "6948b8f083"  
        response = client.reports.get_campaign_click_details(campaign_id, count=1000)
        data = [{'URL': r.get('url'), 'Total Clicks': r.get('total_clicks')} for r in response['urls_clicked']]
        df =pd.DataFrame(data)
        return df
    except ApiClientError as error:
        st.error(f"Error fetching list data: {error.text}")
        return None
