import MetaTrader5 as mt5
from dotenv import load_dotenv

load_dotenv()

FILLING_MODES = {
    mt5.ORDER_FILLING_IOC: "IOC",
    mt5.ORDER_FILLING_FOK: "FOK",
    mt5.ORDER_FILLING_RETURN: "RETURN"
}

def get_pip_value(symbol):
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"❌ Symbol info not found: {symbol}")
    pip_size = 0.01 if symbol.endswith("JPY") else 0.0001
    return pip_size * info.trade_contract_size

def price_to_pips(symbol, price_diff):
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"❌ Symbol info not found: {symbol}")
    return abs(price_diff) / info.point

def calculate_R_value(entry, sl, tp):
    risk = abs(entry - sl)
    reward = abs(tp - entry)
    if risk == 0:
        raise ValueError("SL and entry price cannot be the same.")
    return reward / risk

def calculate_lot_size(symbol, sl_price, entry_price, risk_percent, balance):
    sl_pips = price_to_pips(symbol, entry_price - sl_price)
    if sl_pips == 0:
        raise ValueError("SL in pips cannot be zero.")
    pip_value = get_pip_value(symbol)
    risk_amount = (risk_percent / 100) * balance
    lot_size = risk_amount / (sl_pips * pip_value)
    return max(round(lot_size, 2), 0.01)

def execute_trade(trade):

    symbol = trade["symbol"]
    direction = trade["direction"]
    sl = trade["sl"]
    tp = trade["tp"]
    risk_percent = trade["risk_percent"]

    if not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"❌ Could not select symbol {symbol}")

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"❌ No tick data for {symbol}")

    is_buy = direction.upper() == "BUY"
    current_price = tick.ask if is_buy else tick.bid
    entry_price = current_price

    spread = tick.ask - tick.bid
    pip_value = get_pip_value(symbol)
    spread_pips = price_to_pips(symbol, spread)
    spread_per_lot = spread_pips * pip_value

    account_info = mt5.account_info()
    if account_info is None:
        raise RuntimeError("❌ Could not fetch account info.")

    balance = account_info.balance
    lot_size = calculate_lot_size(symbol, sl, entry_price, risk_percent, balance)

    execute_market_order(symbol, entry_price, sl, tp, is_buy, lot_size)

def execute_market_order(symbol, entry_price, sl, tp, is_buy, lot_size):
    direction = "BUY" if is_buy else "SELL"
    for mode, mode_name in FILLING_MODES.items():
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": mt5.ORDER_TYPE_BUY if is_buy else mt5.ORDER_TYPE_SELL,
            "price": entry_price,
            "sl": sl,
            "tp": tp,
            "deviation": 0,
            "comment": "FXConsoleTrigger",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mode,
        }

        result = mt5.order_send(request)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            r_value = calculate_R_value(entry_price, sl, tp)
            print(f"\n✅✅✅ Trade executed successfully! ✅✅✅")
            print(f"🔹 Symbol        : {symbol}")
            print(f"🔹 Direction     : {direction}")
            print(f"🔹 Entry Price   : {entry_price}")
            print(f"🔹 Stop Loss     : {sl}")
            print(f"🔹 Take Profit   : {tp}")
            print(f"🔹 Lot Size      : {lot_size}")
            print(f"🔹 R-Value       : {r_value:.2f}")
            return
    print("❌ All filling modes failed. Trade not executed.")
