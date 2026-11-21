import pandas as pd
import math
import streamlit as st


st.title("Day 6 PvP planner")

st.write("Below are all player's powers, if you notice any power discrepancies vs in game data, you can edit it here, but please tell Beardy so that he can edit it for all of us.")

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

## BRAWL TECH 
col1, col2 = st.columns(2, wrap=False)
with col1:
  col1_1, col1_2 = st.columns(2, wrap=False)
  with col1_1:
    our_damage_lvl = st.number_input(
        "Our Damage Lvl",
        min_value=0,
        max_value=100,
        value=100,
        step=1,
        key="our_damage_lvl",
    )
  with col1_2:
    our_health_lvl = st.number_input(
        "Our Health Lvl",
        min_value=0,
        max_value=100,
        value=100,
        step=1,
        key="our_health_lvl",
    )

with col2:
  col2_1, col2_2 = st.columns(2, wrap=False)
  with col2_1:
    enemy_damage_lvl = st.number_input(
        "Enemy Damage Lvl",
        min_value=0,
        max_value=100,
        value=100,
        step=1,
        key="enemy_damage_lvl",
    )
  with col2_2:
    enemy_health_lvl = st.number_input(
        "Enemy Health Lvl",
        min_value=0,
        max_value=100,
        value=100,
        step=1,
        key="enemy_health_lvl",
    )


## EFFECTIVE DAY 6 POWER
def calc_effective_power(df, damage_lvl, health_lvl):
  """Computes Effective Power = Power (b) * (1 + (damage + health) / 2)."""
  out = df.copy()
  dmg = damage_lvl or 0
  hp = health_lvl or 0
  multiplier = 1.0 + (dmg + hp) / 2.0
  out["Effective Power"] = out["Power (b)"] * multiplier
  return out 

def format_si_3sf(value):
  """Formats a number to 3 significant figures with custom unit suffixes.

  Examples:
      1         -> "1b"
      1000      -> "1t"
      1000000   -> "1q"
      0.1       -> "10m"
      0.00771   -> "7.71m"
  """
  if value is None or math.isnan(value):
    return "0b"
  if value == 0:
    return "0b"

  sign = "-" if value < 0 else ""
  abs_val = abs(float(value))

  # Units mapped by powers of 10 relative to 1 ("b" = 10^0)
  # Adjust or expand this table if your game uses other letters!
  units = [
      (12, "T"),  # trillions of b (optional)
      (9, "B"),  # billions of b (optional)
      (6, "q"),  # 1,000,000 = 1q (10^6)
      (3, "t"),  # 1,000 = 1t (10^3)
      (0, "b"),  # 1 = 1b (10^0)
      (-3, "m"),  # 0.001 = 1m, 0.1 = 100m (10^-3)
  ]

  # Pick the largest unit step at or below abs_val
  chosen_exp, suffix = 0, "b"
  for exp, unit in units:
    if abs_val >= 10**exp:
      chosen_exp, suffix = exp, unit
      break

  # Scale value into the chosen unit
  scaled = abs_val / (10**chosen_exp)

  # Round to 3 significant figures
  sf_scaled = round(scaled, 3 - 1 - math.floor(math.log10(scaled)))

  # Guard against rounding 999.9 -> 1000 stepping into the next tier
  if sf_scaled >= 1000 and chosen_exp < 12:
    # Re-run at the next 10^3 step up if available
    next_exp = chosen_exp + 3
    for exp, unit in units:
      if exp == next_exp:
        scaled = abs_val / (10**exp)
        sf_scaled = round(scaled, 3 - 1 - math.floor(math.log10(scaled)))
        suffix = unit
        break

  # Format cleanly to 3 significant figures without trailing zeros
  # e.g. 1.0 -> "1", 10.0 -> "10", 7.71 -> "7.71", 123.0 -> "123"
  formatted_num = f"{sf_scaled:.3g}"
  return f"{sign}{formatted_num}{suffix}"


# nested in an if in case user breaks data in editable boxes. 
if "players_df" in st.session_state and "enemies_df" in st.session_state:
  players_eff = calc_effective_power(
      st.session_state.players_df, our_damage_lvl, our_health_lvl
  )
  enemies_eff = calc_effective_power(
      st.session_state.enemies_df, enemy_damage_lvl, enemy_health_lvl
  )

  st.subheader("⚔️ Select Your Player & Find Matchups")

  clan_names = players_eff["Player Name"].dropna().tolist()
  selected_player = st.selectbox("Who are you?", options=clan_names)

  if selected_player:
    player_row = players_eff[players_eff["Player Name"] == selected_player].iloc[
        0
    ]
    my_eff_power = float(player_row["Effective Power"])

    st.metric(
        label=f"{selected_player}'s Effective Power",
        value=format_si_3sf(my_eff_power),
    )


    winnable_enemies = enemies_eff[enemies_eff["Effective Power"] <= my_eff_power]

    st.write(f"**Battleable Enemies ({len(winnable_enemies)}):**")
    st.dataframe(
        winnable_enemies[["Player Name", "Power (b)", "Effective Power"]],
        hide_index=True,
        use_container_width=True,
    )

def simulate_battles(
    attackers_df,
    defenders_df,
    attacks_per_player=5,
    reset_threshold=43,
):
  """Maximizes total points across reset cycles.

  In each cycle of up to `reset_threshold` defeats:
  - Evaluates defenders from highest Points to lowest Points.
  - Assigns the weakest available attacker (with attacks remaining and
    attacker_eff_power >= defender_eff_power) to each high-value target.
  - Stops the cycle at `reset_threshold` wins (triggering a full reset),
    or earlier if no remaining attacker can beat any remaining target.
  """
  attackers = attackers_df.copy().reset_index(drop=True)
  attackers["eff_power"] = attackers["Effective Power"].astype(float)
  attackers["attacks_left"] = attacks_per_player

  # Sort defenders by highest Points first, tie-breaking by Effective Power
  defenders = defenders_df.copy()
  defenders["eff_power"] = defenders["Effective Power"].astype(float)
  defenders["pts"] = (
      defenders["Points"].astype(float) if "Points" in defenders.columns else 0.0
  )
  defenders = defenders.sort_values(
      by=["pts", "eff_power"], ascending=[False, False]
  ).reset_index(drop=True)

  max_possible_battles = len(attackers) * attacks_per_player
  total_wins = 0
  total_points = 0.0
  cycles_completed = 0
  cycle_num = 1
  battle_log = []

  while attackers["attacks_left"].sum() > 0:
    cycle_matches = []

    # Try to claim the highest-point targets first (up to reset_threshold)
    for _, d_row in defenders.iterrows():
      if len(cycle_matches) >= reset_threshold:
        break

      d_power = d_row["eff_power"]
      d_pts = d_row["pts"]

      # Find all attackers who still have attacks left AND can beat this defender
      eligible = attackers[
          (attackers["attacks_left"] > 0) & (attackers["eff_power"] >= d_power)
      ]

      if eligible.empty:
        # Nobody remaining can beat this target; skip down to the next highest-point target
        continue

      # Pick the WEAKEST eligible attacker so top hitters stay free for top targets
      chosen_idx = eligible["eff_power"].idxmin()
      a_row = attackers.loc[chosen_idx]

      attackers.at[chosen_idx, "attacks_left"] -= 1
      cycle_matches.append({
          "attacker_name": a_row["Player Name"],
          "attacker_power": a_row["eff_power"],
          "defender_name": d_row["Player Name"],
          "defender_power": d_power,
          "points": d_pts,
      })

    # If zero matches could be made in this cycle, no valid battles remain anywhere
    if not cycle_matches:
      break

    # Sort this cycle's chosen battles weakest-attacker-first for clean execution order
    cycle_matches.sort(key=lambda m: m["attacker_power"])

    for m in cycle_matches:
      total_wins += 1
      total_points += m["points"]
      battle_log.append({
          "Battle #": total_wins,
          "Cycle": cycle_num,
          "Attacker": m["attacker_name"],
          "Attacker Eff Power": format_si_3sf(m["attacker_power"]),
          "Defender": m["defender_name"],
          "Defender Eff Power": format_si_3sf(m["defender_power"]),
          "Points Gained": m["points"],
      })

    if len(cycle_matches) >= reset_threshold:
      cycles_completed += 1
      cycle_num += 1
    else:
      # Couldn't reach 43 wins to trigger another reset; all possible wins are exhausted
      break

  return {
      "total_wins": total_wins,
      "max_possible_battles": max_possible_battles,
      "total_points": total_points,
      "cycles_completed": cycles_completed,
      "log_df": pd.DataFrame(battle_log),
  }





st.subheader("🏆 Theoretical Max Points (250 Battles / 43-Enemy Reset)")


if st.button("Run Theoretical Max Simulation"):
  sim = simulate_battles(
      players_eff,
      enemies_eff,
      attacks_per_player=5,
      reset_threshold=43,
  )

  m1, m2, m3 = st.columns(3, wrap=False)
  m1.metric("Total Wins", f"{sim['total_wins']} / {sim['max_possible_battles']}")
  m2.metric("Projected Points", f"{sim['total_points']:,.0f}")
  m3.metric("Full 43-Defeat Resets", sim["cycles_completed"])

  if not sim["log_df"].empty:
    st.dataframe(sim["log_df"], hide_index=True, use_container_width=True)
  else:
    st.warning("No battles can be won with the current powers and levels.")

  st.divider()
  st.subheader("🛡️ Possible Enemy Wins")

  sim_enemy = simulate_battles(
      enemies_eff,
      players_eff,
      attacks_per_player=5,
      reset_threshold=43,
  )

  e1, e2, e3 = st.columns(3, wrap=False)
  e1.metric(
      "Enemy Wins vs Us",
      f"{sim_enemy['total_wins']} / {sim_enemy['max_possible_battles']}",
  )
  e2.metric("Points Enemies Could Score", f"{sim_enemy['total_points']:,.0f}")
  e3.metric("Full 43-Defeat Resets", sim_enemy["cycles_completed"])

  if not sim_enemy["log_df"].empty:
    st.dataframe(sim_enemy["log_df"], hide_index=True, use_container_width=True)
  else:
    st.success("Enemies can't beat any of our players with current stats!")
 
