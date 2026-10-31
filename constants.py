# ── PROVIDED — do not edit ────────────────────────────────────────
# All fixed game values used across the lesson.

APP_TITLE    = "AI Mystery Vault — Lesson 4"
MAX_TRUST    = 100
TRUST_TO_OPEN  = 35
TRUST_TO_ENTER = 65
BANISH_THRESHOLD = 0
STREAK_BONUS_AT  = 2

BG       = "#071018"
ACCENT   = "#7c5cff"
ACCENT_2 = "#27c2ff"
TEXT     = "#e5ecf4"
MUTED    = "#95a2b8"
SUCCESS  = "#18b47b"
WARNING  = "#d9a441"
DANGER   = "#d85757"

RUDE_HINTS    = ["stupid", "move", "idiot", "boring", "shut up", "useless", "hurry", "dumb", "fool"]
HELPFUL_HINTS = ["please", "sorry", "thank you", "help", "respect", "honor", "understand", "greet", "bow", "humble"]

RIDDLES = [
    {"question": "I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?", "answer": "keyboard", "hint": "You use me to type."},
    {"question": "The more you take, the more you leave behind. What am I?",                                          "answer": "footsteps","hint": "Think about walking."},
    {"question": "I speak without a mouth and hear without ears. I come alive with wind. What am I?",                 "answer": "echo",     "hint": "Sound returns to you in caves."},
    {"question": "The more you feed me, the more I grow. Give me water and I die. What am I?",                        "answer": "fire",     "hint": "I light the forge and warm the vault."},
    {"question": "What has hands but cannot clap?",                                                                   "answer": "clock",    "hint": "It tells you something every second."},
]

SENTINEL_FALLBACKS = {
    "Suspicious": [
        "You're here. That's something. But the gate doesn't open for just anyone.",
        "I've been watching you. I'm not impressed yet. Say something worth hearing.",
        "The vault is old. Older than your world. You'll need more than words to move it.",
    ],
    "Watching": [
        "You're getting somewhere. I can feel it. Keep going.",
        "Something in your voice is changing. The gate feels it too.",
        "Not bad. You're starting to sound like someone who belongs here.",
    ],
    "Curious": [
        "You're close. Closer than most ever get. Don't stop now.",
        "The vault is listening to you now. Really listening. One more push.",
        "I haven't opened these doors in a very long time. You might just be the one.",
    ],
    "Accepting": [
        "You've done it. I didn't think anyone would, but here we are. Go on — the vault is yours.",
        "The seal breaks for you. Walk carefully. What's inside has been waiting a long time.",
        "Well. I've guarded this place for a thousand years and you're the first to truly earn it.",
    ],
}

REPEAT_REPLIES = [
    "You've said that already. Word for word. Say something new — or don't say anything at all.",
    "Again? That exact phrase? I remember every word spoken here. Try harder.",
    "I heard you the first time. Repeating yourself won't open this gate.",
    "Same words again. The gate doesn't respond to echoes, traveler.",
]
