# ── PROVIDED — do not edit ────────────────────────────────────────
"""
Lesson 4 — The Sentinel Awakens: Build the Trust Gate
Run with:  streamlit run lesson_4_boilerplate/app.py

This file wires the UI to your logic in student_logic.py.
You do NOT need to edit this file.
"""
import random
import streamlit as st

from constants import (
    APP_TITLE, MAX_TRUST, TRUST_TO_OPEN, TRUST_TO_ENTER,
    RIDDLES, REPEAT_REPLIES,
)
from ui import inject_styles, render_hud, render_gate_scene, render_chat_log, render_rules_popup

# ── Import student functions (with safe fallbacks if not done yet) ─
try:
    from student_logic import analyze_player_tone, get_sentinel_mood, process_player_message, process_riddle_answer
    _STUDENT_LOADED = True
except Exception as e:
    _STUDENT_LOADED = False
    _LOAD_ERROR = str(e)

st.set_page_config(page_title=APP_TITLE, page_icon="⚔", layout="wide", initial_sidebar_state="collapsed")

# ── Session state init ────────────────────────────────────────────
def init_state():
    defaults = {
        "player_name":       "",
        "trust_score":       0,
        "sentinel_mood":     "Suspicious",
        "riddle":            random.choice(RIDDLES),
        "riddle_solved":     False,
        "sentinel_messages": [
            "[SYSTEM]: Dimensional breach detected...",
            "[SENTINEL]: Stop where you are, Traveler...",
        ],
        "latest_clue":       "The outer gate is silent, but it is listening.",
        "streak":            0,
        "banished":          False,
        "messages_sent":     0,
        "player_messages":   [],
        "rules_accepted":    False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_game():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    init_state()

def get_phase_label() -> str:
    t = st.session_state.trust_score
    if t >= TRUST_TO_ENTER: return "VAULT THRESHOLD"
    if t >= TRUST_TO_OPEN:  return "GATE OPENING"
    return "TRUST GATE"

# ── Input callbacks ───────────────────────────────────────────────
def _on_msg_change():
    msg = st.session_state.get("msg_input", "").strip()
    if msg:
        if _STUDENT_LOADED:
            process_player_message(msg)
        else:
            st.toast("⚠️ Finish student_logic.py first!", icon="⚠️")
        st.session_state["_clear_msg"] = True

def _on_riddle_change():
    ans = st.session_state.get("riddle_input", "").strip()
    if ans:
        if _STUDENT_LOADED:
            process_riddle_answer(ans)
        else:
            st.toast("⚠️ Finish student_logic.py first!", icon="⚠️")
        st.session_state["_clear_riddle"] = True

# ── Main ──────────────────────────────────────────────────────────
def main():
    inject_styles()
    init_state()
    s = st.session_state

    if not s.rules_accepted:
        render_rules_popup()
        return

    # Show load error banner if student file has a syntax error
    if not _STUDENT_LOADED:
        st.error(f"⚠️ Could not load student_logic.py — fix the error and refresh.\n\n`{_LOAD_ERROR}`")

    render_hud(s.player_name, s.trust_score, s.sentinel_mood, s.streak, get_phase_label())

    # Gate scene
    latest = s.sentinel_messages[-1] if s.sentinel_messages else "[SENTINEL]: ..."
    render_gate_scene(s.trust_score, s.sentinel_mood, latest, s.player_name, s.latest_clue)

    # ── Controls ──────────────────────────────────────────────────
    if s.banished:
        st.error("☠️ You have been banished. The Sentinel remembers your disrespect.")
        if st.button("↺ Try Again", key="reset_banish"):
            reset_game(); st.rerun()
        return

    st.markdown("<div style='background:rgba(5,9,18,.98);border-top:1px solid rgba(124,92,255,.28);padding:10px 16px 8px;'>", unsafe_allow_html=True)

    # Name + message row
    c_name, c_msg, c_send, c_reset = st.columns([1.4, 4, 1, 0.8])
    with c_name:
        st.markdown("<div class='lbl'>Traveler Name</div>", unsafe_allow_html=True)
        n = st.text_input("name", value=s.player_name, placeholder="Your name…",
                          label_visibility="collapsed", key="name_input")
        if n != s.player_name: s.player_name = n

    if s.pop("_clear_msg", False):    st.session_state["msg_input"]    = ""
    if s.pop("_clear_riddle", False): st.session_state["riddle_input"] = ""

    with c_msg:
        st.markdown("<div class='lbl'>Message to the Sentinel</div>", unsafe_allow_html=True)
        st.text_input("msg", placeholder="Speak to the Sentinel…",
                      label_visibility="collapsed", key="msg_input", on_change=_on_msg_change)
    with c_send:
        st.markdown("<div class='lbl'>Send</div>", unsafe_allow_html=True)
        if st.button("▶ Send", use_container_width=True, key="send_btn"):
            msg = st.session_state.get("msg_input", "").strip()
            if msg and _STUDENT_LOADED:
                process_player_message(msg)
                st.session_state["_clear_msg"] = True
            st.rerun()
    with c_reset:
        st.markdown("<div class='lbl'>Reset</div>", unsafe_allow_html=True)
        if st.button("↺", use_container_width=True, key="reset_btn"):
            reset_game(); st.rerun()

    # Riddle row (only while not solved)
    if not s.riddle_solved:
        r1, r2, r3 = st.columns([4, 2, 1])
        with r1:
            st.markdown(
                f"<div style='font-size:.75rem;color:#c9f4ff;padding:4px 0;font-family:Rajdhani,sans-serif;'>"
                f"🔒 <b>Logic Lock:</b> {s.riddle['question']}</div>",
                unsafe_allow_html=True,
            )
        with r2:
            st.text_input("riddle", placeholder="Your answer…",
                          label_visibility="collapsed", key="riddle_input", on_change=_on_riddle_change)
        with r3:
            if st.button("🔓 Solve", use_container_width=True, key="solve_btn"):
                ans = st.session_state.get("riddle_input", "").strip()
                if ans and _STUDENT_LOADED:
                    process_riddle_answer(ans)
                    st.session_state["_clear_riddle"] = True
                st.rerun()
    else:
        st.markdown(
            "<div style='font-size:.75rem;color:#18b47b;padding:4px 0;font-family:Rajdhani,sans-serif;'>"
            "✅ Logic lock solved! Keep talking to the Sentinel to build trust.</div>",
            unsafe_allow_html=True,
        )

    # Vault entry banner
    if s.trust_score >= TRUST_TO_ENTER:
        st.success("🚪 The gate opens. You have earned the Sentinel's trust. Vault access granted!")

    st.markdown("</div>", unsafe_allow_html=True)

    # Chat log
    st.markdown("<div style='padding:6px 16px 0;'>", unsafe_allow_html=True)
    render_chat_log(s.sentinel_messages)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
