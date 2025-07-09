import os
import time
from dotenv import load_dotenv
from mt5_init import mt5_init
from trade_executor import execute_trade, load_settings

def prompt_risk_percent(default_percent):
    user_input = input(f"Risk % (default {default_percent}%): ").strip()
    if user_input == "":
        return default_percent
    try:
        return float(user_input)
    except ValueError:
        print("❌ Invalid number. Using default.")
        return default_percent

def prompt_float(prompt_text):
    while True:
        try:
            return float(input(prompt_text))
        except ValueError:
            print("❌ Please enter a valid number.")

def main():
    load_dotenv()
    mt5_init()

    while True:
        print("\n📥 Enter your trade details below:\n")

        symbol = input("Symbol (e.g., EURUSD): ").strip().upper()
        while not symbol.isalpha() or len(symbol) < 5:
            symbol = input("❌ Invalid symbol. Enter again (e.g., EURUSD): ").strip().upper()

        direction = input("Direction (BUY or SELL): ").strip().upper()
        while direction not in ["BUY", "SELL"]:
            direction = input("❌ Invalid direction. Enter BUY or SELL: ").strip().upper()

        sl = prompt_float("Stop Loss price: ")
        tp = prompt_float("Take Profit price: ")
        risk_percent = prompt_risk_percent(default_percent=1.0)

        trade = {
            "symbol": symbol,
            "direction": direction,
            "entry": "NOW",
            "sl": sl,
            "tp": tp,
            "risk_percent": risk_percent,
        }

        start_time = time.time()
        try:
            execute_trade(trade)
        except Exception as e:
            print(f"\n❌ Error executing trade: {e}")
        else:
            print(f"\n✅ Trade completed in {time.time() - start_time:.2f} seconds.")

        again = input("\n🔁 Would you like to place another trade? (y/n): ").strip().lower()
        if again != "y":
            print("\n👋 Exiting FXConsoleTrigger. Happy trading!")
            break

if __name__ == "__main__":
    main()
