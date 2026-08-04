import streamlit as st
import random
import base64
import os

# 1. Configuration and Data Setup
st.set_page_config(page_title="Accounting Bucket List", layout="centered")

# Replace this sample data with the contents of your provided files
# Format: {"card_text": "Definition or Account Title", "correct_bucket": "Bucket Name"}
MASTER_DECK = [
    {"card_text": "Cash, inventory, and equipment.", "correct_bucket": "Assets"},
    {"card_text": "Amounts owed to suppliers (Accounts Payable).", "correct_bucket": "Liabilities"},
    {"card_text": "Owner's claim to company resources (Common Stock).", "correct_bucket": "Equity"},
    {"card_text": "Amounts earned from selling goods or services.", "correct_bucket": "Revenue"},
    {"card_text": "Costs incurred to generate revenue (Rent, Utilities).", "correct_bucket": "Expenses"}
]

BUCKETS = ["Assets", "Liabilities", "Equity", "Revenue", "Expenses"]

# 2. Helper Functions for Audio
def play_sound(file_name):
    """Embeds an invisible HTML audio player to autoplay sound."""
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay class="stAudio">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)

# 3. Session State Initialization
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'deck' not in st.session_state:
    shuffled = MASTER_DECK.copy()
    random.shuffle(shuffled)
    st.session_state.deck = shuffled
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'message' not in st.session_state:
    st.session_state.message = ""

# 4. Game Logic
def check_answer(selected_bucket):
    current_card = st.session_state.deck[st.session_state.current_index]
    
    if selected_bucket == current_card["correct_bucket"]:
        st.session_state.score += 10
        st.session_state.message = "Correct!"
        play_sound("correct.mp3") # Ensure you have a correct.mp3 file in the directory
    else:
        st.session_state.score -= 5
        st.session_state.message = f"Incorrect. That belongs in {current_card['correct_bucket']}."
        play_sound("incorrect.mp3") # Ensure you have an incorrect.mp3 file in the directory
        
    st.session_state.current_index += 1
    
    if st.session_state.current_index >= len(st.session_state.deck):
        st.session_state.game_over = True

def reset_game():
    st.session_state.score = 0
    st.session_state.current_index = 0
    shuffled = MASTER_DECK.copy()
    random.shuffle(shuffled)
    st.session_state.deck = shuffled
    st.session_state.game_over = False
    st.session_state.message = ""

# 5. User Interface
st.title("Accounting Bucket List")

if not st.session_state.game_over:
    # Display Score and Progress
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score", st.session_state.score)
    with col2:
        st.metric("Card", f"{st.session_state.current_index + 1} / {len(st.session_state.deck)}")
    
    # Display Feedback Message
    if st.session_state.message:
        if "Correct" in st.session_state.message:
            st.success(st.session_state.message)
        else:
            st.error(st.session_state.message)

    # Display Current Card
    st.markdown("---")
    current_card_text = st.session_state.deck[st.session_state.current_index]["card_text"]
    st.markdown(f"<h3 style='text-align: center;'>{current_card_text}</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Display Buckets as interactive buttons
    st.write("### Select the correct bucket:")
    
    # Create a dynamic grid of buttons based on the number of buckets
    cols = st.columns(len(BUCKETS))
    for i, bucket in enumerate(BUCKETS):
        with cols[i]:
            if st.button(bucket, key=bucket, use_container_width=True):
                check_answer(bucket)
                st.rerun()

else:
    # Game Over Sequence
    st.balloons()
    st.header("Activity Complete")
    st.metric("Final Score", st.session_state.score)
    
    if st.button("Play Again"):
        reset_game()
        st.rerun()