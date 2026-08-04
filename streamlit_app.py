import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Accounting Bucket List", layout="wide")

# Card data to be randomized on each load
card_data = [
    {"target": "CASH Account", "text": "Currency on hand, coin, and balance in bank checking & savings accounts (money owned)"},
    {"target": "Sales Revenue", "text": "Amounts earned by a company from selling physical products (goods) to customers"},
    {"target": "Accounts Payable", "text": "Amounts owed to vendors (suppliers) for purchases made on account & not yet paid"},
    {"target": "Service Revenue", "text": "Amounts earned by a company from selling & performing services for customers"},
    {"target": "Equipment", "text": "Machinery, computers, tools, & vehicles owned by a company & used in operations"},
    {"target": "Retained Earnings", "text": "Cumulative sum of past profits earned over time, not distributed (paid) as dividends to shareholders"},
    {"target": "Inventory", "text": "Products (goods) a company owns and is being held for the purpose of resale to customers"},
    {"target": "Accounts Receivable", "text": "Amounts customers owe the company for products or services sold on credit (Due from customers)"},
    {"target": "Utilities Expense", "text": "Cost incurred for use of electricity, Internet, water & sewage necessary to operate the business"},
    {"target": "Land & Buildings", "text": "Land & physical stores used in a retailer's operations"},
    {"target": "Intangible Assets", "text": "Patents, Trademarks, & Copyrights"},
    {"target": "Land Investments", "text": "Land owned but not used in operations; being held for future use or capital appreciation, e.g., will build a store in 3 yrs."},
    {"target": "Unearned Revenue", "text": "Amounts received in advance from customers before goods or services have been delivered or performed"},
    {"target": "Cost of Goods Sold", "text": "Cost of inventory that was sold to customers; cost that was paid to suppliers for items sold"},
    {"target": "Interest Expense", "text": "Cost incurred for borrowing money from creditors arising from loans, mortgages, bonds."},
    {"target": "Common Stock", "text": "Total amount paid-in (invested) in the corp. by stockholders (investors) in exchange for shares of ownership"},
    {"target": "Supplies", "text": "Goods owned & on-hand for future that will be used/consumed in operations (not for resale)"},
    {"target": "Supplies Expense", "text": "Office supplies & cleaning supplies that have been consumed/used in operations"},
    {"target": "NET INCOME (LOSS)", "text": "Total Revenue less Total Expenses for an accounting period"},
    {"target": "Stock Investments", "text": "Amount a company invests in another corporation by buying their stock with plans to hold it for the long-term"},
    {"target": "Cost of Goods Sold", "text": "Cost of products sold; EX: cost Walmart incurred to buy the sold merchandise from suppliers"},
    {"target": "Mortgage Payable", "text": "Amount due on a 20-year mortgage to finance purchase of a building"},
    {"target": "Advertising Expense", "text": "Cost incurred for services used to design marketing materials & promote the business and its products."},
    {"target": "Prepaid", "text": "Paid rent to landlord two months in advance for future occupancy, e.g., effective next month"},
    {"target": "Wages Payable", "text": "Salary & wages owed to employees for work performed, but company has not yet paid"},
    {"target": "Salaries & Wages Expense", "text": "Cost of labor performed by employees during a period (cost of labor services used by the company)"},
    {"target": "Notes Payable due > 12 mos.", "text": "Amount due to a creditor (bank) after 12 months evidenced by a written, signed promissory note."}
]

# Randomize card order
random.shuffle(card_data)

# Generate HTML for cards
cards_html = ""
for i, card in enumerate(card_data):
    cards_html += f'<div class="card" draggable="true" data-target="{card["target"]}" id="card{i}"><span>{card["text"]}</span></div>\n'

custom_game_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/mobile-drag-drop@2.3.0-rc.2/default.css">
<script src="https://cdn.jsdelivr.net/npm/mobile-drag-drop@2.3.0-rc.2/index.min.js"></script>

<style>
    body, html {{ 
        margin: 0; 
        padding: 0; 
        height: 100%; 
        font-family: sans-serif; 
        overflow: hidden; 
        touch-action: none; 
    }}
    
    #main-container {{
        height: 100vh;
        overflow-y: auto;
        box-sizing: border-box;
        background-color: #f4f4f9;
        -webkit-overflow-scrolling: touch;
    }}

    /* Persistent Header */
    #header-container {{
        position: sticky;
        top: 0;
        background: #ffffff;
        z-index: 1000;
        padding: 10px 15px;
        border-bottom: 2px solid #ddd;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px -6px #222;
    }}

    #header-title {{
        font-size: 24px;
        font-weight: bold;
        margin: 0;
        text-align: center;
        flex-grow: 1;
        color: #333;
    }}

    #score-board {{ 
        font-size: 20px; 
        font-weight: bold; 
        margin: 0; 
        color: #e63946;
        min-width: 90px;
        text-align: right;
    }}
    
    /* Layout */
    .layout-container {{
        display: flex;
        flex-direction: row;
        gap: 20px;
        align-items: flex-start;
        width: 100%;
        padding: 15px;
        box-sizing: border-box;
    }}
    
    #game-board {{ 
        flex: 1.5; 
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding-bottom: 20px;
    }}
    
    .section {{
        border: 2px solid #aaa;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }}
    
    .section-header {{
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #222;
    }}
    
    .bucket-grid {{
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); 
        gap: 15px; 
    }}

    /* Color Coding - Applied to section backgrounds */
    .assets {{ background-color: #e3f2fd; border-color: #90caf9; }}
    .liabilities {{ background-color: #ffebee; border-color: #ef9a9a; }}
    .equity {{ background-color: #f3e5f5; border-color: #ce93d8; }}
    .revenue {{ background-color: #fff3e0; border-color: #ffcc80; }}
    .expenses {{ background-color: #e8f5e9; border-color: #a5d6a7; }}
    .net-income {{ background-color: #fffde7; border-color: #fff59d; }}
    
    /* Transparent Pail Styling */
    .bucket {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end; 
        min-height: 140px;
        padding: 10px;
        font-size: 13px;
        font-weight: 800;
        text-align: center;
        color: #111;
        position: relative;
        
        /* Removed all borders and backgrounds */
        border: none !important;
        background-color: transparent !important;
        
        transition: transform 0.2s, filter 0.2s;
        
        /* Updated Sand Pail Raw URL */
        background-image: url('https://raw.githubusercontent.com/cybercrs/ACC-202-Bucket-Game/8bb985afef7866ffb440aee0da29e64a5ef40392/Bucket%20Image%2002.png');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }}

    .bucket.drag-over {{ 
        transform: scale(1.1);
        /* Subtle glow instead of an outline */
        filter: drop-shadow(0px 0px 8px #e63946);
    }}
    
    /* Card Pool Styling */
    #card-pool {{ 
        flex: 1; 
        min-width: 300px;
        display: flex; 
        flex-wrap: wrap; 
        gap: 10px; 
        justify-content: center; 
        border: 2px solid #ddd; 
        padding: 15px; 
        border-radius: 10px; 
        background-color: #ffffff;
        position: sticky;
        top: 70px;
        max-height: calc(100vh - 90px);
        overflow-y: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }}
    
    /* Transparent Sand Grain Styling */
    .card {{
        /* Adjust padding so text stays strictly inside the grain graphic */
        padding: 15px 20px;
        cursor: grab;
        width: 45%; 
        max-width: 170px;
        min-height: 90px;
        font-size: 11px;
        text-align: center;
        color: #111;
        font-weight: 800;
        
        /* Text shadow to ensure readability on the image */
        text-shadow: 1px 1px 2px rgba(255,255,255,0.7);
        
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.1s;
        
        /* Removed all outlines */
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        
        /* Updated Sand Grain Raw URL */
        background-image: url('https://raw.githubusercontent.com/cybercrs/ACC-202-Bucket-Game/8bb985afef7866ffb440aee0da29e64a5ef40392/Sand%20Grain%20Image%2002.png');
        background-size: 100% 100%; /* Stretches graphic slightly to contain text completely */
        background-repeat: no-repeat;
        background-position: center;
    }}
    
    .card:active {{ 
        cursor: grabbing; 
        transform: scale(1.05);
    }}
    
    /* Dropped Card Styling - Retains sand grain appearance */
    .bucket .card {{
        width: 90%;
        min-height: 60px;
        font-size: 9px;
        padding: 10px;
        cursor: default;
        margin-top: 5px;
        
        /* Keep it looking like a piece of sand, just smaller */
        background-image: url('https://raw.githubusercontent.com/cybercrs/ACC-202-Bucket-Game/8bb985afef7866ffb440aee0da29e64a5ef40392/Sand%20Grain%20Image%2002.png');
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* Mobile Responsive Logic */
    @media (max-width: 768px) {{
        .layout-container {{
            flex-direction: column;
            padding: 10px;
        }}
        
        #game-board {{
            flex: none;
            width: 100%;
        }}
        
        #card-pool {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            max-height: 35vh; 
            border-radius: 15px 15px 0 0;
            box-shadow: 0 -5px 15px rgba(0,0,0,0.2);
            z-index: 2000;
            top: auto;
            margin: 0;
            padding: 10px;
            box-sizing: border-box;
        }}

        #main-container {{
            padding-bottom: 38vh; 
        }}

        .card {{
            width: 46%; 
            font-size: 10px;
            padding: 10px;
        }}
        
        .bucket-grid {{
            grid-template-columns: repeat(2, 1fr); 
        }}
    }}

    /* Animations */
    @keyframes shake {{
        0% {{ transform: translate(1px, 1px) rotate(0deg); }}
        10% {{ transform: translate(-1px, -2px) rotate(-1deg); }}
        20% {{ transform: translate(-3px, 0px) rotate(1deg); }}
        30% {{ transform: translate(3px, 2px) rotate(0deg); }}
        40% {{ transform: translate(1px, -1px) rotate(1deg); }}
        50% {{ transform: translate(-1px, 2px) rotate(-1deg); }}
        60% {{ transform: translate(-3px, 1px) rotate(0deg); }}
        70% {{ transform: translate(3px, 1px) rotate(-1deg); }}
        80% {{ transform: translate(-1px, -1px) rotate(1deg); }}
        90% {{ transform: translate(1px, 2px) rotate(0deg); }}
        100% {{ transform: translate(1px, -2px) rotate(-1deg); }}
    }}
    .shake-animation {{ animation: shake 0.5s; }}
</style>
</head>
<body>

<div id="main-container">
    
    <div id="header-container">
        <h1 id="header-title">Accounting Bucket List</h1>
        <div id="score-board">Score: <span id="score">0</span></div>
    </div>

    <div class="layout-container">
        <div id="game-board">
            
            <div class="section assets">
                <div class="section-header">ASSETS</div>
                <div class="bucket-grid">
                    <div class="bucket" data-type="CASH Account">CASH Account</div>
                    <div class="bucket" data-type="Accounts Receivable">Accounts Receivable</div>
                    <div class="bucket" data-type="Inventory">Inventory</div>
                    <div class="bucket" data-type="Supplies">Supplies</div>
                    <div class="bucket" data-type="Prepaid">Prepaid</div>
                    <div class="bucket" data-type="Stock Investments">Stock Investments</div>
                    <div class="bucket" data-type="Land Investments">Land Investments</div>
                    <div class="bucket" data-type="Equipment">Equipment</div>
                    <div class="bucket" data-type="Land & Buildings">Land & Buildings</div>
                    <div class="bucket" data-type="Intangible Assets">Intangible Assets</div>
                </div>
            </div>

            <div class="section liabilities">
                <div class="section-header">LIABILITIES</div>
                <div class="bucket-grid">
                    <div class="bucket" data-type="Accounts Payable">Accounts Payable</div>
                    <div class="bucket" data-type="Wages Payable">Wages Payable</div>
                    <div class="bucket" data-type="Unearned Revenue">Unearned Revenue</div>
                    <div class="bucket" data-type="Notes Payable due > 12 mos.">Notes Payable due > 12 mos.</div>
                    <div class="bucket" data-type="Mortgage Payable">Mortgage Payable</div>
                    <div class="bucket" data-type="Bonds Payable">Bonds Payable</div>
                </div>
            </div>

            <div class="section equity">
                <div class="section-header">STOCKHOLDER'S EQUITY</div>
                <div class="bucket-grid">
                    <div class="bucket" data-type="Retained Earnings">Retained Earnings</div>
                    <div class="bucket" data-type="Common Stock">Common Stock</div>
                </div>
            </div>

            <div class="section revenue">
                <div class="section-header">REVENUE</div>
                <div class="bucket-grid">
                    <div class="bucket" data-type="Service Revenue">Service Revenue</div>
                    <div class="bucket" data-type="Sales Revenue">Sales Revenue</div>
                    <div class="bucket" data-type="Interest Income">Interest Income</div>
                </div>
            </div>

            <div class="section expenses">
                <div class="section-header">EXPENSES</div>
                <div class="bucket-grid">
                    <div class="bucket" data-type="Cost of Goods Sold">Cost of Goods Sold</div>
                    <div class="bucket" data-type="Supplies Expense">Supplies Expense</div>
                    <div class="bucket" data-type="Rent Expense">Rent Expense</div>
                    <div class="bucket" data-type="Salaries & Wages Expense">Salaries & Wages Expense</div>
                    <div class="bucket" data-type="Advertising Expense">Advertising Expense</div>
                    <div class="bucket" data-type="Insurance Expense">Insurance Expense</div>
                    <div class="bucket" data-type="Interest Expense">Interest Expense</div>
                    <div class="bucket" data-type="Income Tax Expense">Income Tax Expense</div>
                </div>
            </div>

            <div class="section net-income">
                <div class="section-header">NET INCOME (LOSS)</div>
                <div class="bucket-grid">
                    <div class="bucket" data-type="NET INCOME (LOSS)">NET INCOME (LOSS)</div>
                </div>
            </div>
            
        </div>

        <div id="card-pool">
            {cards_html}
        </div>
    </div>
</div>

<audio id="snd-correct" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
<audio id="snd-incorrect" src="https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3"></audio>

<script>
    // Initialize Mobile Drag and Drop Polyfill
    MobileDragDrop.polyfill({{
        holdToDrag: 150, // milliseconds a user must hold before dragging begins
        dragImageTranslateOverride: MobileDragDrop.scrollBehaviourDragImageTranslateOverride
    }});
    
    // Required to prevent scrolling while dragging on mobile
    window.addEventListener("touchmove", function() {{}}, {{passive: false}});

    let score = 0;
    const cards = document.querySelectorAll('.card');
    const buckets = document.querySelectorAll('.bucket');
    const scoreDisplay = document.getElementById('score');
    
    const sndCorrect = document.getElementById('snd-correct');
    const sndIncorrect = document.getElementById('snd-incorrect');

    cards.forEach(card => {{
        card.addEventListener('dragstart', dragStart);
        card.addEventListener('dragend', dragEnd);
    }});

    buckets.forEach(bucket => {{
        bucket.addEventListener('dragover', dragOver);
        bucket.addEventListener('dragenter', dragEnter);
        bucket.addEventListener('dragleave', dragLeave);
        bucket.addEventListener('drop', dragDrop);
    }});

    let draggedItem = null;

    function dragStart(e) {{
        draggedItem = this;
        setTimeout(() => this.style.opacity = '0.5', 0);
    }}

    function dragEnd() {{
        draggedItem.style.opacity = '1';
        draggedItem = null;
    }}

    function dragOver(e) {{
        e.preventDefault();
    }}

    function dragEnter(e) {{
        e.preventDefault();
        this.classList.add('drag-over');
    }}

    function dragLeave() {{
        this.classList.remove('drag-over');
    }}

    function dragDrop(e) {{
        e.preventDefault();
        this.classList.remove('drag-over');
        
        // Safety check in case non-card items are dropped
        if (!draggedItem) return;

        const expectedTarget = draggedItem.getAttribute('data-target');
        const bucketType = this.getAttribute('data-type');

        if (expectedTarget === bucketType) {{
            this.appendChild(draggedItem);
            draggedItem.setAttribute('draggable', 'false');
            draggedItem.style.cursor = 'default';
            score += 10;
            scoreDisplay.innerText = score;
            sndCorrect.currentTime = 0;
            sndCorrect.play();
        }} else {{
            score -= 5;
            scoreDisplay.innerText = score;
            sndIncorrect.currentTime = 0;
            sndIncorrect.play();
            
            draggedItem.classList.add('shake-animation');
            setTimeout(() => {{
                draggedItem.classList.remove('shake-animation');
            }}, 500);
        }}
    }}
</script>
</body>
</html>
"""

components.html(custom_game_html, height=900, scrolling=False)