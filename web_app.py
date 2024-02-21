import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

# Function to create a sidebar based on the selected tab
def create_sidebar(tab):
    if tab == 'On-Off +/- Metrics w/ Season Stats':
        min_games = st.sidebar.slider('Select Minimum Number Games Played', 0, 15, 10)
        years = st.sidebar.selectbox('Select Seasons', ('All', '2021', '2022', '2023'))
        positions = st.sidebar.selectbox('Select Positions', ('All', 'Cutter', 'Handler', 'Defender'))
        teams = st.sidebar.selectbox('Select Team', tuple(team_options))
        return min_games, years, positions, teams
    elif tab == 'Mixed Effects Model Metrics w/ Career Stats':
        min_games1 = st.sidebar.slider('Select Minimum Number Games Played', 0, 100, 50)
        positions1 = st.sidebar.selectbox('Select Positions', ('All', 'Cutter', 'Handler', 'Defender'), key='x')
        return min_games1, positions1

@st.cache_data
def data_upload():
    df1 = pd.read_csv('final_dataframe.csv')
    df2 = pd.read_csv('final_df_career.csv')
    df1 = df1[df1['year']>=2021]

    df1['year'] = df1['year'].astype(str)
    df2['year'] = df1['year'].astype(str)

    df1.rename(columns = {'predicted position' : 'Position', 'name' : 'Name', 'year': 'Year',
                         'gamesPlayed': 'Games Played', 'goals': 'Goals', 'assists': 'Assists', 
                         'blocks' : 'Blocks', 'o_point_on_off_rating': 'Offensive On-Off +/-',
                         'd_point_on_off_rating':'Defensive On-Off +/-', 'total_on_off_rating': 
                         'Total On-Off +/-', 'teams': 'Team', 'oPointsPlayed': 'Offensive Points',
                           'dPointsPlayed': 'Defensive Points'}, inplace = True)
    
    df2.rename(columns = {'position' : 'Position', 'name' : 'Name', 
                        'gamesPlayed': 'Games Played', 'goals': 'Goals', 'assists': 'Assists', 
                        'blocks' : 'Blocks', 'teams': 'Team', 'oPointsPlayed': 'Offensive Points',
                        'dPointsPlayed': 'Defensive Points', 'goal_rating' : 'Goal Rating',
                        'assist_rating': 'Assist Rating', 'oeff_rating': 'oEfficiency Rating', 'composite_rating' : 
                        'Composite Rating', 'block_rating': 'Block Rating'}, inplace = True)
    
    df1 = df1[['Name', 'Position', 'Year', 'Team', 'Games Played', 'Goals', 'Assists', 'Blocks','Offensive Points', 'Defensive Points', 'Offensive On-Off +/-',
             'Defensive On-Off +/-', 'Total On-Off +/-']]
    df2 = df2[['Name', 'Position', 'Games Played', 'Goals', 'Assists', 'Blocks', 'oEfficiency', 'Offensive Points', 'Defensive Points', 'Goal Rating',
             'Assist Rating', 'Block Rating', 'oEfficiency Rating', 'Composite Rating']]
    return df1, df2


df1, df2 = data_upload()
team_options = ['All']+list(set(df1['Team']))
team_options = [item for item in team_options if ',' not in item]


# Create sidebars for each tab
with st.sidebar:
    tab_selection = st.radio("Select a tab", ['On-Off +/- Metrics w/ Season Stats', 'Mixed Effects Model Metrics w/ Career Stats'])

# Display the selected tab
if tab_selection == 'On-Off +/- Metrics w/ Season Stats':
    # tab1, tab2 = st.tabs(['On-Off +/- Metrics w/ Season Stats', 'Mixed Effects Model Metrics w/ Career Stats'])
    min_games, years, positions, teams = create_sidebar(tab_selection)

    # with tab1:
    st.header("On-Off +/- Metrics w/ Season Stats")
    st.dataframe(data=df1[(df1['Games Played'] >= min_games) & ((years == 'All') | (df1['Year'] == years)) &
                            ((positions == 'All') | (df1['Position'] == positions)) &
                            ((teams == 'All') | (df1['Team'] == teams))], width = 1500, height = 800, hide_index = True)
        
elif tab_selection == 'Mixed Effects Model Metrics w/ Career Stats':
    # tab1, tab2 = st.tabs(['On-Off +/- Metrics w/ Season Stats', 'Mixed Effects Model Metrics w/ Career Stats'])
    min_games1, positions1 =create_sidebar(tab_selection)

    # with tab2:
    st.header("Mixed Effects Model Metrics w/ Career Stats")
    st.dataframe(data=df2[(df2['Games Played'] >= min_games1) &
                        ((positions1 == 'All') | (df2['Position'] == positions1))], 
                        width = 1500, height = 800, hide_index = True)


