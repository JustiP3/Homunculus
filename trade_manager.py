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

def exit_trade(position_id, exit_price):
    db.update_position_price(position_id, exit_price)
    db.update_position_status(position_id, "CLOSED")

def update_position(position_id, current_price, quantity=None):
    #quantity is quanitiy sold
    stating_quantity = db.get_position(position_id)["quantity"]
    
    if quantity is not None:
        new_quantity = max(stating_quantity - quantity, 0)
        if new_quantity == 0:
            status = "CLOSED"
        else:
            status = "PARTIAL"
        
        db.update_position_quantity(position_id, new_quantity, status)

    db.update_position_price(position_id, current_price)

def get_all_positions():
    return db.get_open_positions()