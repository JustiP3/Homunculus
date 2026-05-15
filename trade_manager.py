import db

def enter_trade(symbol, option_type, strike_price, expiration_date, quantity, entry_price):
    position_id = db.create_position(
        symbol=symbol,
        option_type=option_type,
        strike_price=strike_price,
        expiration_date=expiration_date,
        quantity=quantity,
        entry_price=entry_price,
        current_price=entry_price
    )
    return position_id