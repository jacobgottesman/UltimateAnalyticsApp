import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

st.set_page_config(layout='wide')

# Function to create a sidebar based on the selected tab
def create_sidebar(tab):
    if tab == 'On-Off +/- Metrics w/ Season Stats':
        min_games = st.sidebar.slider('Select Minimum Number Games', 0, 15, 10)
        min_o_points = st.sidebar.slider('Select Minimum Offensive Points Per Game', 0, 20, 0)
        min_d_points = st.sidebar.slider('Select Minimum Defensive Points Per Game', 0, 20, 0)
        years = st.sidebar.selectbox('Select Seasons', ('All', '2021', '2022', '2023', '2024'))
        positions = st.sidebar.selectbox('Select Positions', ('All', 'Cutter', 'Handler', 'Defender'))
        teams = st.sidebar.selectbox('Select Team', tuple(team_options))
        return min_games, min_o_points, min_d_points, years, positions, teams
    elif tab == 'Mixed Effects Model Metrics w/ Career Stats':
        min_games1 = st.sidebar.slider('Select Minimum Number Games', 0, 100, 50)
        min_o_points = st.sidebar.slider('Select Minimum Offensive Points Per Game', 0, 20, 0)
        min_d_points = st.sidebar.slider('Select Minimum Defensive Points Per Game', 0, 20, 0)
        positions1 = st.sidebar.selectbox('Select Positions', ('All', 'Cutter', 'Handler', 'Defender'), key='x')
        return min_games1, min_o_points, min_d_points, positions1

@st.cache_data
def data_upload():
    df1 = pd.read_csv('final_yearly_df_aug_24.csv')
    df2 = pd.read_csv('career_stats_w_ratings_aug_24.csv')
    df1 = df1[df1['year']>=2021]

    df1['year'] = df1['year'].astype(str)
    df2['year'] = df1['year'].astype(str)

    df1.rename(columns = {'position' : 'Position', 'name' : 'Name', 'year': 'Year',
                         'gamesPlayed': 'Games', 'goals': 'Goals', 'assists': 'Assists', 
                         'blocks' : 'Blocks', 'o_point_on_off_rating': 'Offensive On-Off +/-',
                         'd_point_on_off_rating':'Defensive On-Off +/-', 'total_on_off_rating': 
                         'Total On-Off +/-', 'teams': 'Team', 'oPointsPlayed': 'Offensive Points',
                           'dPointsPlayed': 'Defensive Points'}, inplace = True)
    
    df2.rename(columns = {'position' : 'Position', 'name' : 'Name', 
                        'gamesPlayed': 'Games', 'goals': 'Goals', 'assists': 'Assists', 
                        'blocks' : 'Blocks', 'teams': 'Team', 'oPointsPlayed': 'Offensive Points',
                        'dPointsPlayed': 'Defensive Points', 'goal_rating' : 'Goal Rating',
                        'assist_rating': 'Assist Rating', 'oeff_rating': 'oEfficiency Rating', 'composite_rating' : 
                        'Composite Rating', 'block_rating': 'Block Rating'}, inplace = True)
    
    df1 = df1[['Name', 'Position', 'Year', 'Team','Games', 'Total On-Off +/-','Offensive On-Off +/-','Defensive On-Off +/-',
                'Offensive Points', 'Defensive Points', 'Goals', 'Assists', 'Blocks']]
    df2 = df2[['Name', 'Position', 'Games', 'Composite Rating', 'Goal Rating','Assist Rating', 'Block Rating', 
               'oEfficiency Rating','Goals', 'Assists', 'Blocks', 'oEfficiency', 'Offensive Points', 
               'Defensive Points'
              ]]
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
    min_games, min_o_points, min_d_points,  years, positions, teams = create_sidebar(tab_selection)
    
    # changing index to have name (year) pinned on left
    df1['Name (Year)']= df1.apply(lambda row: str(row['Name'] + ' ('+row['Year']+')'), axis =1)
    df1.index = df1['Name (Year)']
    df1 = df1[((years == 'All') | (df1['Year'] == years))]
    df1.drop(columns = ['Name', 'Year', 'Name (Year)'], inplace = True)

    # with tab1:
    st.header("On-Off +/- Metrics w/ Season Stats")
    st.dataframe(data=df1[(df1['Games'] >= min_games) & (df1['Offensive Points']>= min_o_points) & 
                          (df1['Defensive Points'] >= min_d_points) &
                            ((positions == 'All') | (df1['Position'] == positions)) &
                            ((teams == 'All') | (df1['Team'] == teams))], width = 1500, height = 800)
    
    text = '''This project was created by Jacob Gottesman with the mentorship of Dr. Eric Gerber.  
    The data in this project was gathered through the AUDL stats API along with the UFA webiste.  '''
    st.markdown(text)
    poster = "https://pbs.twimg.com/media/GK0wqkgaIAQmY-4?format=jpg&name=4096x4096"
    st.markdown("View more info on this project: [poster](%s)" % poster)
    linkedin = "https://www.linkedin.com/in/jacob-gottesman-neu/"
    st.markdown("Linkedin: [link](%s)" % linkedin)
        

elif tab_selection == 'Mixed Effects Model Metrics w/ Career Stats':
    # tab1, tab2 = st.tabs(['On-Off +/- Metrics w/ Season Stats', 'Mixed Effects Model Metrics w/ Career Stats'])
    min_games1, min_o_points, min_d_points, positions1 =create_sidebar(tab_selection)

    # changing index to name to have that column as pinned left column
    df2.index = df2['Name']
    df2.drop(columns = ['Name'], inplace = True)

    # with tab2:
    st.header("Mixed Effects Model Metrics w/ Career Stats")
    st.dataframe(data=df2[(df2['Games'] >= min_games1) &( df2['Offensive Points']>= min_o_points) & 
                          (df2['Defensive Points'] >= min_d_points) &
                        ((positions1 == 'All') | (df2['Position'] == positions1))], 
                        width = 1500, height = 800)

    text = '''This project was created by Jacob Gottesman with the mentorship of Dr. Eric Gerber.  
    The data in this project was gathered through the AUDL stats API along with the UFA webiste.  '''
    st.markdown(text)
    poster = "https://pbs.twimg.com/media/GK0wqkgaIAQmY-4?format=jpg&name=4096x4096"
    st.markdown("View more info on this project: [poster](%s)" % poster)
    linkedin = "https://www.linkedin.com/in/jacob-gottesman-neu/"
    st.markdown("Linkedin: [link](%s)" % linkedin)
 
