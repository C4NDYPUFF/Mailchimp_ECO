import plotly_express as px
import pandas as pd
import streamlit as st
from data_config import refresh_data, get_landing_info
from data_email_list import merged_campaign_data
import requests
from io import StringIO

### Global variables 

camp_id = '6948b8f083'
ls_id = 'e8f8d15f9f'


id_url = ['be0f2e9d1a',
        'f167932088',
        '09f75c08c6',
        '38acaadc01',
        '0138607c14',
        '1eccc839b5',
        '1be18cbf8e',
        '832823e8fe']



# Ensure 'authenticated' key is initialized in session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def creds_entered():
    if st.session_state['user'].strip() == 'admin' and st.session_state['passwd'].strip() == 'admin':
        st.session_state['authenticated'] = True  # Fixed assignment operator
    else:
        st.session_state['authenticated'] = False
        st.error('Invalid Username/Password : :face_with_raised_eyebrow:')

def authenthicate_user():
    if not st.session_state['authenticated']:
        st.text_input(label='Username: ', value='', key='user', on_change=creds_entered)
        st.text_input(label='Password: ', value='', key='passwd', type='password', on_change=creds_entered)
        return False  # Return False immediately if not authenticated
    return True  # Return True if authenticated


if authenthicate_user():


    def main_app():
        st.set_page_config(
            page_title='Real time Mailchimp Report',
            page_icon=':coffee:',
            layout='wide'
        )


        # Initialize session state for data refresh
        if 'data_refreshed' not in st.session_state:
            st.session_state['data_refreshed'] = False

        # Button for refreshing data
        if st.button('Refresh Data'):
            st.session_state['data_refreshed'] = True

        # Fetch data and update session state
        if 'data_refreshed' not in st.session_state or st.session_state['data_refreshed']:
            try:
                # Unpack the returned values from refresh_data()
                opens_metrics, emails_sent, bounces, clicks, stats = refresh_data(camp_id, ls_id)
                clicks_table, emails_clicked = merged_campaign_data(camp_id, id_url)
                landing_info = get_landing_info()

                # Assign each value to the session state
                st.session_state['opens_metrics'] = opens_metrics
                st.session_state['emails_sent'] = emails_sent
                st.session_state['bounces'] = bounces
                st.session_state['stats'] = stats
                st.session_state['clicks'] = clicks
                st.session_state['landing_info'] = landing_info

                st.session_state['clicks_table'] = clicks_table
                st.session_state['emails_clicked'] = emails_clicked 
                st.session_state['data_refreshed'] = False
            except Exception as e:
                st.error(f"Error fetching data: {e}")
                return

        # Dashboard Title
        st.title('Dashboard report mailchimp for ecomondo exhibitors')

        # Ensure data is available before displaying
        if 'opens_metrics' in st.session_state:
            kpi1, kpi2, kpi3 = st.columns(3)
            # Access opens_metrics from st.session_state
            opens_metrics = st.session_state['opens_metrics']
            emails_sent = st.session_state['emails_sent']
            bounces = st.session_state['bounces']
            stats = st.session_state['stats']
            clicks = st.session_state['clicks']
            clicks_table = st.session_state['clicks_table']
            emails_clicked = st.session_state['emails_clicked']


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
    main_app()