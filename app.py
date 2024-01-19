import plotly_express as px
import pandas as pd
import streamlit as st
from data_config import refresh_data
from data_email_list import email_list_data
import requests
from io import StringIO

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

    # Refresh data if the button was clicked
    if st.session_state['data_refreshed']:
        try:
            opens_metrics, emails_sent, stats_campaing, stats = refresh_data()
            clicks_table = email_list_data()
            # Reset the flag after data is refreshed
            st.session_state['data_refreshed'] = False
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return

    # Dashboard Title
    st.title('Dashboard report mailchimp for ecomondo exhibitors')

    # Ensure data is available before displaying
    if 'opens_metrics' in locals():
        kpi1, kpi2, kpi3 = st.columns(3)

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

        kpi4.metric(label='Target Sub Rate', value=stats['target_sub_rate'], delta=int(stats['avg_sub_rate'])/10, help='Target number of subscription per month')
        kpi5.metric(label='Member Count', value=stats['member_count'], help='The Number of Active Members')
        kpi6.metric(label='Clicks', value=f"{stats['click_rate']:.2f}")

        st.sidebar.header('Please Filter Here')

        url = st.sidebar.multiselect(
            'Select Link',
            options=clicks_table['URL'].unique(),
            default=clicks_table['URL'].unique() 

        )
        df_selection = clicks_table.query('URL == @url')
        st.title('Emails clicked by users')
        st.dataframe(clicks_table)

# Run the main app function
main_app()
