import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Accounting Bucket List", layout="wide")
st.title("Accounting Bucket List")

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
    cards_html += f'<div class="card" draggable="true" data-target="{card["target"]}" id="card{i}">{card["text"]}</div>\n'

custom_game_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    body, html {{ 
        margin: 0; 
        padding: 0; 
        height: 100%; 
        font-family: sans-serif; 
        overflow: hidden; 
    }}
    
    #main-container {{
        height: 100vh;
        overflow-y: auto;
        padding: 10px;
        box-sizing: border-box;
    }}

    #score-board {{ 
        font-size: 24px; 
        font-weight: bold; 
        margin-bottom: 20px; 
        text-align: center;
    }}

    .layout-container {{
        display: flex;
        flex-direction: row;
        gap: 20px;
        align-items: flex-start;
        width: 100%;
    }}
    
    #game-board {{ 
        flex: 2;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }}
    
    .section {{
        border: 2px solid #aaa;
        border-radius: 8px;
        padding: 10px;
    }}
    
    .section-header {{
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .bucket-grid {{
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); 
        gap: 10px; 
    }}

    /* Color Coding */
    .assets {{ background-color: #e3f2fd; border-color: #90caf9; }}
    .liabilities {{ background-color: #ffebee; border-color: #ef9a9a; }}
    .equity {{ background-color: #f3e5f5; border-color: #ce93d8; }}
    .revenue {{ background-color: #fff3e0; border-color: #ffcc80; }}
    .expenses {{ background-color: #e8f5e9; border-color: #a5d6a7; }}
    .net-income {{ background-color: #fffde7; border-color: #fff59d; }}
    
    .bucket {{
        border: 2px dashed #777;
        border-radius: 5px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        background-color: rgba(255, 255, 255, 0.6);
        transition: background-color 0.3s;
        min-height: 110px;
        padding: 10px;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }}
    .bucket.drag-over {{ background-color: rgba(255, 255, 255, 1); border-color: #000; border-style: solid; }}
    
    #card-pool {{ 
        flex: 1;
        display: flex; 
        flex-wrap: wrap; 
        gap: 10px; 
        justify-content: center; 
        border: 2px solid #ddd; 
        padding: 15px; 
        border-radius: 10px; 
        background-color: #fafafa;
        position: sticky;
        top: 0;
        max-height: 90vh;
        overflow-y: auto;
    }}
    
    .card {{
        padding: 8px;
        background-color: #fff;
        border: 1px solid #333;
        border-radius: 3px;
        cursor: grab;
        width: 100%;
        max-width: 200px;
        font-size: 11px;
        text-align: center;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }}
    .card:active {{ cursor: grabbing; }}
    
    .bucket .card {{
        width: 90%;
        font-size: 10px;
        padding: 4px;
        cursor: default;
        margin-top: 5px;
    }}

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
    <div id="score-board">Score: <span id="score">0</span></div>

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
    let score = 0;
    const cards = document.querySelectorAll('.card');
    const buckets = document.querySelectorAll('.bucket');
    const scoreDisplay = document.getElementById('score');
    const container = document.getElementById('main-container');
    
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

    // Auto-scroll logic when dragging near top or bottom of the container
    document.addEventListener('drag', function(e) {{
        if (e.clientY === 0) return; // Prevent jump to top on drop
        const buffer = 80;
        const speed = 15;
        
        if (e.clientY < buffer) {{
            container.scrollBy(0, -speed);
        }} else if (window.innerHeight - e.clientY < buffer) {{
            container.scrollBy(0, speed);
        }}
    }});

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

    function dragDrop() {{
        this.classList.remove('drag-over');
        
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

# Render the component, configuring height to fit window viewport
components.html(custom_game_html, height=800, scrolling=False)