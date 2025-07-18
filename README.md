<h1 align="center">FXConsoleTrigger</h1> 
<p align="center"> 
<em>A terminal-based trading assistant for MetaTrader 5</em> 
</p>
FXConsoleTrigger helps you quickly execute live market trades on your MetaTrader 5 account. Enter your symbol, direction (BUY/SELL), SL/TP, and desired risk % — and it automatically calculates the appropriate lot size and places the trade.

---

## 🚀 1. MetaTrader 5 Account Setup

To use this tool, you’ll need a MetaTrader 5 account (demo or real).

### MT5 Demo Setup (Mobile)
1. Open the MetaTrader 5 app.
2. Go to **Settings > New Account > Open a Demo Account**.
3. Choose a broker (e.g., MetaQuotes, ICMarkets).
4. Create your demo account and note:
   - **Login**
   - **Password**
   - **Server** (e.g. MetaQuotes-Demo)

> 💡 For live trading, sign up with a regulated broker like ICMarkets, OANDA, etc.

---

## ⚙️ 2. Environment Configuration (`.env`)

Create a `.env` file in the root of your project:

```env
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server (e.g., MetaQuotes-Demo)
```

> ✅ This file is ignored by Git to protect your credentials.

---

## 💡3. MetaTrader 5 64-bit Requirement

> ⚠️ **Important:** FXConsoleTrigger requires the **64-bit version of MetaTrader 5** to interface correctly with the Python API.  
> Please ensure your MT5 installation is 64-bit, or the connection will fail.  
> The 64-bit version is usually installed under `C:\Program Files\MetaTrader 5` on Windows. 

## ▶️ 4. Run the Program

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

Then, launch the application from the root directory:

```bash
python main.py
```

You'll be prompted in the terminal to enter your trade details (symbol, direction, SL, TP, and risk%), and FXConsoleTrigger will calculate the lot size and execute the trade instantly via MetaTrader 5.