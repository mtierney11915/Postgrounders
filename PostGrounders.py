#Imports
import pandas as pd
import streamlit as st
import altair as alt

#Set Page Configuration
st.set_page_config(
    page_title="Post University Baseball Ground Ball Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":baseball:")
st.title("Post U Baseball Ground Ball Analytics")
alt.themes.enable("dark")
col= st.columns([5, 2])  # Divide the space into three equal columns

#Read in Data
#df=pd.read_excel(r'C:\Users\Matt Tierney\OneDrive\Post U Baseball\Post Ground Ball Data.xlsx')
df=pd.read_excel('Post Ground Ball Data.xlsx')
#Subset Game Column
game_column = df['Game'].tolist()
gamelist=df['Game'].unique()

#Subset Pitcher Column
pitcher_column = df['Pitcher ']
pitcherlist=df['Pitcher '].unique()

#Subset Pitch Column
pitch_column = df['Pitch Type'].tolist()
pitchlist=df['Pitch Type'].unique()

#Subset Opponent Column
opp_column = df['Opponent'].tolist()
opplist=df['Opponent'].unique()

#Create Sidebar
with st.sidebar:
    st.title('Filter by Individual Games or Opponents:')
    gamechoice=st.multiselect('Select a game(s)',gamelist)
    oppchoice=st.multiselect('Select specific opponents',opplist)
    st.title('Or Filter Here By Pitcher and/or Pitch Type')
    pitcherselects=st.multiselect('Select a pitcher(s)',pitcherlist)
    pitchselect=st.multiselect('Select a pitch',pitchlist)

#Create Subset off of user input
selected_games_df = df[df['Game'].isin(gamechoice)]
opponentsdf=df[df['Opponent'].isin(oppchoice)]
pitchdf=df[df['Pitch Type'].isin(pitchselect)]
pitcherdf=df[df['Pitcher '].isin(pitcherselects)]

#Choose Columns for user inputs
cols=['Position','Lane','Hop','Hands','Arm Slot','Footwork','Play At']

#Overall Dashboard Value Percentages
def calc_percentages(df):
    uni_value_per = {} #Empty Dict
    for column in df.columns:
        value_counts = df[column].value_counts()
        total_count = df[column].count()
        percentages = value_counts / total_count
        uni_value_per[column] = percentages
    return uni_value_per

#Percentages for games selected by user
def gameselect(seldf):
    selectper = {}
    for column in seldf:
        val_counts = seldf[column].value_counts()
        tot_count = seldf[column].count()
        pers = val_counts / tot_count
        selectper[column] = pers
    return selectper

#Functions
def oppselect(oppdf):
    oppsper = {}
    for column in oppdf:
        val_counts = oppdf[column].value_counts()
        tot_count = oppdf[column].count()
        pers = val_counts / tot_count
        oppsper[column] = pers
    return oppsper

def pitchselect(pitchdf):
    pitchdict = {}
    for column in pitchdf:
        val_counts = pitchdf[column].value_counts()
        tot_count = pitchdf[column].count()
        pers = val_counts / tot_count
        pitchdict[column] = pers
    return pitchdict

def pitcherselect(pitcherdf):
    pitcherdict = {}
    for column in pitcherdf:
        val_counts = pitcherdf[column].value_counts()
        tot_count = pitcherdf[column].count()
        pers = val_counts / tot_count
        pitcherdict[column] = pers
    return pitcherdict

#Call Functions
uvp=calc_percentages(df)
svp=gameselect(selected_games_df)
ovp=oppselect(opponentsdf)
pvp=pitchselect(pitchdf)
pitchervp=pitcherselect(pitcherdf)

#Middle Dashboard
with col[0]:
    #If statements for game selection
    if gamechoice:
        st.header('Ground Balls for Selected Games')
        game_sel_coms=st.multiselect("Select Specific Data Point(s):",cols)
        if game_sel_coms:
            for column in game_sel_coms:
                if column in svp:
                    st.subheader(f'{column} Summary:')
                    percentages_formatted = svp[column].map(lambda x: '{:.2%}'.format(x))
                    st.write(percentages_formatted)
        else:
            for column in cols:
                if column in svp:
                    st.subheader(f'{column} Summary:')
                    percentages_formatted = svp[column].map(lambda x: '{:.2%}'.format(x))
                    st.write(percentages_formatted)
        st.subheader('Raw Data For Selected Game(s)')
        st.dataframe(selected_games_df)
    elif oppchoice:
        st.header('Ground Ball Summary For Selected Opponent(s)')
        selected_columns = st.multiselect("Select Specific Data Point(s):", cols)
        if selected_columns:
            for column in selected_columns:
                if column in ovp:
                    st.subheader(f'{column} Summary:')
                    percentages_formatted = ovp[column].map(lambda x: '{:.2%}'.format(x))
                    st.write(percentages_formatted)
        else:
            for column in cols:
                if column in ovp:
                    st.subheader(f'{column} Summary:')
                    percentages_formatted = ovp[column].map(lambda x: '{:.2%}'.format(x))
                    st.write(percentages_formatted)
    #elif pitchselect:
        #st.header('Ground Ball Summary For Selected Pitch Type(s)')
        #selected_columns = st.multiselect("Select Specific Data Point(s):", cols)
        #if selected_columns:
            #for column in selected_columns:
                #if column in pvp:
                    #st.subheader(f'{column} Summary:')
                    #percentages_formatted = pvp[column].map(lambda x: '{:.2%}'.format(x))
                    #st.write(percentages_formatted)
        #else:
            #for column in cols:
                #if column in pvp:
                    #st.subheader(f'{column} Summary:')
                    #percentages_formatted = pvp[column].map(lambda x: '{:.2%}'.format(x))
                    #st.write(percentages_formatted)
    elif pitcherselects:
        st.header('Ground Ball Summary For Selected Pitcher(s)')
        selected_columns = st.multiselect("Select Specific Data Point(s):", cols)
        if selected_columns:
            for column in selected_columns:
                if column in pitchervp:
                    st.subheader(f'{column} Summary:')
                    percentages_formatted = pitchervp[column].map(lambda x: '{:.2%}'.format(x))
                    st.write(percentages_formatted)
        else:
            for column in cols:
                if column in pitchervp:
                    st.subheader(f'{column} Summary:')
                    percentages_formatted = pitchervp[column].map(lambda x: '{:.2%}'.format(x))
                    st.write(percentages_formatted)
    else:
        st.header('Overall Ground Ball Dashboard')
        selected_columns = st.multiselect("Select Specific Data Point(s):", cols)
        if selected_columns:
            for column in selected_columns:
                if column in uvp:
                    st.subheader(f'{column} Summary:')
                    percentages_formatted = uvp[column].map(lambda x: '{:.2%}'.format(x))
                    st.write(percentages_formatted,text_align='Center')
        else:
            for column in cols:
                if column in uvp:
                    st.subheader(f'{column} Summary:')
                    percentages_formatted = uvp[column].map(lambda x: '{:.2%}'.format(x))
                    st.write(percentages_formatted)
        st.header('Overall Raw Data')
        st.dataframe(df)

    # Third Column Content
    with col[1]:
        st.header('Season Category Leaders')

        #Position High
        pos = df['Position'].value_counts().idxmax()
        poshigh=uvp['Position'].max()
        poshighper = f"{poshigh * 100:.0f}%"
        st.metric(f'Position Getting Most Grounders: {pos}',poshighper)

        #Lane
        ln = df['Lane'].value_counts().idxmax()
        lnhigh = uvp['Lane'].max()
        lnper = f"{lnhigh * 100:.0f}%"
        st.metric(f'Most Common Lane Is: {ln}',lnper)

        #Footwork
        hp = df['Footwork'].value_counts().idxmax()
        hphigh = uvp['Footwork'].max()
        hpper = f"{hphigh * 100:.0f}%"
        st.metric(f'Most Common Footwork Is: {hp}', hpper)

        #Arm Slot
        asl = df['Arm Slot'].value_counts().idxmax()
        aslhigh = uvp['Arm Slot'].max()
        aslper = f"{aslhigh * 100:.0f}%"
        st.metric(f'Most Arm Slot Is: {asl}', aslper)

        #Pitch Type
        pt = df['Pitch Type'].value_counts().idxmax()
        pthigh = uvp['Pitch Type'].max()
        ptper = f"{pthigh * 100:.0f}%"
        st.metric(f'Most Common Pitch: {pt}', ptper)

        #Error
        errors=df[df['Error (Y/N)'] == 'Yes']
        total_errors = errors.shape[0]
        st.metric('Total Infielder Errors Made:',total_errors)
