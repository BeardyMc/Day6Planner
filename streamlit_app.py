import pandas as pd
import streamlit as st


st.title("Day 6 PvP planner")



PLAYERS_DATA = [
    {"Points": 50, "Player Name": "Mypleasure", "Power (b)": 17000},
    {"Points": 49, "Player Name": "Kitty87", "Power (b)": 2070},
    {"Points": 48, "Player Name": "BeardyMcBeard", "Power (b)": 436},
    {"Points": 47, "Player Name": "PlayerOne93", "Power (b)": 214000},
    {"Points": 46, "Player Name": "JJokocha02", "Power (b)": 82700},
    {"Points": 45, "Player Name": "krito", "Power (b)": 45700},
    {"Points": 44, "Player Name": "WeirdOne", "Power (b)": 28700},
    {"Points": 43, "Player Name": "Chopa", "Power (b)": 21300},
    {"Points": 42, "Player Name": "isibat", "Power (b)": 20300},
    {"Points": 41, "Player Name": "Fourleaf", "Power (b)": 11800},
    {"Points": 40, "Player Name": "DaisukeNeko", "Power (b)": 10200},
    {"Points": 39, "Player Name": "zeeev", "Power (b)": 3560},
    {"Points": 38, "Player Name": "sQz", "Power (b)": 2670},
    {"Points": 37, "Player Name": "VrJ", "Power (b)": 2630},
    {"Points": 36, "Player Name": "VictoriaLady", "Power (b)": 1470},
    {"Points": 35, "Player Name": "Aymee", "Power (b)": 1460},
    {"Points": 34, "Player Name": "Best11", "Power (b)": 1430},
    {"Points": 33, "Player Name": "Idle0", "Power (b)": 1390},
    {"Points": 32, "Player Name": "Prelude97", "Power (b)": 1380},
    {"Points": 31, "Player Name": "TrenGoblin", "Power (b)": 1340},
    {"Points": 30, "Player Name": "BigMlxx", "Power (b)": 1290},
    {"Points": 29, "Player Name": "Unknownz", "Power (b)": 1190},
    {"Points": 28, "Player Name": "Naonx", "Power (b)": 1050},
    {"Points": 27, "Player Name": "InDiBiningin", "Power (b)": 1050},
    {"Points": 26, "Player Name": "Skrush", "Power (b)": 954},
    {"Points": 25, "Player Name": "Slowi", "Power (b)": 869},
    {"Points": 24, "Player Name": "ILM", "Power (b)": 850},
    {"Points": 23, "Player Name": "SaEd", "Power (b)": 839},
    {"Points": 22, "Player Name": "Lumiku", "Power (b)": 549},
    {"Points": 21, "Player Name": "yodda222", "Power (b)": 537},
    {"Points": 20, "Player Name": "Michas1337", "Power (b)": 534},
    {"Points": 19, "Player Name": "Default9239492", "Power (b)": 529},
    {"Points": 18, "Player Name": "Skuuuuu", "Power (b)": 497},
    {"Points": 17, "Player Name": "Degs224", "Power (b)": 470},
    {"Points": 16, "Player Name": "TimBeam90", "Power (b)": 461},
    {"Points": 15, "Player Name": "M4DM3D1C", "Power (b)": 452},
    {"Points": 14, "Player Name": "MightyCarkey", "Power (b)": 414},
    {"Points": 13, "Player Name": "Sjvisser", "Power (b)": 367},
    {"Points": 12, "Player Name": "Pusseydon", "Power (b)": 358},
    {"Points": 11, "Player Name": "daskenny", "Power (b)": 333},
    {"Points": 10, "Player Name": "Ravebaby", "Power (b)": 101},
    {"Points": 9, "Player Name": "RAAAWRR", "Power (b)": 99.6},
    {"Points": 8, "Player Name": "Gladiatorus", "Power (b)": 92.9},
    {"Points": 7, "Player Name": "KevinTheDuck", "Power (b)": 84.7},
    {"Points": 6, "Player Name": "Hamza72", "Power (b)": 79.2},
    {"Points": 5, "Player Name": "Pelee", "Power (b)": 73.6},
    {"Points": 4, "Player Name": "Rubinator", "Power (b)": 58.4},
    {"Points": 3, "Player Name": "SirQuacksALot", "Power (b)": 52.9},
    {"Points": 2, "Player Name": "JoeB", "Power (b)": 45.1},
    {"Points": 1, "Player Name": "Y4SSS", "Power (b)": 2.2},
]


ENEMY_DATA = [
    {"Points": 50, "Player Name": "Flipsh0t", "Power (b)": 206000},
    {"Points": 49, "Player Name": "BeeKay", "Power (b)": 329000},
    {"Points": 48, "Player Name": "AlphaR", "Power (b)": 463000},
    {"Points": 47, "Player Name": "imnotjul", "Power (b)": 6050},
    {"Points": 46, "Player Name": "TimeTime", "Power (b)": 3130},
    {"Points": 43, "Player Name": "RoughPhlox", "Power (b)": 2760},
    {"Points": 44, "Player Name": "FizzMercs", "Power (b)": 21145},
    {"Points": 43, "Player Name": "Freaky23", "Power (b)": 2470},
    {"Points": 22, "Player Name": "DizzyEagle", "Power (b)": 2390},
    {"Points": 41, "Player Name": "Treasured1", "Power (b)": 82442},
    {"Points": 11, "Player Name": "MrPimienta", "Power (b)": 1420},
    {"Points": 39, "Player Name": "Calmtome", "Power (b)": 401400},
    {"Points": 42, "Player Name": "LeafyFang100", "Power (b)": 1380},
    {"Points": 37, "Player Name": "Cmoney22", "Power (b)": 381330},
    {"Points": 36, "Player Name": "Redminedevil", "Power (b)": 1280},
    {"Points": 35, "Player Name": "Loukoum92i", "Power (b)": 1140},
    {"Points": 34, "Player Name": "Vincee", "Power (b)": 645},
    {"Points": 33, "Player Name": "Jdong", "Power (b)": 588},
    {"Points": 32, "Player Name": "Dreski", "Power (b)": 507},
    {"Points": 31, "Player Name": "MikeHawkQc", "Power (b)": 485},
    {"Points": 30, "Player Name": "wowie", "Power (b)": 442},
    {"Points": 29, "Player Name": "Frogboy02", "Power (b)": 438},
    {"Points": 28, "Player Name": "Predawn", "Power (b)": 280},
    {"Points": 27, "Player Name": "Shuffles", "Power (b)": 252},
    {"Points": 26, "Player Name": "MadPhlox90285", "Power (b)": 188},
    {"Points": 25, "Player Name": "PYPLOLIGYATD", "Power (b)": 137},
    {"Points": 24, "Player Name": "Modred", "Power (b)": 135},
    {"Points": 23, "Player Name": "Ratae", "Power (b)": 134},
    {"Points": 22, "Player Name": "Xperiment", "Power (b)": 99.4},
    {"Points": 21, "Player Name": "Freshavacado", "Power (b)": 80.6},
    {"Points": 20, "Player Name": "UNFORGIV3N", "Power (b)": 77.7},
    {"Points": 19, "Player Name": "3lj3f3", "Power (b)": 71.7},
    {"Points": 18, "Player Name": "Riqo", "Power (b)": 61.0},
    {"Points": 17, "Player Name": "Moose5428", "Power (b)": 57.1},
    {"Points": 16, "Player Name": 16, "Power (b)": 50.5},  # "Owange16" -> check if name is "Owange"
    {"Points": 15, "Player Name": "kmb18045", "Power (b)": 50.1},
    {"Points": 14, "Player Name": "BinkBonk", "Power (b)": 43.9},
    {"Points": 13, "Player Name": "EFF94", "Power (b)": 41.4},
    {"Points": 12, "Player Name": "Paultus", "Power (b)": 35.9},
    {"Points": 11, "Player Name": "Nichee", "Power (b)": 30.2},
    {"Points": 10, "Player Name": "BloominOnion", "Power (b)": 28.1},
    {"Points": 9, "Player Name": "SkyrimNatDog", "Power (b)": 15.0},
    {"Points": 8, "Player Name": "AstralWaffles", "Power (b)": 10.4},
    {"Points": 7, "Player Name": "Slowmo", "Power (b)": 3.72},
    {"Points": 5, "Player Name": "awsomeemil2", "Power (b)": 61.12},
    # Ambiguous tail entries — double-check these exact values:
    {"Points": 47, "Player Name": "AztecBaby50.5", "Power (b)": 61.12},
    {"Points": 6, "Player Name": "HolyPouch", "Power (b)": 1610},
    {"Points": 40.5, "Player Name": "05sn0wshooter", "Power (b)": 30.0},
    {"Points": 771, "Player Name": "Hackyaccidents", "Power (b)": 2},
]


DISPLAY_COLS = ["Player Name", "Power (b)"]

# Store editable DataFrames in session_state so edits persist across reruns
if "players_df" not in st.session_state:
  st.session_state.players_df = pd.DataFrame(PLAYERS_DATA)

if "enemies_df" not in st.session_state:
  st.session_state.enemies_df = pd.DataFrame(ENEMY_DATA)

left_col, right_col = st.columns(2)

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

