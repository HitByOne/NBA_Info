import pandas as pd
import os
import streamlit as st

player_info_versues_defense_sheet_id = '1-LJBuRyoTfp38xLM_6TQ7fUOHgbEnNVh'
todays_games_sheet_id = '1-Din9sCqXU7KGoRPenl8zX_KhBkFVLUg'
player_log_id = '1-S9tHnbGZmU_bvif79po3Wa26zykbc0G'
player_stats_id = '1-YNog3n-extsuV2AWmaFnxWJnG6CJVCi'
oneplusallstats_id = '1-YsxiFZUqtglhQ8e2GeQ9Od9At6xS2rU'
offensive_stats_id = '1-ZfYDUwq3V-b7ySJuFkKMJ85plH2MLXF'
defensive_stats_id = '1-_B-pCo2jv_6sR0wOPxvVyaQtYh9Zuim'

player_info_versues_defense = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{player_info_versues_defense_sheet_id}/export?format=csv")
todays_games = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{todays_games_sheet_id}/export?format=csv")
player_log  = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{player_log_id}/export?format=csv")
player_stats = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{player_stats_id}/export?format=csv")
oneplusallstats = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{oneplusallstats_id}/export?format=csv")
offensive_stats = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{offensive_stats_id}/export?format=csv")
defensive_stats = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{defensive_stats_id}/export?format=csv")
# Remove text after the dot in column names
# %%

# Set page configuration
st.set_page_config(layout="wide")

# Define columns to format
columns_to_format = ['Player Averages', 'Line', 'Defensive Averages']
columns_to_format_4 = ['Minutes']
columns_to_format_5 = ['Last 1','Last 2','Last 3','Last 4','Last 5']
columns_to_format_6 = ['Averages']
columns_to_format_7 = ['Three Points Made', 'Rebounds', 'Assists', 'Fouls', 'Steals', 'Turnovers', 'Block', 'Points', 'PA', 'PR', 'RA', 'PAR', 'DD', 'TD']
def home_page():
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

    ## Player Vs Opponent Log #
    player_info = player_info_versues_defense[player_info_versues_defense['Player'] == selected_player]

    # Check if player_info is empty
    if not player_info.empty:
        player_opponent = player_info[['Player', 'Opponent']].head(1)
        player_v_opponent = pd.merge(player_opponent, player_log, how='inner', on=['Player', 'Opponent'])

        # Convert the Date column to datetime format and remove T00:00:00
        player_v_opponent['Date'] = pd.to_datetime(player_v_opponent['Date']).dt.strftime('%Y-%m-%d')

        player_v_opponent[columns_to_format_4] = player_v_opponent[columns_to_format_4].applymap(lambda x: '{:.1f}'.format(x))
        st.markdown(f'<h4 style="color:blue;">{selected_player} vs. {player_opponent["Opponent"].iloc[0]}</h4>', unsafe_allow_html=True)

        # Sort DataFrame by Date
        player_v_opponent = player_v_opponent.sort_values(by='Date')

        st.dataframe(player_v_opponent.set_index(player_v_opponent.columns[0]))
    else:
        st.markdown(f'<h4 style="color:red;">{selected_player} has not played this team.</h4>', unsafe_allow_html=True)

    # Player Log #  
    # Filter the player_log table based on the selected player and team
    filtered_player_log = player_log[
        (player_log['Player'] == selected_player) &
        (player_log['Team'] == selected_team)
    ]

    # Convert the Date column to datetime format and remove T00:00:00
    filtered_player_log['Date'] = pd.to_datetime(filtered_player_log['Date']).dt.strftime('%Y-%m-%d')

    # Sort DataFrame by Date
    filtered_player_log = filtered_player_log.sort_values(by='Date', ascending=False)
    st.markdown(f'<h4 style="color:blue;">{selected_player} Previous Games</h4>', unsafe_allow_html=True)
    # Dropdown to dynamically filter the number of columns shown by date
    options = ["Last 1", "Last 3", "Last 5", "Last 10", "All Dates"]
    selected_option = st.selectbox("Select Last Games Played:", options)

    # Determine the number of columns to show based on the selected option
    if selected_option == "All Dates":
        num_columns_to_show = len(filtered_player_log)
    else:
        num_columns_to_show = int(selected_option.split()[-1])

    filtered_player_log_subset = filtered_player_log.head(num_columns_to_show)
    filtered_player_log_subset[columns_to_format_4] = filtered_player_log_subset[columns_to_format_4].applymap(lambda x: '{:.1f}'.format(x))
    st.dataframe(filtered_player_log_subset.set_index(filtered_player_log_subset.columns[0]))

    # Opposing Team Player Log #
    st.markdown(f'<h4 style="color:blue;">Players Against Opponent</h4>', unsafe_allow_html=True)
    selected_opponent = st.selectbox("Select Opponent:", sorted(player_log['Opponent'].unique()))
    selected_position = st.selectbox("Select Position:", sorted(player_log['Position'].unique()))

    options_opp = ["Last 1", "Last 3", "Last 5", "Last 10", "All Dates"]
    selected_option_opp = st.selectbox("Select Last Games Played:", options_opp, key="opp_games_selectbox")
    is_starter = st.checkbox("Show only Starters")
    # Filter the player log based on the selected opponent, starter, and position
    filtered_player_log_opp = player_log[
        (player_log['Opponent'] == selected_opponent)
        & (player_log['Starter'] == 'Y' if is_starter else True)
        & (player_log['Position'] == selected_position)
    ]
    filtered_player_log_opp['Date'] = pd.to_datetime(filtered_player_log_opp['Date']).dt.strftime('%Y-%m-%d')
    filtered_player_log_opp = filtered_player_log_opp.sort_values(by='Date', ascending=False)

    # Determine the number of columns to show based on the selected option
    if selected_option_opp == "All Dates":
        num_columns_to_show_opp = len(filtered_player_log_opp)
    else:
        num_columns_to_show_opp = int(selected_option_opp.split()[-1])
    filtered_player_log_opp[columns_to_format_4] = filtered_player_log_opp[columns_to_format_4].applymap(lambda x: '{:.1f}'.format(x))
    st.dataframe(filtered_player_log_opp.head(num_columns_to_show_opp).set_index(filtered_player_log_opp.columns[0]))
def about_page():


# Schedule #
    st.markdown('<h4 style="color:blue;">Schedule</h4>', unsafe_allow_html=True)
    st.dataframe(todays_games.set_index(todays_games.columns[0]))
# Dropdown filter for Position
    selected_prop_filter = st.selectbox("Filter by Position:", sorted(player_stats['Prop'].unique()))

# Filter the DataFrame based on the selected position
    filtered_player_stats = player_stats[player_stats['Prop'] == selected_prop_filter]

# Display the filtered DataFrame
    filtered_player_stats = filtered_player_stats.set_index('Rank').reset_index()
    filtered_player_stats[columns_to_format_6] = filtered_player_stats[columns_to_format_6].applymap(lambda x: '{:.1f}'.format(x))
    st.markdown('<h4 style="color:blue;">Player Ranks</h4>', unsafe_allow_html=True)
    st.dataframe(filtered_player_stats)

    cols_to_round = oneplusallstats.columns.difference(['Player', 'Position', 'Team', 'Games'])
    oneplusallstats[cols_to_round] = oneplusallstats[cols_to_round].round(1)

    oneplusallstats[columns_to_format_7] = oneplusallstats[columns_to_format_7].applymap(lambda x: '{:.1f}'.format(x))
    st.markdown('<h4 style="color:blue;">Players Who Average 1 Steal and Block</h4>', unsafe_allow_html=True)
    st.dataframe(oneplusallstats)

def team_page():

# Display the Schedule
    st.markdown('<h4 style="color:blue;">Schedule</h4>', unsafe_allow_html=True)
    st.dataframe(todays_games.set_index(todays_games.columns[0]))

# Filter by Prop for Offensive Stats
    st.markdown('<h4 style="color:blue;">Offensive Stats</h4>', unsafe_allow_html=True)
    selected_prop_filter_offensive = st.selectbox("Filter by Prop (Offensive):", sorted(offensive_stats['Prop'].unique()))
    filtered_offensive_stats = offensive_stats[offensive_stats['Prop'] == selected_prop_filter_offensive]
    filtered_offensive_stats[columns_to_format_6] = filtered_offensive_stats[columns_to_format_6].applymap(lambda x: '{:.1f}'.format(x))
    
    st.dataframe(filtered_offensive_stats)

# Filter by Prop for Defensive Stats
    st.markdown('<h4 style="color:blue;">Defensive Stats</h4>', unsafe_allow_html=True)
    selected_prop_filter_defensive = st.selectbox("Filter by Prop (Defensive):", sorted(defensive_stats['Prop'].unique()))
    filtered_defensive_stats = defensive_stats[defensive_stats['Prop'] == selected_prop_filter_defensive]
    filtered_defensive_stats[columns_to_format_6] = filtered_defensive_stats[columns_to_format_6].applymap(lambda x: '{:.1f}'.format(x))
    
    st.dataframe(filtered_defensive_stats)

def main():
    st.title("NBA Information")

    menu = ["Player V Defense", "Player Stats","Team Stats"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Player V Defense":
        home_page()
    elif choice == "Player Stats":
        about_page()
    elif choice == "Team Stats":
        team_page()

if __name__ == '__main__':
    main()
