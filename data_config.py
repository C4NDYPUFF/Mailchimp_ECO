import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import streamlit as st

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
        stats_campaing = response['list_stats']
    except ApiClientError as error:
        st.error(f"Error fetching campaign data: {error.text}")
        return None, None, None

    try:
        list_id = "e8f8d15f9f"  # Example list ID
        response1 = client.lists.get_list(list_id)
        stats = response1['stats']
    except ApiClientError as error:
        st.error(f"Error fetching list data: {error.text}")
        return opens_metrics, emails_sent, stats_campaing, None

    return opens_metrics, emails_sent, stats_campaing, stats

def refresh_data():
    return get_mailchimp_data()
