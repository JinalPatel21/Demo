import yfinance as yf
import json

ticker_symbol = "ICICIBANK.NS"

ticker = yf.Ticker(ticker_symbol)

summary = ticker.info
print(f"Summary: {json.dumps(summary, indent=4)}")