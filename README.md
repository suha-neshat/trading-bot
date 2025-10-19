# Automated Trading Bot (AWS Lambda + Alpaca Paper) — with DRY_RUN

SMA crossover bot that can run:
- **DRY_RUN** (no API keys, simulated orders)
- **Alpaca Paper** (real API, paper money)
- On **AWS Lambda** (scheduled) or **locally**

## Quick start (local backtest)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export SYMBOLS="AAPL,MSFT"
python backtests/backtest_sma.py
```

## No-API Live Demo (DRY_RUN)
See it run live without any broker:
```bash
# macOS/Linux
export DRY_RUN=true
python run_live_dryrun.py
```
```powershell
# Windows PowerShell
$env:DRY_RUN='true'
python run_live_dryrun.py
```
```cmd
:: Windows Command Prompt
set DRY_RUN=true
python run_live_dryrun.py
```

## Alpaca Paper (optional)
Create a .env or set env vars:
```
ALPACA_BASE_URL=https://paper-api.alpaca.markets
ALPACA_KEY_ID=YOUR_KEY
ALPACA_SECRET_KEY=YOUR_SECRET
SYMBOLS=AAPL,MSFT
TIMEFRAME=1h
FAST_WINDOW=20
SLOW_WINDOW=50
MAX_NOTIONAL_PER_SYMBOL=500
MAX_POSITION_USD=1000
STOP_LOSS_PCT=0.03
TAKE_PROFIT_PCT=0.06
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

## Deploy to AWS (SAM)
```bash
sam build --use-container
sam deploy --guided
```
