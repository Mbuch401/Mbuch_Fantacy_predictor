import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('mbuch_fantasy_data.csv')

data = load_data()

# App title
st.title("⚽ Mbuch Fantasy - Team Efficiency Predictor")
st.write("Build your perfect 11 and get an efficiency score!")

# Formation selector
formations = {
    "4-4-2": {"GK": 1, "Defender": 4, "Midfielder": 4, "Attacker": 2},
    "4-3-3": {"GK": 1, "Defender": 4, "Midfielder": 3, "Attacker": 3},
    "3-5-2": {"GK": 1, "Defender": 3, "Midfielder": 5, "Attacker": 2},
    "4-2-3-1": {"GK": 1, "Defender": 4, "Midfielder": 5, "Attacker": 1}
}

formation = st.selectbox("Choose Formation:", list(formations.keys()))
st.write(f"Selected Formation: {formation}")

# Get player names for autocomplete
player_names = data['Player'].tolist()

# Create input boxes based on formation
selected_players = []
formation_setup = formations[formation]

for position, count in formation_setup.items():
    if position == "GK":
        position_name = "Goalkeeper"
    else:
        position_name = position
    
    st.subheader(f"{position_name}s ({count})")
    
    for i in range(count):  # Fixed indentation here
        player = st.selectbox(
            f"{position_name} {i+1}:",
            [""] + player_names,
            key=f"{position}_{i}"
        )
        if player:
            selected_players.append(player)

# Calculate team efficiency when all positions filled
if len(selected_players) == 11:
    if st.button("🔮 PREDICT TEAM EFFICIENCY"):
        # Get ratings for selected players
        team_data = data[data['Player'].isin(selected_players)]
        
        if len(team_data) == 11:
            avg_rating = team_data['Player_Rating'].mean()
            
            # Display results
            st.success(f"🎯 Team Efficiency Score: {avg_rating:.1f}%")
            
            if avg_rating >= 80:
                st.write("🔥 **ELITE TEAM** - Championship material! Noma sana")
            elif avg_rating >= 70:
                st.write("⭐ **STRONG TEAM** - Top 4 contender!")
            elif avg_rating >= 60:
                st.write("👍 **DECENT TEAM** - Mid-table finish! si mbaaya")
            else:
                st.write("😬 **NEEDS WORK** - Haha Relegation battle Mzee")
            
            # Show team breakdown
            st.subheader("Team Breakdown:")
            st.dataframe(team_data[['Player', 'Squad', 'Pos_Category', 'Player_Rating']])
        else:
            st.error("Some players not found in database!")
else:
    st.info(f"Select all 11 players to predict efficiency. ({len(selected_players)}/11 selected)")
