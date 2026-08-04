import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Accounting Bucket List", layout="wide")
st.title("Accounting Bucket List")

# The following string contains the complete HTML, CSS, and JavaScript for the game.
# It uses the HTML5 Drag and Drop API.
custom_game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; }
    #game-board { display: flex; justify-content: space-around; width: 100%; margin-bottom: 30px; }
    
    /* Bucket Styling */
    .bucket {
        width: 150px;
        height: 150px;
        border: 3px dashed #ccc;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f9f9f9;
        transition: background-color 0.3s;
    }
    .bucket.drag-over { background-color: #e0f7fa; border-color: #00bcd4; }
    
    /* Card Pool Styling */
    #card-pool { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; width: 80%; border: 2px solid #ddd; padding: 20px; border-radius: 10px; min-height: 100px;}
    
    /* Individual Card Styling */
    .card {
        padding: 15px;
        background-color: #fff;
        border: 2px solid #333;
        border-radius: 5px;
        cursor: grab;
        width: 200px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .card:active { cursor: grabbing; }
    
    /* Animations */
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(3px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(1px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    .shake-animation { animation: shake 0.5s; }
    
    #score-board { font-size: 24px; font-weight: bold; margin-bottom: 20px; }
</style>
</head>
<body>

<div id="score-board">Score: <span id="score">0</span></div>

<!-- Drop Zones (Buckets) -->
<!-- To use custom images, add an <img> tag inside these divs or set CSS background-image -->
<div id="game-board">
    <div class="bucket" data-type="Assets">Assets</div>
    <div class="bucket" data-type="Liabilities">Liabilities</div>
    <div class="bucket" data-type="Equity">Equity</div>
    <div class="bucket" data-type="Revenue">Revenue</div>
    <div class="bucket" data-type="Expenses">Expenses</div>
</div>

<!-- Draggable Items (Cards) -->
<div id="card-pool">
    <div class="card" draggable="true" data-target="Assets" id="card1">Cash, inventory, and equipment</div>
    <div class="card" draggable="true" data-target="Liabilities" id="card2">Amounts owed to suppliers</div>
    <div class="card" draggable="true" data-target="Equity" id="card3">Owner's claim to resources</div>
    <div class="card" draggable="true" data-target="Revenue" id="card4">Amounts earned from selling</div>
    <div class="card" draggable="true" data-target="Expenses" id="card5">Costs incurred to generate revenue</div>
</div>

<audio id="snd-correct" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
<audio id="snd-incorrect" src="https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3"></audio>

<script>
    let score = 0;
    const cards = document.querySelectorAll('.card');
    const buckets = document.querySelectorAll('.bucket');
    const scoreDisplay = document.getElementById('score');
    
    const sndCorrect = document.getElementById('snd-correct');
    const sndIncorrect = document.getElementById('snd-incorrect');

    cards.forEach(card => {
        card.addEventListener('dragstart', dragStart);
        card.addEventListener('dragend', dragEnd);
    });

    buckets.forEach(bucket => {
        bucket.addEventListener('dragover', dragOver);
        bucket.addEventListener('dragenter', dragEnter);
        bucket.addEventListener('dragleave', dragLeave);
        bucket.addEventListener('drop', dragDrop);
    });

    let draggedItem = null;

    function dragStart(e) {
        draggedItem = this;
        setTimeout(() => this.style.opacity = '0.5', 0);
    }

    function dragEnd() {
        draggedItem.style.opacity = '1';
        draggedItem = null;
    }

    function dragOver(e) {
        e.preventDefault();
    }

    function dragEnter(e) {
        e.preventDefault();
        this.classList.add('drag-over');
    }

    function dragLeave() {
        this.classList.remove('drag-over');
    }

    function dragDrop() {
        this.classList.remove('drag-over');
        
        const expectedTarget = draggedItem.getAttribute('data-target');
        const bucketType = this.getAttribute('data-type');

        if (expectedTarget === bucketType) {
            // Correct Match
            this.appendChild(draggedItem);
            draggedItem.setAttribute('draggable', 'false');
            draggedItem.style.cursor = 'default';
            score += 10;
            scoreDisplay.innerText = score;
            sndCorrect.currentTime = 0;
            sndCorrect.play();
        } else {
            // Incorrect Match
            score -= 5;
            scoreDisplay.innerText = score;
            sndIncorrect.currentTime = 0;
            sndIncorrect.play();
            
            // Trigger shake animation
            draggedItem.classList.add('shake-animation');
            setTimeout(() => {
                draggedItem.classList.remove('shake-animation');
            }, 500);
        }
    }
</script>
</body>
</html>
"""

# Render the custom HTML component in Streamlit
components.html(custom_game_html, height=700, scrolling=False)