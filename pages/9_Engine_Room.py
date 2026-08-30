import streamlit as st

from components.bento_layout import render_bento_shell
from components.engine_room import render_engine_room
from components.layout import render_hero
from utils.bootstrap import load_context, setup_page

setup_page("Engine Room", "⚙️")

render_bento_shell()
render_hero(
  "Engine Room",
  "Behind the scenes — processing methods, data lineage, contracts, and runtime telemetry.",
  badge="Technical · Not shown to end users",
)

try:
  ctx = load_context()
  render_engine_room(ctx)
except Exception as e:
  st.error(f"Unable to load engine room: {e}")
