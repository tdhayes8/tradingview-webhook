from flask import Flask, request, jsonify
from ib_insync import *
import threading
import asyncio

# Flask app
app = Flask(__name__)

# Define the MNQ (Micro E-mini Nasdaq) Futures Contract
def create_mnq_contract():
    return Future(symbol='MNQ', lastTradeDateOrContractMonth='', exchange='GLOBEX', currency='USD')

# Function to connect to IBKR (inside the thread)
def connect_ibkr():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)  # Paper trading port: 7497, Live: 7496
    return ib

# Place order based on signal
def place_order(signal):
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    contract = Future(symbol='MNQ', lastTradeDateOrContractMonth='202506', exchange='CME', currency='USD')
    ib.qualifyContracts(contract)

    if signal.lower() == 'buy':
        order = MarketOrder('BUY', 1)
    elif signal.lower() == 'sell':
        order = MarketOrder('SELL', 1)
    else:
        print(f"Invalid signal: {signal}")
        ib.disconnect()
        return

    trade = ib.placeOrder(contract, order)
    ib.sleep(1)  # Let IBKR process the order

    print(f"Order status: {trade.orderStatus.status}")
    ib.disconnect()

# Flask endpoint to receive TradingView webhook alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'signal' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    signal = data['signal']
    print(f"Received signal: {signal}")

    # Run IBKR order in background to not block the server
    threading.Thread(target=place_order, args=(signal,)).start()

    return jsonify({'status': f'Order for {signal} received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)