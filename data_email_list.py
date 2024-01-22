import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import streamlit as st
import pandas as pd 
from concurrent.futures import ThreadPoolExecutor, as_completed



def merged_campaign_data():
    campaign_id = "6948b8f083" 
    api_key = st.secrets['API_KEY']
    # Initialize Mailchimp client
    data_center = api_key.split('-')[-1]
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
        "server": data_center
    })

    # Function to fetch subscriber info
    def fetch_data(link_id):
        try:
            response = client.reports.get_subscribers_info(campaign_id, link_id, count=100)
            return [{'Email': r.get('email_address'), 'Clicks': r.get('clicks'), 'URL': url} for r in response['members'] for url in df1['URL'].unique()]
        except ApiClientError as error:
            print(f"Error with link {link_id}: {error.text}")
            return []

    try:
        # Fetch URL and total clicks
        response = client.reports.get_campaign_click_details(campaign_id, count=1000)
        url_data = [{'URL': r.get('url'), 'Total Clicks': r.get('total_clicks')} for r in response['urls_clicked']]
        df1 = pd.DataFrame(url_data)
    except ApiClientError as error:
        print(f"Error fetching URL data: {error.text}")
        return None, None

    try:
        id_url = ['be0f2e9d1a',
        'f167932088',
        '09f75c08c6',
        '38acaadc01',
        '0138607c14',
        '1eccc839b5',
        '1be18cbf8e',
        '832823e8fe']
        # Fetch subscriber info
        data = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_link = {executor.submit(fetch_data, link): link for link in id_url}
            for future in as_completed(future_to_link):
                data.extend(future.result())

        df2 = pd.DataFrame(data) if data else None
    except ApiClientError as error:
        print(f"Error fetching subscriber info: {error.text}")
        return df1, None

    return df1, df2
