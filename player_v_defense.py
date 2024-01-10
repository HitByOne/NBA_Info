import pandas as pd
import os
import streamlit as st

player_info_versues_defense_sheet_id = '1-LJBuRyoTfp38xLM_6TQ7fUOHgbEnNVh'
todays_games_sheet_id = '1-Din9sCqXU7KGoRPenl8zX_KhBkFVLUg'
player_log_id = '1-S9tHnbGZmU_bvif79po3Wa26zykbc0G'

player_info_versues_defense = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{player_info_versues_defense_sheet_id}/export?format=csv")
todays_games = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{todays_games_sheet_id}/export?format=csv")
player_log  = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{player_log_id}/export?format=csv")

# Remove text after the dot in column names
# %%

# Set page configuration
st.set_page_config(layout="wide")

# Define columns to format
columns_to_format = ['Player Averages', 'Line', 'Defensive Averages']
columns_to_format_4 = ['Minutes']
columns_to_format_5 = ['Last 1','Last 2','Last 3','Last 4','Last 5']

# Schedule #
st.markdown('<h4 style="color:blue;">Schedule</h4>', unsafe_allow_html=True)
st.dataframe(todays_games.set_index(todays_games.columns[0]))

# Player Props #
# Sidebar with dropdown filter
st.markdown('<h4 style="color:blue;">Player Props</h4>', unsafe_allow_html=True)
prop_filter = st.selectbox('Select Prop:', player_info_versues_defense['Prop'].unique())

# Filter the DataFrame based on the selected Prop
filtered_df = player_info_versues_defense[player_info_versues_defense['Prop'] == prop_filter]
filtered_df[columns_to_format] = filtered_df[columns_to_format].applymap(lambda x: '{:.1f}'.format(x))
filtered_df[columns_to_format_5] = filtered_df[columns_to_format_5].applymap(lambda x: '{:.0f}'.format(x))

st.dataframe(filtered_df.set_index(filtered_df.columns[0]))

# Player Log #
st.markdown(f'<h4 style="color:blue;">Player Log</h4>', unsafe_allow_html=True)
selected_team = st.selectbox("Select a Team:", sorted(player_log['Team'].unique()))

# Filter players based on the selected team
players_in_selected_team = sorted(player_log[player_log['Team'] == selected_team]['Player'].unique())

# Create a dropdown menu for selecting a player in the selected team
selected_player = st.selectbox("Select a Player:", players_in_selected_team)

# Filter the player_log table based on the selected player and team
filtered_player_log = player_log[
    (player_log['Player'] == selected_player) &
    (player_log['Team'] == selected_team)
]

filtered_player_log[columns_to_format_4] = filtered_player_log[columns_to_format_4].applymap(lambda x: '{:.1f}'.format(x))

st.dataframe(filtered_player_log.set_index(filtered_player_log.columns[0]))


# Opposing Team  Player Log # 
st.markdown(f'<h4 style="color:blue;">Players Against Opponent</h4>', unsafe_allow_html=True)
selected_opponent = st.selectbox("Select Opponent:", sorted(player_log['Opponent'].unique()))

# Create a dropdown menu for selecting a position
selected_position = st.selectbox("Select Position:", sorted(player_log['Position'].unique()))

# Create a checkbox for filtering by Starter
is_starter = st.checkbox("Show only Starters")



# Apply filters based on user input
filtered_player_log = player_log[
        (player_log['Opponent'] == selected_opponent) &
        (player_log['Starter'] == 'Y' if is_starter else True) &
        (player_log['Position'] == selected_position)
    ]
filtered_player_log['Date'] = pd.to_datetime(filtered_player_log['Date']).dt.strftime('%m/%d/%Y')

filtered_player_log[columns_to_format_4] = filtered_player_log[columns_to_format_4].applymap(lambda x: '{:.1f}'.format(x))
st.dataframe(filtered_player_log.set_index(filtered_player_log.columns[0]))
