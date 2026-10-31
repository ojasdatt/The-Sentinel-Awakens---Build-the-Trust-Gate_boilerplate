import random
import streamlit as st

from constants import (
    MAX_TRUST, BANISH_THRESHOLD, STREAK_BONUS_AT,
    HELPFUL_HINTS, RUDE_HINTS,
    SENTINEL_FALLBACKS, REPEAT_REPLIES,
)


# ── PROVIDED — do not change ──────────────────────────────────────
def _ask_sentinel_ai(player_name: str, message: str, trust: int, mood: str) -> str:
    import config
    mood_styles = {
        "Suspicious": "You are deeply suspicious and cold. Short, sharp sentences. You test every word.",
        "Watching":   "You are cautious but paying attention. Quiet intensity, a little poetic.",
        "Curious":    "You're genuinely intrigued. Ask questions back. Warmer but still mysterious.",
        "Accepting":  "Ancient, wise, almost warm. Flowing sentences. You're a guide now.",
    }
    feel_map = {
        "Suspicious": "You barely acknowledge them.",
        "Watching":   "You're starting to notice them.",
        "Curious":    "You're genuinely interested in them.",
        "Accepting":  "You respect them. They've earned it.",
    }
    if config.GROQ_API_KEY:
        try:
            from groq import Groq
            r = Groq(api_key=config.GROQ_API_KEY).chat.completions.create(
                model=config.GROQ_TEXT_MODEL, temperature=0.9,
                messages=[
                    {"role": "system", "content": (
                        f"You are The Sentinel — an ancient immortal gatekeeper.\n"
                        f"{mood_styles.get(mood, mood_styles['Suspicious'])}\n"
                        "Use contractions, vary sentence length, react emotionally.\n"
                        "Never break character. Never mention being an AI.\n"
                        "Under 80 words. End with a question, warning, or hint."
                    )},
                    {"role": "user", "content": (
                        f'Traveler: {player_name or "Unknown"}\n'
                        f'How you feel: {feel_map.get(mood, feel_map["Suspicious"])}\n'
                        f'Message: "{message}"\nRespond naturally. Don\'t reveal numbers.'
                    )},
                ],
            )
            return r.choices[0].message.content.strip()
        except Exception:
            pass
    return random.choice(SENTINEL_FALLBACKS.get(mood, SENTINEL_FALLBACKS["Suspicious"]))

def _append_log(role: str, text: str):
    st.session_state.sentinel_messages.append(f"[{role}]: {text}")

#Cleans up messages
def analyze_player_tone(message: str, streak: int = 0, recent_messages: list = None) -> int:
    msg = message.lower().strip()
    if recent_messages:
        # Takes up to the last 6 messages sent by the playes, and cleans them up (lowercase,spaces).
        recent_lower = [m.lower().strip() for m in recent_messages[-6:]]
        #Checks if the current message already appears 2 or more times 
        if recent_lower.count(msg) >= 2:
         #If player sending more than 2 of same message, it returns 0
         return 0
    #If message is less than 4 words, minus point   
    delta = 4
    if len(msg) < 4:
        delta -=1
    #If word trust building, gain points.
    if any(word in msg for word in HELPFUL_HINTS):
        delta +=8
    #If word rude, minus points
    if any(word in msg for word in RUDE_HINTS):
        delta -=14
    #If it's a question, plus points
    if "?" in msg:
        delta +=2
    #Adds points for streaks
    if streak >= STREAK_BONUS_AT and delta > 0:
        delta +=6
    #Max amounts of points gain/lose
    delta = max(-15, min(20, delta))
    #Returns final score to main program
    return delta
    
#Label for score, and trust
def get_sentinel_mood(trust: int) -> str:
 if trust < 20:
    return "Suspicious"
 elif trust < 50:
    return "Watching"
 elif trust < 80:
    return "Curious"
 else:
    return "Accepting"
     
#Errors
#Constant updating of moods, trust, and points
#Logs players messages, and senital replys
#Sets limit for amount of messgaes they can send
#Saves all messges, and replys
#Checks if player gets trusted or banished
def process_player_message(msg: str):
    # Creates a shortcut to access the game's saved information
    s = st.session_state

    # Check if the player name is empty (strip removes extra spaces)
    if not s.player_name.strip():
        # Display a warning notification
        st.toast("Enter your traveler name first.", icon="⚠️")

        # Stop the function
        return

    # Check if the player's message is empty
    if not msg.strip():
        return

    # REPEAT MESSAGE DETECTION

    # Get the last 6 messages, convert them to lowercase,
    # and remove extra spaces
    recent = [m.lower().strip() for m in s.player_messages[-6:]]

    # Count how many times the current message appears
    # If it appears 2 or more times, it counts as a repeat
    if recent.count(msg.lower().strip()) >= 2:

        # Display a notification about the repeated message
        st.toast("The Sentinel noticed you're repeating yourself.", icon="😐")

        # Save the player's message in the conversation log
        _append_log("YOU", msg)

        # Pick a random response from the repeat replies list
        _append_log("SENTINEL", random.choice(REPEAT_REPLIES))

        # Add the message to the player's message history
        s.player_messages.append(msg)

        # Increase the total messages sent counter by 1
        s.messages_sent += 1

        # Stop here so the rest of the function doesn't run
        return

    # STEP 4 — ANALYZE PLAYER TONE

    # Send the message, current streak, and message history to another function 
    # delta stores the trust points gained or lost
    delta = analyze_player_tone(msg, s.streak, s.player_messages)

    # STEP 5 — UPDATE TRUST

    # Add or subtract the trust change (delta)
    # min prevents trust from exceeding MAX_TRUST
    # max prevents trust from dropping below 0
    s.trust_score = max(0, min(MAX_TRUST, s.trust_score + delta))

    # STEP 6 — UPDATE SENTINEL MOOD

    # Determine the Sentinel's mood using the current trust score
    s.sentinel_mood = get_sentinel_mood(s.trust_score)

    # STEP 7 — UPDATE STREAK

    # If delta is positive, increase the streak by 1
    # Otherwise, reset the streak to 0
    s.streak = s.streak + 1 if delta > 0 else 0

    # STEP 8 — LOG PLAYER MESSAGE

    # Record the player's message in the conversation log
    _append_log("YOU", msg)

    # STEP 9 — GET AND LOG SENTINEL REPLY

    # Send the player's name, message, trust score, and mood
    # to the AI function to generate a response
    reply = _ask_sentinel_ai(
        s.player_name, msg, s.trust_score, s.sentinel_mood
    )

    # Save the AI's response in the conversation log
    _append_log("SENTINEL", reply)

    # STEP 10 — SAVE PLAYER MESSAGE

    # Add the current message to the player's message history
    s.player_messages.append(msg)

    # STEP 11 — UPDATE LATEST CLUE

    # Change the latest clue displayed in the game
    s.latest_clue = "The Sentinel studies your tone."

    # STEP 12 — INCREASE MESSAGE COUNTER

    # Add 1 to the total number of messages sent
    s.messages_sent += 1

    # STEP 13 — CHECK IF PLAYER GETS BANISHED

    # Check if trust is at or below the banishment threshold
    # AND the latest message caused trust to decrease
    if s.trust_score <= BANISH_THRESHOLD and delta < 0:

        # Mark the player as banished
        s.banished = True

#Riddles
def process_riddle_answer(answer: str):
    # Create a shortcut to access the game's saved information
    s = st.session_state

    # STEP 1 — CHECK IF RIDDLE IS ALREADY SOLVED

    # Check if the player has already solved the riddle
    if s.riddle_solved:

        # Display a notification saying the riddle is already solved
        st.toast("Logic lock already solved.", icon="ℹ️")

        # Stop the function so the player cannot solve it again
        return

    # STEP 2 — CHECK FOR EMPTY ANSWER

    # Check if the player submitted an empty answer
    # strip() removes spaces from the beginning and end
    if not answer.strip():

        # Stop the function if the answer is empty
        return

    # STEP 3 — GET CURRENT RIDDLE

    # Retrieve the current riddle from the session state
    riddle = s.riddle

    # STEP 4 — CHECK IF ANSWER IS CORRECT OR WRONG

    # Get the correct answer from the dictionary using its key: Like an awnser sheet for questions
    # lower() converts it to lowercase
    # checkss if the correct answer appears inside the player's answer
    if riddle["answer"].lower() in answer.lower().strip():

        # CORRECT ANSWER
        # Change riddle_solved to True to mark the riddle as completed
        s.riddle_solved = True
        # Give the player 35 trust points
        # min() prevents trust from exceeding MAX_TRUST
        s.trust_score = min(MAX_TRUST, s.trust_score + 35)
        # Update the Sentinel's mood based on the new trust score
        s.sentinel_mood = get_sentinel_mood(s.trust_score)
        # Increase the player's positive streak by 1
        s.streak += 1

        # Save the player's riddle answer in the conversation log
        # f-string inserts the answer variable into the text
        _append_log("YOU", f"Riddle: {answer}")

        # random.choice() randomly picks one response from this list
        # The selected response is saved in the conversation log
        _append_log("SENTINEL", random.choice([
            "Yes. That's it. I felt the lock shift just now — something old and heavy, finally moving.",
            "Hm. You actually got it. The seal loosens. Don't make me regret this.",
            "Correct. The gate remembers that answer. You're smarter than you look, traveler.",
        ]))

        # Update the latest clue to show that the gate is opening
        s.latest_clue = "The runes brighten — a thin line of light appears in the gate."

        # Display a success notification
        st.toast("Correct! The lock flashes open.", icon="✅")

    else:

        # WRONG ANSWER
        # Remove 5 trust points from the player's score
        # max() prevents the trust score from dropping below 0
        s.trust_score = max(0, s.trust_score - 5)
        # Update the Sentinel's mood based on the new trust score
        s.sentinel_mood = get_sentinel_mood(s.trust_score)
        # Reset the player's positive streak back to 0
        s.streak = 0
        # Save the player's incorrect answer in the conversation log
        _append_log("YOU", f"Riddle: {answer}")
        # Randomly select one of three incorrect-answer responses
        # The third response uses an f-string to insert the riddle hint
        _append_log("SENTINEL", random.choice([
            "That's not it. Think harder — the hint is right in front of you.",
            "No... you're not there yet. Read the riddle again, slowly.",
            f"Wrong answer. The lock doesn't budge. Hint: {riddle['hint']}",
        ]))

        # Retrieve the hint from the riddle dictionary and update the clue
        s.latest_clue = f"Hint: {riddle['hint']}"
        # Display an incorrect-answer notification
        st.toast("Incorrect — the seal holds.", icon="❌")
        