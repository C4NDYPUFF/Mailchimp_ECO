import plotly_express as px
import pandas as pd
import streamlit as st
from data_config import refresh_data
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
        kpi3.metric(label='Open Rate', value=f"{stats_campaing['open_rate']:.2f}", help='Average open rate in the campaign')

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
        kpi6.metric(label='Click Rate', value=f"{stats['click_rate']:.2f}")


        # Set a user-agent header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(st.secrets['EXCEL_FILE'], headers=headers)

        if response.status_code == 200:
            data = StringIO(response.text)
            df1 = pd.read_csv(data)
            # print(df)
        else:
            print(f"Failed to retrieve the file: HTTP Status Code {response.status_code}")

        # df1 = pd.read_csv(st.secrets['EXCEL_FILE'], encoding="ISO-8859-1")
        df1 = df1[['Email Address', 'Member Rating', 'Opens', 'GROUP']]

        st.sidebar.header('Please Filter Here')

        group = st.sidebar.multiselect(
            'Select the Group',
            options=df1['GROUP'].unique(),
            default=df1['GROUP'].unique()
        )

        df_selection = df1.query('GROUP == @group')
        st.title('Emails list for users subscribed')
        st.dataframe(df_selection)

# Run the main app function
main_app()
