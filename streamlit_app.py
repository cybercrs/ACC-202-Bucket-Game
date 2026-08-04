import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Accounting Bucket List", layout="wide")
st.title("Accounting Bucket List")

custom_game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; }
    
    #game-board { 
        display: grid; 
        grid-template-columns: repeat(6, 1fr); 
        gap: 10px; 
        width: 100%; 
        margin-bottom: 30px; 
    }
    
    .category-header {
        grid-column: span 6;
        background-color: #eee;
        padding: 5px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    
    .bucket {
        border: 2px dashed #ccc;
        border-radius: 5px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        background-color: #f9f9f9;
        transition: background-color 0.3s;
        min-height: 100px;
        padding: 10px;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    .bucket.drag-over { background-color: #e0f7fa; border-color: #00bcd4; }
    
    #card-pool { 
        display: flex; 
        flex-wrap: wrap; 
        gap: 10px; 
        justify-content: center; 
        width: 95%; 
        border: 2px solid #ddd; 
        padding: 20px; 
        border-radius: 10px; 
        min-height: 150px;
        background-color: #fafafa;
    }
    
    .card {
        padding: 8px;
        background-color: #fff;
        border: 1px solid #333;
        border-radius: 3px;
        cursor: grab;
        width: 180px;
        font-size: 11px;
        text-align: center;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        margin-bottom: 5px;
    }
    .card:active { cursor: grabbing; }
    
    .bucket .card {
        width: 90%;
        font-size: 10px;
        padding: 4px;
        cursor: default;
    }

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

<div id="game-board">
    <div class="category-header">ASSETS</div>
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

    <div class="category-header">LIABILITIES</div>
    <div class="bucket" data-type="Accounts Payable">Accounts Payable</div>
    <div class="bucket" data-type="Wages Payable">Wages Payable</div>
    <div class="bucket" data-type="Unearned Revenue">Unearned Revenue</div>
    <div class="bucket" data-type="Notes Payable due > 12 mos.">Notes Payable due > 12 mos.</div>
    <div class="bucket" data-type="Mortgage Payable">Mortgage Payable</div>
    <div class="bucket" data-type="Bonds Payable">Bonds Payable</div>

    <div class="category-header">STOCKHOLDER'S EQUITY</div>
    <div class="bucket" data-type="Retained Earnings">Retained Earnings</div>
    <div class="bucket" data-type="Common Stock">Common Stock</div>

    <div class="category-header">REVENUE</div>
    <div class="bucket" data-type="Service Revenue">Service Revenue</div>
    <div class="bucket" data-type="Sales Revenue">Sales Revenue</div>
    <div class="bucket" data-type="Interest Income">Interest Income</div>

    <div class="category-header">EXPENSES</div>
    <div class="bucket" data-type="Cost of Goods Sold">Cost of Goods Sold</div>
    <div class="bucket" data-type="Supplies Expense">Supplies Expense</div>
    <div class="bucket" data-type="Rent Expense">Rent Expense</div>
    <div class="bucket" data-type="Salaries & Wages Expense">Salaries & Wages Expense</div>
    <div class="bucket" data-type="Advertising Expense">Advertising Expense</div>
    <div class="bucket" data-type="Insurance Expense">Insurance Expense</div>
    <div class="bucket" data-type="Interest Expense">Interest Expense</div>
    <div class="bucket" data-type="Income Tax Expense">Income Tax Expense</div>

    <div class="category-header">NET INCOME (LOSS)</div>
    <div class="bucket" data-type="NET INCOME (LOSS)">NET INCOME (LOSS)</div>
</div>

<div id="card-pool">
    <div class="card" draggable="true" data-target="CASH Account">Currency on hand, coin, and balance in bank checking & savings accounts (money owned)</div>
    <div class="card" draggable="true" data-target="Sales Revenue">Amounts earned by a company from selling physical products (goods) to customers</div>
    <div class="card" draggable="true" data-target="Accounts Payable">Amounts owed to vendors (suppliers) for purchases made on account & not yet paid</div>
    <div class="card" draggable="true" data-target="Service Revenue">Amounts earned by a company from selling & performing services for customers</div>
    <div class="card" draggable="true" data-target="Equipment">Machinery, computers, tools, & vehicles owned by a company & used in operations</div>
    <div class="card" draggable="true" data-target="Retained Earnings">Cumulative sum of past profits earned over time, not distributed (paid) as dividends to shareholders</div>
    <div class="card" draggable="true" data-target="Inventory">Products (goods) a company owns and is being held for the purpose of resale to customers</div>
    <div class="card" draggable="true" data-target="Accounts Receivable">Amounts customers owe the company for products or services sold on credit (Due from customers)</div>
    <div class="card" draggable="true" data-target="Utilities Expense">Cost incurred for use of electricity, Internet, water & sewage necessary to operate the business</div>
    <div class="card" draggable="true" data-target="Land & Buildings">Land & physical stores used in a retailer's operations</div>
    <div class="card" draggable="true" data-target="Intangible Assets">Patents, Trademarks, & Copyrights</div>
    <div class="card" draggable="true" data-target="Land Investments">Land owned but not used in operations; being held for future use or capital appreciation, e.g., will build a store in 3 yrs.</div>
    <div class="card" draggable="true" data-target="Unearned Revenue">Amounts received in advance from customers before goods or services have been delivered or performed</div>
    <div class="card" draggable="true" data-target="Cost of Goods Sold">Cost of inventory that was sold to customers; cost that was paid to suppliers for items sold</div>
    <div class="card" draggable="true" data-target="Interest Expense">Cost incurred for borrowing money from creditors arising from loans, mortgages, bonds.</div>
    <div class="card" draggable="true" data-target="Common Stock">Total amount paid-in (invested) in the corp. by stockholders (investors) in exchange for shares of ownership</div>
    <div class="card" draggable="true" data-target="Supplies">Goods owned & on-hand for future that will be used/consumed in operations (not for resale)</div>
    <div class="card" draggable="true" data-target="Supplies Expense">Office supplies & cleaning supplies that have been consumed/used in operations</div>
    <div class="card" draggable="true" data-target="NET INCOME (LOSS)">Total Revenue less Total Expenses for an accounting period</div>
    <div class="card" draggable="true" data-target="Stock Investments">Amount a company invests in another corporation by buying their stock with plans to hold it for the long-term</div>
    <div class="card" draggable="true" data-target="Cost of Goods Sold">Cost of products sold; EX: cost Walmart incurred to buy the sold merchandise from suppliers</div>
    <div class="card" draggable="true" data-target="Mortgage Payable">Amount due on a 20-year mortgage to finance purchase of a building</div>
    <div class="card" draggable="true" data-target="Advertising Expense">Cost incurred for services used to design marketing materials & promote the business and its products.</div>
    <div class="card" draggable="true" data-target="Prepaid">Paid rent to landlord two months in advance for future occupancy, e.g., effective next month</div>
    <div class="card" draggable="true" data-target="Wages Payable">Salary & wages owed to employees for work performed, but company has not yet paid</div>
    <div class="card" draggable="true" data-target="Salaries & Wages Expense">Cost of labor performed by employees during a period (cost of labor services used by the company)</div>
    <div class="card" draggable="true" data-target="Notes Payable due > 12 mos.">Amount due to a creditor (bank) after 12 months evidenced by a written, signed promissory note.</div>
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
            this.appendChild(draggedItem);
            draggedItem.setAttribute('draggable', 'false');
            draggedItem.style.cursor = 'default';
            score += 10;
            scoreDisplay.innerText = score;
            sndCorrect.currentTime = 0;
            sndCorrect.play();
        } else {
            score -= 5;
            scoreDisplay.innerText = score;
            sndIncorrect.currentTime = 0;
            sndIncorrect.play();
            
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

components.html(custom_game_html, height=1800, scrolling=True)