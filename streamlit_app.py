import math
import pandas as pd
import requests
import base64
import json
from pathlib import Path
import streamlit as st

# ==========================================
# 1. HELPER FUNCTIONS
# ==========================================

def _get_jsonbin_config():
  """Returns `(url, headers)` from `st.secrets`, or `(None, None)` if missing."""
  try:
    api_key = st.secrets["JSONBIN_API_KEY"]
    bin_id = st.secrets["BIN_ID"]
  except (KeyError, FileNotFoundError):
    return None, None

  url = f"https://api.jsonbin.io/v3/b/{bin_id}"
  headers = {
      "X-Master-Key": api_key,
      "Content-Type": "application/json",
  }
  return url, headers


def get_visit_count():
  """Fetches the current visit count from JSONBin without modifying it."""
  url, headers = _get_jsonbin_config()
  if not url:
    return None

  try:
    resp = requests.get(url, headers={"X-Master-Key": headers["X-Master-Key"]}, timeout=5)
    resp.raise_for_status()
    record = resp.json().get("record", {})
    return int(record.get("visits", 0))
  except Exception as exc:
    print(f"JSONBin get visit count error: {exc}", flush=True)
    return None


def set_visit_count(new_value):
  """Writes an exact `visits` count to JSONBin and returns `new_value` on success."""
  url, headers = _get_jsonbin_config()
  if not url:
    return None

  try:
    clean_value = max(0, int(new_value))
    resp = requests.put(
        url,
        headers=headers,
        json={"visits": clean_value},
        timeout=5,
    )
    resp.raise_for_status()
    return clean_value
  except Exception as exc:
    print(f"JSONBin set visit count error: {exc}", flush=True)
    return None
 

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


def sum_roster_power(df, power_col="Power (b)"):
  """Sums numeric power values safely, ignoring blank or non-numeric cells."""
  if df is None or df.empty or power_col not in df.columns:
    return 0.0
  return float(pd.to_numeric(df[power_col], errors="coerce").fillna(0.0).sum())


def format_df_powers(df, power_cols=("Power (b)", "Effective Power")):
  """Returns a copy of `df` with specified power columns formatted via `format_si_3sf`."""
  if df is None or df.empty:
    return df.copy() if df is not None else pd.DataFrame()

  out = df.copy()
  for col in power_cols:
    if col in out.columns:
      out[col] = out[col].apply(format_si_3sf)
  return out


def simulate_battles(
    attackers_df,
    defenders_df,
    attacks_per_player=5,
    reset_threshold=43,
    safety_margin=1.0,
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
          (attackers["attacks_left"] > 0)
          & ((attackers["eff_power"] * safety_margin) >= d_power)
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
    # cycle_matches.sort(key=lambda m: m["attacker_power"])

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


def build_cycle_summary_tables(
    log_df, defenders_df, attackers_df, attacks_per_player=5
):
  """Builds two summary tables from a simulation `log_df`:

  1. `enemy_cycles_df`: For each defender ("Defender"), shows which attacker
     ("Attacker") beats them in each Cycle (`Cycle 1`, `Cycle 2`, ...).
  2. `attacker_targets_df`: For each attacker ("Attacker"), lists their
     assigned defenders across columns `"Battle 1"`, `"Battle 2"`, ...
     formatted as `"Defender (Cycle X)"`.
  """
  defender_names = (
      defenders_df["Player Name"].dropna().tolist()
      if defenders_df is not None and not defenders_df.empty
      else []
  )
  attacker_names = (
      attackers_df["Player Name"].dropna().tolist()
      if attackers_df is not None and not attackers_df.empty
      else []
  )

  battle_cols = [f"Battle {i}" for i in range(1, attacks_per_player + 1)]

  if log_df is None or log_df.empty:
    empty_enemies = pd.DataFrame({"Defender": defender_names})
    empty_attackers = pd.DataFrame([
        {
            "Attacker": a,
            "Attacks Used": 0,
            **{col: "" for col in battle_cols},
        }
        for a in attacker_names
    ])
    return empty_enemies, empty_attackers

  cycles = sorted(log_df["Cycle"].dropna().unique().tolist())
  cycle_cols = [f"Cycle {int(c)}" for c in cycles]

  all_defenders = list(
      dict.fromkeys(defender_names + log_df["Defender"].dropna().tolist())
  )
  enemy_rows = {d: {col: "" for col in cycle_cols} for d in all_defenders}

  all_attackers = list(
      dict.fromkeys(attacker_names + log_df["Attacker"].dropna().tolist())
  )
  attacker_entries = {a: [] for a in all_attackers}

  for _, row in log_df.iterrows():
    cyc = int(row["Cycle"])
    cyc_col = f"Cycle {cyc}"
    att = row["Attacker"]
    dfnd = row["Defender"]

    # Table 1: Who beats each defender in each cycle
    if dfnd in enemy_rows:
      if enemy_rows[dfnd][cyc_col]:
        enemy_rows[dfnd][cyc_col] = f"{enemy_rows[dfnd][cyc_col]}, {att}"
      else:
        enemy_rows[dfnd][cyc_col] = att

    # Table 2: Who each attacker is up against, formatted as "Defender (Cycle X)"
    if att in attacker_entries:
      attacker_entries[att].append(f"{dfnd} (Cycle {cyc})")

  enemy_records = [{"Defender": d, **enemy_rows[d]} for d in all_defenders]
  enemy_cycles_df = pd.DataFrame(enemy_records)

  # Dynamically size Battle columns to at least `attacks_per_player`
  max_battles = max(
      attacks_per_player,
      max((len(v) for v in attacker_entries.values()), default=0),
  )
  battle_cols = [f"Battle {i}" for i in range(1, max_battles + 1)]

  attacker_records = []
  for a in all_attackers:
    battles = attacker_entries[a]
    battle_dict = {
        f"Battle {i + 1}": (battles[i] if i < len(battles) else "")
        for i in range(max_battles)
    }
    attacker_records.append({
        "Attacker": a,
        "Attacks Used": len(battles),
        **battle_dict,
    })

  attacker_targets_df = pd.DataFrame(attacker_records)

  return enemy_cycles_df, attacker_targets_df


def assign_rank_points(df, power_col="Power (b)"):
  """Assigns Points with Leader = 50 and up to 49 other players receiving 49..1.

  Order after Leader (50):
  Commander -> Captain -> r1 -> r2 -> r3 -> r4 -> r5 (highest power first within r1..r5).
  """
  if df is None or df.empty:
    out = df.copy() if df is not None else pd.DataFrame()
    out["Points"] = []
    return out

  out = df.copy()
  rank_clean = out.get("Rank", pd.Series(["r4"] * len(out), index=out.index))
  rank_clean = rank_clean.fillna("r4").astype(str).str.strip().str.lower()

  r_order = {"r1": 0, "r2": 1, "r3": 2, "r4": 3, "r5": 4}

  sort_power_col = power_col if power_col in out.columns else "Power (b)"
  out["_sort_power"] = pd.to_numeric(out[sort_power_col], errors="coerce").fillna(
      0.0
  )

  def _tier_tuple(row_idx):
    rk = rank_clean.loc[row_idx]
    pwr = out.loc[row_idx, "_sort_power"]
    if rk == "leader":
      return (0, 0, -pwr, row_idx)
    if rk == "commander":
      return (1, 0, -pwr, row_idx)
    if rk == "captain":
      return (2, 0, -pwr, row_idx)
    if rk in r_order:
      return (3, r_order[rk], -pwr, row_idx)
    return (4, 99, -pwr, row_idx)

  ordered_indices = sorted(out.index.tolist(), key=_tier_tuple)

  next_points = 49
  points_map = {}
  for idx in ordered_indices:
    if rank_clean.loc[idx] == "leader":
      points_map[idx] = 50
    else:
      points_map[idx] = max(1, next_points)
      next_points -= 1

  out["Points"] = out.index.map(points_map)
  return out.drop(columns=["_sort_power"])

 
def _get_github_config():
  """Reads GitHub repo settings from `st.secrets`."""
  try:
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["GITHUB_REPO"]
    path = st.secrets.get("GITHUB_DATA_PATH", "data/pvp_rosters.json")
    branch = st.secrets.get("GITHUB_BRANCH", "main")
    return token, repo, path, branch
  except (KeyError, FileNotFoundError):
    return None, None, None, None


def load_rosters():
  """Fetches `data/pvp_rosters.json` from GitHub API, falling back to local disk."""
  token, repo, path, branch = _get_github_config()

  if token and repo:
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    try:
      resp = requests.get(
          url, headers=headers, params={"ref": branch}, timeout=10
      )
      resp.raise_for_status()
      payload = resp.json()
      # GitHub Contents API returns file content base64-encoded
      raw_text = base64.b64decode(payload["content"]).decode("utf-8")
      return json.loads(raw_text)
    except Exception as exc:
      print(f"GitHub load error, falling back to local file: {exc}", flush=True)

  local_path = Path(path or "data/pvp_rosters.json")
  if local_path.exists():
    try:
      return json.loads(local_path.read_text(encoding="utf-8"))
    except Exception as exc:
      print(f"Local roster read error: {exc}", flush=True)

  return {}


def _filter_active_entries(entries):
  """Excludes any player/enemy marked `"active": false`."""
  if not isinstance(entries, list):
    return []
  return [
      entry
      for entry in entries
      if isinstance(entry, dict) and entry.get("active", True) is not False
  ]


def save_rosters_to_github(
    players_df, enemies_df, commit_message="Update PvP rosters"
):
  """Pushes `players_df` and `enemies_df` to the GitHub JSON file."""
  token, repo, path, branch = _get_github_config()
  if not token or not repo:
    return False, "Missing GITHUB_TOKEN or GITHUB_REPO in secrets."

  url = f"https://api.github.com/repos/{repo}/contents/{path}"
  headers = {
      "Authorization": f"Bearer {token}",
      "Accept": "application/vnd.github+json",
  }

  try:
    # Fetch latest file SHA first so GitHub accepts the update
    get_resp = requests.get(
        url, headers=headers, params={"ref": branch}, timeout=10
    )
    get_resp.raise_for_status()
    current_sha = get_resp.json()["sha"]

    clean_players = (
        players_df.dropna(how="all")
        if players_df is not None
        else pd.DataFrame()
    )
    clean_enemies = (
        enemies_df.dropna(how="all")
        if enemies_df is not None
        else pd.DataFrame()
    )

    roster_payload = {
        "players": clean_players.to_dict(orient="records"),
        "enemies": clean_enemies.to_dict(orient="records"),
    }
    encoded_content = base64.b64encode(
        json.dumps(roster_payload, indent=2).encode("utf-8")
    ).decode("utf-8")

    put_body = {
        "message": commit_message,
        "content": encoded_content,
        "sha": current_sha,
        "branch": branch,
    }
    put_resp = requests.put(url, headers=headers, json=put_body, timeout=10)
    put_resp.raise_for_status()
    return True, f"Pushed rosters to `{path}` on `{branch}`."
  except Exception as exc:
    print(f"GitHub push error: {exc}", flush=True)
    return False, f"GitHub push failed: {exc}"



# ==========================================
# 2. DATA & UI DISPLAY
# ==========================================

# if creator, don't count me as a visitor and let me know how many others have used it. 
ignore_key = st.secrets.get("IGNORE_VISIT_KEY", "")
is_ignored_visitor = bool(ignore_key) and st.query_params.get("key") == ignore_key

if "active" not in st.session_state:
  st.session_state.active = True
  current_visits = get_visit_count()
  if is_ignored_visitor:
    st.session_state.visit_count = current_visits
  elif current_visits is not None:
    st.session_state.visit_count = set_visit_count(current_visits + 1)
  else:
    st.session_state.visit_count = None

if is_ignored_visitor:
  count_display = (
      st.session_state.visit_count
      if st.session_state.visit_count is not None
      else "Unavailable"
  )
  st.caption(f"🔧 Creator mode active\n\nUsers so far: {count_display}")

  with st.expander("Creator Counter Controls", expanded=False):
    col_val, col_btn, col_rst = st.columns(
      [1.5, 1, 1],
      vertical_alignment="bottom",
      wrap=False,
    )
    with col_val:
      override_val = st.number_input(
        "Set Visit Counter To",
        min_value=0,
        value=int(st.session_state.visit_count or 0),
        step=1,
        key="override_visit_count_input",
      )
    with col_btn:
      if st.button(
        "Apply Count", key="apply_visit_count_btn", width="stretch"
      ):
        updated = set_visit_count(override_val)
        if updated is not None:
          st.session_state.visit_count = updated
          st.rerun()
        else:
          st.error("Failed to update counter in JSONBin.")
    with col_rst:
      if st.button(
        "Reset to 0", key="reset_visit_count_btn", width="stretch"
      ):
        updated = set_visit_count(0)
        if updated is not None:
          st.session_state.visit_count = updated
          st.rerun()
        else:
          st.error("Failed to reset counter in JSONBin.")


st.title("Day 6 PvP planner")

st.write(
    "Below are all player's powers, if you notice any power discrepancies vs in"
    " game data, you can edit it here, but please tell Beardy so that he can"
    " edit it for everyone."
)

if "players_df" not in st.session_state or "enemies_df" not in st.session_state:
  rosters = load_rosters()
  active_players = _filter_active_entries(rosters.get("players", []))
  active_enemies = _filter_active_entries(rosters.get("enemies", []))

  st.session_state.players_df = pd.DataFrame(active_players)
  st.session_state.enemies_df = pd.DataFrame(active_enemies)


DISPLAY_COLS = ["Rank", "Player Name", "Power (b)"]

left_col, right_col = st.columns(2, wrap=False)

with left_col:
  our_total_power = format_si_3sf(sum_roster_power(st.session_state.players_df))
  st.subheader(f"EDGR: {our_total_power}")
  edited_players = st.data_editor(
      st.session_state.players_df,
      column_order=DISPLAY_COLS,
      hide_index=True,
      num_rows="dynamic",
      key="players_editor",
  )
  st.session_state.players_df = edited_players

with right_col:
  enemy_total_power = format_si_3sf(sum_roster_power(st.session_state.enemies_df))
  st.subheader(f"Enemies: {enemy_total_power}") 
  st.subheader("Enemies")
  edited_enemies = st.data_editor(
      st.session_state.enemies_df,
      column_order=DISPLAY_COLS,
      hide_index=True,
      num_rows="dynamic",
      key="enemies_editor",
  )
  st.session_state.enemies_df = edited_enemies


## PUSH TO SAVE FILE
if "push_unlocked" not in st.session_state:
  st.session_state.push_unlocked = False

with st.expander("Save / Push Rosters to GitHub", expanded=False):
  expected_push_pwd = st.secrets.get("PUSH_PASSWORD", "")

  if not st.session_state.push_unlocked:
    with st.form("push_auth_form", clear_on_submit=True):
      entered_pwd = st.text_input("Push Password", type="password")
      unlock_clicked = st.form_submit_button("Unlock Push")
      if unlock_clicked:
        if expected_push_pwd and entered_pwd == expected_push_pwd:
          st.session_state.push_unlocked = True
          st.rerun()
        else:
          st.error("Incorrect push password.")
  else:
    st.caption(
        "If updating player power, please leave a message for what and why you"
        " edited."
    )
    commit_msg_input = st.text_input(
        "Commit Message",
        placeholder="e.g. Updated [my name]'s power",
        key="roster_commit_msg_input",
    )
    final_commit_msg = (
        commit_msg_input.strip()
        if commit_msg_input and commit_msg_input.strip()
        else "Update PvP rosters from planner"
    )

    col_push, col_lock = st.columns([3, 1], vertical_alignment="bottom")
    with col_push:
      if st.button(
          "Push Rosters to GitHub", key="push_rosters_btn", width="stretch"
      ):
        ok, msg = save_rosters_to_github(
            st.session_state.players_df,
            st.session_state.enemies_df,
            commit_message=final_commit_msg,
        )
        if ok:
          st.success(msg)
        else:
          st.error(msg)
    with col_lock:
      if st.button("Lock", key="lock_push_btn", width="stretch"):
        st.session_state.push_unlocked = False
        st.rerun()
 
 

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
        value=80,
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

players_eff = calc_effective_power(
    st.session_state.players_df, our_damage_lvl, our_health_lvl
)
enemies_eff = calc_effective_power(
    st.session_state.enemies_df, enemy_damage_lvl, enemy_health_lvl
)

players_eff = assign_rank_points(players_eff, power_col="Effective Power")
enemies_eff = assign_rank_points(enemies_eff, power_col="Effective Power")

st.subheader("⚔️ Select Your Player & Find Matchups")

valid_players_eff = players_eff[
    players_eff["Player Name"].notna()
    & (players_eff["Player Name"].astype(str).str.strip() != "")
].copy()
clan_names = valid_players_eff["Player Name"].tolist()
selected_player = st.selectbox("Who are you?", options=clan_names)

safety_margin_pct = st.slider(
    "Target Safety Margin (% of Attacker Effective Power) \n\n(aka how good"
    " is your build vs theirs):",
    min_value=50,
    max_value=150,
    value=90,
    step=1,
    key="safety_margin_pct",
)
safety_margin = (
    float(safety_margin_pct if safety_margin_pct is not None else 100.0)
    / 100.0
)

if selected_player:
  player_matches = valid_players_eff[
      valid_players_eff["Player Name"] == selected_player
  ]
  if not player_matches.empty:
    player_row = player_matches.iloc[0]
    my_eff_power = float(
        pd.to_numeric(player_row["Effective Power"], errors="coerce") or 0.0
    )
    max_target_power = my_eff_power * safety_margin
    enemy_mult = 1.0 + ((enemy_damage_lvl or 0) + (enemy_health_lvl or 0)) / 2.0

    st.metric(
        label=f"{selected_player}'s Effective Power",
        value=format_si_3sf(my_eff_power),
        delta=(
            "Safe target cap:"
            f" {format_si_3sf(max_target_power / enemy_mult)}"
            f" ({safety_margin_pct:.0f}%)"
        ),
        delta_color="off",
    )

    winnable_enemies = enemies_eff[
        pd.to_numeric(enemies_eff["Effective Power"], errors="coerce").fillna(
            math.inf
        )
        <= max_target_power
    ]

    st.write(f"**Battleable Enemies ({len(winnable_enemies)}):**")
    st.dataframe(
        format_df_powers(
            winnable_enemies[["Player Name", "Power (b)", "Effective Power"]]
        ),
        hide_index=True,
        use_container_width=True,
    )


st.subheader("🏆 Theoretical Max Points (250 Battles / 43-Enemy Reset)")

if st.button("Run Theoretical Max Simulation"):
  sim = simulate_battles(
      players_eff,
      enemies_eff,
      attacks_per_player=5,
      reset_threshold=43,
      safety_margin=safety_margin,
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
      safety_margin=(1 / safety_margin),
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

  enemy_cycles_df, our_targets_df = build_cycle_summary_tables(
      sim["log_df"], enemies_eff, players_eff
  )

  st.markdown("#### Who should target each Enemy by Cycle")
  st.dataframe(enemy_cycles_df, hide_index=True, use_container_width=True)

  st.markdown("#### Our Players' Assigned Enemies")
  st.dataframe(our_targets_df, hide_index=True, use_container_width=True)

