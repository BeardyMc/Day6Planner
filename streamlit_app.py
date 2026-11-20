import pandas as pd
import streamlit as st


st.title("Day 6 PvP planner")



PLAYERS_DATA = [
    {"Points": 50, "Player Name": "Flipsh0t", "Power (b)": 206000.0},
    {"Points": 49, "Player Name": "BeeKay", "Power (b)": 329000.0},
    {"Points": 48, "Player Name": "AlphaR", "Power (b)": 463000.0},
    {"Points": 47, "Player Name": "imnotjul", "Power (b)": 6050.0},
    {"Points": 46, "Player Name": "TimeTime", "Power (b)": 3130.0},
    {"Points": 45, "Player Name": "RoughPhlox43211", "Power (b)": 2760.0,},
    {"Points": 44, "Player Name": "FizzMercs", "Power (b)": 2600.0},
    {"Points": 43, "Player Name": "Freaky23", "Power (b)": 2470.0},
    {"Points": 42, "Player Name": "DizzyEagle22824", "Power (b)": 2390.0},
    {"Points": 41, "Player Name": "Treasured1", "Power (b)": 1890.0},
    {"Points": 40, "Player Name": "MrPimienta11", "Power (b)": 1420.0},
    {"Points": 39, "Player Name": "Calmtome", "Power (b)": 1400.0},
    {"Points": 38, "Player Name": "LeafyFang10042", "Power (b)": 1380.0},
    {"Points": 37, "Player Name": "Cmoney22", "Power (b)": 1330.0},
    {"Points": 36, "Player Name": "Redminedevil", "Power (b)": 1280.0},
    {"Points": 35, "Player Name": "Loukoum92i", "Power (b)": 1140.0},
    {"Points": 34, "Player Name": "Vincee", "Power (b)": 645.0},
    {"Points": 33, "Player Name": "Jdong", "Power (b)": 588.0},
    {"Points": 32, "Player Name": "Dreski", "Power (b)": 507.0},
    {"Points": 31, "Player Name": "MikeHawkQc", "Power (b)": 485.0},
    {"Points": 30, "Player Name": "wowie", "Power (b)": 442.0},
    {"Points": 29, "Player Name": "Frogboy02", "Power (b)": 438.0},
    {"Points": 28, "Player Name": "Predawn", "Power (b)": 436.0},
    {"Points": 27, "Player Name": "Shuffles", "Power (b)": 280.0},
    {"Points": 26, "Player Name": "MadPhlox90285", "Power (b)": 252.0},
    {"Points": 25, "Player Name": "PYPLOLIGYATD", "Power (b)": 188.0},
    {"Points": 24, "Player Name": "Modred", "Power (b)": 137.0},
    {"Points": 23, "Player Name": "Ratae", "Power (b)": 135.0},
    {"Points": 22, "Player Name": "Xperiment", "Power (b)": 134.0},
    {"Points": 21, "Player Name": "Freshavacado", "Power (b)": 99.4},
    {"Points": 20, "Player Name": "UNFORGIV3N", "Power (b)": 80.6},
    {"Points": 19, "Player Name": "3lj3f3", "Power (b)": 77.7},
    {"Points": 18, "Player Name": "Riqo", "Power (b)": 71.7},
    {"Points": 17, "Player Name": "Moose5428", "Power (b)": 61.0},
    {"Points": 16, "Player Name": "Owange", "Power (b)": 57.1},
    {"Points": 15, "Player Name": "kmb18045", "Power (b)": 50.5},
    {"Points": 14, "Player Name": "BinkBonk", "Power (b)": 50.1},
    {"Points": 13, "Player Name": "EFF94", "Power (b)": 43.9},
    {"Points": 12, "Player Name": "Paultus", "Power (b)": 41.4},
    {"Points": 11, "Player Name": "Nichee", "Power (b)": 35.9},
    {"Points": 10, "Player Name": "BloominOnion", "Power (b)": 30.2},
    {"Points": 9, "Player Name": "SkyrimNatDog", "Power (b)": 28.1},
    {"Points": 8, "Player Name": "AstralWaffles", "Power (b)": 15.0},
    {"Points": 7, "Player Name": "Slowmo", "Power (b)": 10.4},
    {"Points": 6, "Player Name": "awsomeemil25", "Power (b)": 3.72},
    {"Points": 5, "Player Name": "AztecBaby", "Power (b)": 1.12},
    {"Points": 4, "Player Name": "HolyPouch61610", "Power (b)": 0.547},
    {"Points": 3, "Player Name": "sn0wshooter", "Power (b)": 0.505},
    {"Points": 2, "Player Name": "Hackyaccidents", "Power (b)": 0.00771},
]


DISPLAY_COLS = ["Player Name", "Power (b)"]

# Store editable DataFrames in session_state so edits persist across reruns
if "players_df" not in st.session_state:
  st.session_state.players_df = pd.DataFrame(PLAYERS_DATA)

if "enemies_df" not in st.session_state:
  st.session_state.enemies_df = pd.DataFrame(ENEMY_DATA)

left_col, right_col = st.columns(2, wrap=False)

with left_col:
  st.subheader("Players")
  edited_players = st.data_editor(
      st.session_state.players_df,
      column_order=DISPLAY_COLS,
      hide_index=True,
      num_rows="dynamic",
      key="players_editor",
  )
  st.session_state.players_df = edited_players

with right_col:
  st.subheader("Enemies")
  edited_enemies = st.data_editor(
      st.session_state.enemies_df,
      column_order=DISPLAY_COLS,
      hide_index=True,
      num_rows="dynamic",
      key="enemies_editor",
  )
  st.session_state.enemies_df = edited_enemies

