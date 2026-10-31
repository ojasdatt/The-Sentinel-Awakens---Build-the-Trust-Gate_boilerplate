# ── PROVIDED — do not edit ────────────────────────────────────────
"""All Streamlit rendering for Lesson 4. Students do not edit this."""
import html as _h
import streamlit as st
import streamlit.components.v1 as components
from constants import (
    APP_TITLE, MAX_TRUST, TRUST_TO_OPEN, TRUST_TO_ENTER,
    BG, ACCENT, ACCENT_2, TEXT, MUTED, SUCCESS, WARNING, DANGER,
)

# ── Global CSS ────────────────────────────────────────────────────
def inject_styles():
    st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');
:root{{--bg:{BG};--accent:{ACCENT};--accent2:{ACCENT_2};--text:{TEXT};--muted:{MUTED};}}
html,body,[data-testid="stAppViewContainer"]{{background:var(--bg)!important;overflow:hidden;}}
.block-container{{padding:0!important;max-width:100%!important;}}
header[data-testid="stHeader"],[data-testid="stToolbar"],.stSidebar,footer{{display:none!important;}}
iframe{{display:block!important;width:100%!important;border:none!important;}}
[data-testid="stIFrame"]{{width:100%!important;}}
div[data-testid="stVerticalBlock"]>div{{gap:0!important;}}
.ctrl{{background:rgba(5,9,18,.98);border-top:1px solid rgba(124,92,255,.28);padding:10px 16px 8px;}}
.lbl{{font-size:.58rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:2px;}}
.stButton>button{{border-radius:8px!important;border:1px solid rgba(124,92,255,.35)!important;
  background:linear-gradient(180deg,rgba(124,92,255,.22),rgba(39,194,255,.12))!important;
  color:var(--text)!important;font-family:'Rajdhani',sans-serif!important;font-weight:600!important;
  font-size:.82rem!important;min-height:2rem!important;padding:0 10px!important;}}
.stTextInput input{{background:rgba(255,255,255,.03)!important;color:var(--text)!important;
  border-radius:8px!important;border:1px solid rgba(124,92,255,.22)!important;
  font-family:'Share Tech Mono',monospace!important;font-size:.82rem!important;}}
</style>""", unsafe_allow_html=True)

# ── HUD bar ───────────────────────────────────────────────────────
def render_hud(player_name, trust, mood, streak, phase):
    pct = int(trust / MAX_TRUST * 100)
    streak_html = (f"<span style='padding:2px 9px;border-radius:999px;font-size:.65rem;font-weight:700;"
                   f"border:1px solid rgba(242,193,79,.5);background:rgba(242,193,79,.12);color:#f2c14f;'>🔥 x{streak}</span>"
                   ) if streak >= 3 else ""
    components.html(f"""<!DOCTYPE html><html><head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{width:100%;height:48px;overflow:hidden;background:rgba(7,12,22,.97);
  font-family:'Rajdhani',sans-serif;border-bottom:1px solid rgba(124,92,255,.35);}}
.bar{{display:flex;align-items:center;height:48px;padding:0 14px;gap:0;}}
.title{{font-size:1rem;font-weight:700;letter-spacing:.12em;color:#27c2ff;text-transform:uppercase;margin-right:16px;white-space:nowrap;}}
.stat{{display:flex;flex-direction:column;align-items:center;padding:0 12px;border-left:1px solid rgba(255,255,255,.07);min-width:80px;}}
.lbl{{font-size:.54rem;color:#95a2b8;text-transform:uppercase;letter-spacing:.08em;}}
.val{{font-size:.88rem;font-weight:700;color:#e5ecf4;white-space:nowrap;}}
.bwrap{{flex:1;max-width:160px;margin:0 10px;}}
.bbg{{height:6px;border-radius:3px;background:rgba(255,255,255,.08);overflow:hidden;}}
.bfill{{height:100%;border-radius:3px;background:linear-gradient(90deg,#7c5cff,#27c2ff);}}
.phase{{margin-left:auto;padding:3px 12px;border-radius:999px;font-size:.65rem;letter-spacing:.1em;
  border:1px solid rgba(39,194,255,.4);background:rgba(39,194,255,.08);color:#c9f4ff;text-transform:uppercase;}}
</style></head><body>
<div class="bar">
  <div class="title">&#x2694; {_h.escape(APP_TITLE)}</div>
  <div class="stat"><span class="lbl">Traveler</span><span class="val">{_h.escape(player_name or "—")}</span></div>
  <div class="stat"><span class="lbl">Trust</span><span class="val">{trust}/{MAX_TRUST}</span></div>
  <div class="bwrap"><div class="lbl" style="font-size:.5rem;">TRUST CORE</div>
    <div class="bbg"><div class="bfill" style="width:{pct}%;"></div></div></div>
  <div class="stat"><span class="lbl">Mood</span><span class="val">{_h.escape(mood)}</span></div>
  {streak_html}
  <div class="phase">{_h.escape(phase)}</div>
</div></body></html>""", height=48, scrolling=False)

# ── Gate scene ────────────────────────────────────────────────────
def render_gate_scene(trust, mood, latest_msg, player_name, clue):
    pct = int(trust / MAX_TRUST * 100)
    is_open = trust >= TRUST_TO_OPEN
    gate_color = "#27c2ff" if trust >= TRUST_TO_ENTER else ("#7c5cff" if is_open else "#3a2e5a")
    mood_colors = {"Suspicious":"#d85757","Watching":"#d9a441","Curious":"#7c5cff","Accepting":"#18b47b"}
    mc = mood_colors.get(mood, "#7c5cff")
    dialogue = _h.escape(latest_msg.split(":",1)[-1].strip() if ":" in latest_msg else latest_msg)
    name_esc  = _h.escape(player_name or "Traveler")
    clue_esc  = _h.escape(clue)
    components.html(f"""<!DOCTYPE html><html><head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Rajdhani:wght@400;600;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{width:100%;height:420px;overflow:hidden;background:linear-gradient(180deg,#0a0520 0%,#1a0a40 50%,#0a0818 100%);font-family:'Rajdhani',sans-serif;}}
.scene{{position:relative;width:100%;height:420px;}}
.stars{{position:absolute;inset:0;}}
.gate-wrap{{position:absolute;left:50%;top:30px;transform:translateX(-50%);}}
.pillar{{position:absolute;top:0;width:36px;height:200px;background:linear-gradient(180deg,#2a2440,#16122a);border-radius:4px;}}
.pillar.left{{left:0;}}.pillar.right{{right:0;}}
.arch{{position:absolute;top:0;left:36px;right:36px;height:80px;border-top:8px solid {gate_color};
  border-left:4px solid {gate_color};border-right:4px solid {gate_color};border-radius:60px 60px 0 0;
  box-shadow:0 0 30px {gate_color}88,0 0 60px {gate_color}44;}}
.door{{position:absolute;top:80px;left:36px;right:36px;bottom:0;background:#08060f;
  border-left:2px solid #2a2440;border-right:2px solid #2a2440;}}
.door-glow{{position:absolute;inset:0;background:linear-gradient(180deg,{gate_color}22,transparent);
  {'animation:pulse-glow 2s ease-in-out infinite;' if is_open else ''}}}
@keyframes pulse-glow{{0%,100%{{opacity:.4;}}50%{{opacity:1;}}}}
.trust-bar-wrap{{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:200px;text-align:center;}}
.trust-label{{font-size:.55rem;color:#95a2b8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px;}}
.trust-bg{{height:5px;border-radius:3px;background:rgba(255,255,255,.08);overflow:hidden;}}
.trust-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,#7c5cff,#27c2ff);width:{pct}%;transition:width .6s;}}
.sentinel-card{{position:absolute;right:3%;bottom:20px;width:140px;background:rgba(10,8,28,.97);
  border:1.5px solid {mc}88;border-radius:14px;padding:10px;text-align:center;
  box-shadow:0 0 24px {mc}44;animation:float-s 4s ease-in-out infinite;}}
@keyframes float-s{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-8px);}}}}
.sentinel-name{{font-size:.6rem;font-weight:700;color:{mc};text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px;}}
.sentinel-mood{{font-size:.55rem;color:#95a2b8;margin-bottom:6px;}}
.sentinel-avatar{{font-size:2.2rem;margin-bottom:4px;}}
.bubble{{position:absolute;right:160px;bottom:80px;max-width:220px;background:rgba(5,8,18,.96);
  border:1px solid {mc}66;border-radius:12px;padding:8px 12px;font-size:.75rem;color:#eef3ff;
  line-height:1.4;box-shadow:0 0 12px {mc}22;animation:bubble-in .3s ease;}}
@keyframes bubble-in{{from{{opacity:0;transform:translateY(6px);}}to{{opacity:1;transform:translateY(0);}}}}
.bubble::after{{content:"";position:absolute;right:-8px;top:14px;width:12px;height:12px;
  background:rgba(5,8,18,.96);border-right:1px solid {mc}66;border-top:1px solid {mc}66;transform:rotate(45deg);}}
.clue{{position:absolute;top:12px;left:12px;background:rgba(5,8,18,.88);border:1px solid rgba(255,255,255,.1);
  border-radius:999px;padding:4px 12px;font-size:.65rem;color:#e9f1ff;max-width:300px;backdrop-filter:blur(6px);}}
.open-hint{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-family:'Cinzel',serif;font-size:1rem;font-weight:700;color:{gate_color};
  letter-spacing:.2em;text-transform:uppercase;text-shadow:0 0 20px {gate_color};
  {'display:block;' if is_open else 'display:none;'}}}
</style></head><body><div class="scene">
<svg class="stars" viewBox="0 0 800 420" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="420" fill="transparent"/>
  <g opacity=".6"><circle cx="50" cy="30" r="1" fill="#fff"/><circle cx="150" cy="60" r="1.2" fill="#fff"/>
  <circle cx="250" cy="20" r="1" fill="#fff"/><circle cx="400" cy="15" r="1.5" fill="#fff"/>
  <circle cx="550" cy="40" r="1" fill="#fff"/><circle cx="650" cy="25" r="1.2" fill="#fff"/>
  <circle cx="750" cy="55" r="1" fill="#fff"/><circle cx="100" cy="80" r="1" fill="#fff"/>
  <circle cx="700" cy="70" r="1.2" fill="#fff"/><circle cx="350" cy="50" r="1" fill="#fff"/></g>
  <g opacity=".5">
    <polygon points="0,280 80,200 160,280" fill="#0d0b22"/>
    <polygon points="120,280 240,180 360,280" fill="#0a0818"/>
    <polygon points="300,280 450,160 600,280" fill="#0c0a20"/>
    <polygon points="560,280 700,175 800,280" fill="#0a0818"/>
  </g>
  <rect x="0" y="340" width="800" height="80" fill="#060410"/>
</svg>
<div class="gate-wrap" style="width:200px;height:200px;">
  <div class="pillar left"></div>
  <div class="pillar right"></div>
  <div class="arch"></div>
  <div class="door"><div class="door-glow"></div></div>
</div>
<div class="open-hint">Gate Opening…</div>
<div class="clue">💡 {clue_esc}</div>
<div class="bubble">{dialogue}</div>
<div class="sentinel-card">
  <div class="sentinel-avatar">🗿</div>
  <div class="sentinel-name">The Sentinel</div>
  <div class="sentinel-mood">{_h.escape(mood)}</div>
</div>
<div class="trust-bar-wrap">
  <div class="trust-label">Trust Core — {trust}/{MAX_TRUST}</div>
  <div class="trust-bg"><div class="trust-fill"></div></div>
</div>
</div></body></html>""", height=420, scrolling=False)

# ── Chat log ──────────────────────────────────────────────────────
def render_chat_log(messages: list):
    if not messages: return
    lines = []
    for m in messages[-8:]:
        if m.startswith("[YOU]"):
            lines.append(f"<div style='color:#27c2ff;font-size:.78rem;padding:2px 0;'>{_h.escape(m)}</div>")
        elif m.startswith("[SENTINEL]"):
            lines.append(f"<div style='color:#c9f4ff;font-size:.78rem;padding:2px 0;'>{_h.escape(m)}</div>")
        else:
            lines.append(f"<div style='color:#95a2b8;font-size:.7rem;padding:1px 0;font-style:italic;'>{_h.escape(m)}</div>")
    st.markdown(
        f"<div style='background:rgba(5,9,18,.9);border:1px solid rgba(124,92,255,.2);border-radius:10px;"
        f"padding:10px 14px;max-height:140px;overflow-y:auto;font-family:Share Tech Mono,monospace;'>"
        + "".join(lines) + "</div>",
        unsafe_allow_html=True,
    )

# ── Rules / intro screen ──────────────────────────────────────────
def render_rules_popup():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Rajdhani:wght@400;600;700&display=swap');
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 50% 30%,#1a0a40 0%,#0a0520 55%,#050210 100%) !important;}
.rw{max-width:680px;margin:0 auto;padding:28px 20px 16px;}
.rt{font-family:'Cinzel',serif;font-size:2rem;font-weight:700;color:#fff;text-align:center;letter-spacing:.18em;
  text-transform:uppercase;margin-bottom:4px;text-shadow:0 0 40px rgba(124,92,255,.9);}
.rs{text-align:center;font-size:.75rem;color:#7c5cff;letter-spacing:.2em;text-transform:uppercase;
  margin-bottom:18px;font-family:'Rajdhani',sans-serif;}
.rd{height:1px;background:linear-gradient(90deg,transparent,rgba(124,92,255,.7),rgba(39,194,255,.5),transparent);margin-bottom:18px;}
.rg{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;}
.rc{background:rgba(124,92,255,.08);border:1px solid rgba(124,92,255,.25);border-radius:12px;padding:12px 14px;display:flex;gap:10px;}
.ri{font-size:1.4rem;flex-shrink:0;}
.rtt{font-size:.75rem;font-weight:700;color:#c9f4ff;letter-spacing:.06em;text-transform:uppercase;margin-bottom:2px;font-family:'Rajdhani',sans-serif;}
.rd2{font-size:.68rem;color:#95a2b8;line-height:1.5;font-family:'Rajdhani',sans-serif;}
.tip{background:rgba(242,193,79,.07);border:1px solid rgba(242,193,79,.28);border-radius:10px;padding:10px 16px;
  margin-bottom:18px;font-size:.72rem;color:#f2c14f;line-height:1.6;text-align:center;font-family:'Rajdhani',sans-serif;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#7c5cff,#27c2ff)!important;border:none!important;
  border-radius:12px!important;font-family:'Cinzel',serif!important;font-size:1rem!important;font-weight:700!important;
  color:#fff!important;letter-spacing:.15em!important;padding:14px 0!important;min-height:50px!important;
  box-shadow:0 0 30px rgba(124,92,255,.5)!important;text-transform:uppercase!important;}
</style>
<div class="rw">
  <div class="rt">⚔ The Sentinel Awakens</div>
  <div class="rs">Lesson 4 — Build the Trust Gate</div>
  <div class="rd"></div>
  <div class="rg">
    <div class="rc"><div class="ri">🗣️</div><div><div class="rtt">Speak Wisely</div><div class="rd2">Polite, respectful words earn Trust. Rude words lose it fast.</div></div></div>
    <div class="rc"><div class="ri">🔒</div><div><div class="rtt">Solve the Riddle</div><div class="rd2">A logic lock guards the gate. Solve it for a big Trust boost.</div></div></div>
    <div class="rc"><div class="ri">📊</div><div><div class="rtt">Build Trust (0–100)</div><div class="rd2">Reach 35 to open the gate. Reach 65 to enter the vault.</div></div></div>
    <div class="rc"><div class="ri">🔥</div><div><div class="rtt">Streak Bonus</div><div class="rd2">3 good actions in a row — each earns bonus Trust points.</div></div></div>
  </div>
  <div class="tip">💡 Say <b>"please"</b>, <b>"I understand"</b>, <b>"I respect your power"</b> — the Sentinel responds to humility.</div>
</div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        if st.button("⚔  Begin Your Journey", use_container_width=True, key="begin_btn", type="primary"):
            st.session_state.rules_accepted = True
            st.rerun()
