import MetaTrader5 as mt5
import time
import os
from dotenv import load_dotenv

load_dotenv()

MT5_LOGIN = int(os.getenv("MT5_LOGIN"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD")
MT5_SERVER = os.getenv("MT5_SERVER")

def mt5_init():
    print("🚀 Initializing MetaTrader 5...")
    start_time = time.time()

    if not mt5.initialize():
        raise RuntimeError(f"❌ MT5 initialization failed: {mt5.last_error()}")

    if not mt5.login(MT5_LOGIN, MT5_PASSWORD, MT5_SERVER):
        raise RuntimeError(f"❌ Login failed: {mt5.last_error()}")

    elapsed = time.time() - start_time
    print(f"✅ MT5 connected and logged in! Initialization took {elapsed:.2f} seconds.")

# For standalone use - If testing initialization
if __name__ == "__main__":
    mt5_init()
