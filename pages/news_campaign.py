import plotly_express as px
import pandas as pd
import streamlit as st
from data_config import refresh_data, get_landing_info
from data_email_list import merged_campaign_data
import requests
from io import StringIO


### Globals

camp_id2 = 'b39e6761dc'
ls_id2 = 'f481663a5f'

id_url2 = ['e9a6d414de',
 '59aeea0c6a',
 '257b67873e',
 'd1683d6fa1',
 '4480a13acf',
 '1f50c2ec34',
 '6fed0c3237',
 'e563681523']



def additional_page():
    st.set_page_config(
        page_title='Real time Mailchimp Report',
        page_icon=':coffee:',
        layout='wide'
    )

    # Initialize session state for data refresh
    if 'data_refreshed_2' not in st.session_state:
        st.session_state['data_refreshed_2'] = False

    # Button for refreshing data
    if st.button('Refresh Data'):
        st.session_state['data_refreshed_2'] = True

    # Fetch data and update session state
    if 'data_refreshed_2' not in st.session_state or st.session_state['data_refreshed_2']:
        try:
            # Unpack the returned values from refresh_data()
            opens_metrics, emails_sent, bounces, clicks, stats = refresh_data(camp_id2, ls_id2)
            clicks_table, emails_clicked = merged_campaign_data(camp_id2, id_url2)
            landing_info = get_landing_info()

            # Assign each value to the session state
            st.session_state['opens_metrics_2'] = opens_metrics
            st.session_state['emails_sent_2'] = emails_sent
            st.session_state['bounces_2'] = bounces
            st.session_state['stats_2'] = stats
            st.session_state['clicks_2'] = clicks
            st.session_state['landing_info_2'] = landing_info

            st.session_state['clicks_table_2'] = clicks_table
            st.session_state['emails_clicked_2'] = emails_clicked
            st.session_state['data_refreshed_2'] = False
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return

    # Dashboard Title
    st.title('Dashboard report mailchimp for ecomondo exhibitors')

    # Ensure data is available before displaying
    if 'opens_metrics_2' in st.session_state:
        kpi1, kpi2, kpi3 = st.columns(3)
        # Access opens_metrics from st.session_state
        opens_metrics = st.session_state['opens_metrics_2']
        emails_sent = st.session_state['emails_sent_2']
        bounces = st.session_state['bounces_2']
        stats = st.session_state['stats_2']
        clicks = st.session_state['clicks_2']
        clicks_table = st.session_state['clicks_table_2']
        emails_clicked = st.session_state['emails_clicked_2']


        kpi1.metric(label='Total Opens', value=opens_metrics['opens_total'], help='Emails open in the last campaign')
        kpi2.metric(label='Unique Opens', value=opens_metrics['unique_opens'], help='New emails that open the newsletter')
        kpi3.metric(label='Open Rate', value=f"{opens_metrics['open_rate']:.2f}", help='Average open rate in the campaign')

        data = {
            'Count': [emails_sent, opens_metrics['opens_total']],
            'Categories': ['Emails Sent', 'Total Emails Open']
        }

        df = pd.DataFrame(data)
        fig = px.bar(df, x='Categories', y='Count', color='Categories')
        st.plotly_chart(fig, use_container_width=True)

        kpi4, kpi5, kpi6 = st.columns(3)

        kpi4.metric(label='Bounce email', value=bounces.get('hard_bounces'), help='Number of teh emails that have been bounce')
        kpi5.metric(label='Member Count', value=stats['member_count'], help='The Number of Active Members')
        kpi6.metric(label='Clicks', value=f"{clicks.get('clicks_total'):.2f}", help='Total of the clicks made by user')

        #     st.dataframe(clicks_table)
        st.title('Links that have been clicked')
        st.dataframe(clicks_table, use_container_width=True)
        st.title('Emails from the people that click')
        emails_clicked = emails_clicked.drop_duplicates(subset=['Email'])
        st.dataframe(emails_clicked, use_container_width=True)
        st.title('Emails from the landing')
        st.dataframe(landing_info, use_container_width=True)



# Run the main app function
additional_page()
