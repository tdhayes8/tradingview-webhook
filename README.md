# TradingView to IBKR Webhook Signal Automation

Receive TradingView webhook alerts and place real-time trades via Interactive Brokers using `ib_insync`.

---

## Requirements

- Python 3.8+
- [IB Gateway or TWS](https://www.interactivebrokers.com/en/trading/ib-gateway.php) running locally
- IB API port (default paper: `7497`). Do not switch to live trading (default port 7496) until you've thoroughly tested your setup!
- TradingView account (to send alerts)
- ngrok (or Cloudflare tunnel with a custom subdomain) for public webhook access

Install dependencies:

```bash
pip install flask ib_insync gunicorn
```

## Run the Webhook Server

With Gunicorn (Production ready features like worker processes)
```bash
gunicorn -w 2 -b 0.0.0.0:5002 webhook_ibkr:app       //user might need to precede this command with "python3 -m"
```
-w 2: number of worker processes

-b: bind address and port

webhook_ibkr:app: Flask app object

This starts your Flask app via Gunicorn on port 5002.


## Expose to the Internet

Ngrok (Simple, low latency Tunnel)
```bash
ngrok http 5002
```
Use the HTTPS URL (e.g., https://abc123.ngrok.io/webhook) in TradingView.


## TradingView Setup (in a custom alert attached to a strategy)

Webhook URL (in custom alert settings):
https://your-ngrok-url/webhook

Message Body:
{
  "signal": "{{strategy.order.action}}"
}


## Security Notes

Your script can place live market orders. Use paper trading for testing first!
Protect your webhook URL — do not expose it publicly or in unsecured environments. If infiltrated, hackers could send fake signals that place unwanted orders.


## Testing

Test Locally (using a third terminal)

curl -X POST http://localhost:5002/webhook -H "Content-Type: application/json" -d '{"signal": "buy"}'


To Test in Tradingview: I recommended making a strategy that will execute very often like one that buys and sells red or green candles.
