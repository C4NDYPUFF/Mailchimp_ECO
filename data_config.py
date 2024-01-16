import mailchimp_marketing as MailchimpMarketing 
from mailchimp_marketing.api_client import ApiClientError
import streamlit as st 

api_key = st.secrets['API_KEY']
data_center = api_key.split('-')[-1]

client = MailchimpMarketing.Client()
client.set_config({
    "api_key": api_key,
    "server": data_center
})

try:
    response = client.reports.get_all_campaign_reports()
except ApiClientError as error:
    print("Error: {}".format(error.text))

# for i in range(1,10):
#     print(response['reports'][i]['id'],'and', response['reports'][i]['campaign_title'])

try:
    campaign_id = "6948b8f083"  # Corrected campaign ID
    response = client.reports.get_campaign_report(campaign_id)
except ApiClientError as error:
    print("Error: {}".format(error.text))


opens_metrics = response['opens']
emails_sent = response['emails_sent']
stats_campaing = response['list_stats']

try:
    list_id = "e8f8d15f9f"  # Corrected campaign ID
    response = client.lists.get_list(list_id)
    # print(response)
except ApiClientError as error:
    print("Error: {}".format(error.text))


stats = response['stats']

print(stats)