import db

def enter_trade(
    symbol,
    option_type,
    strike_price,
    expiration_date,
    quantity,
    entry_price,

    # Optional metadata
    option_symbol=None,
    signal_id=None,

    # Trend / entry analytics
    trend_score=None,
    entry_score=None,

    entry_rsi=None,
    entry_atr=None,

    relative_volume=None,
    distance_from_ema20=None,

    # Market context
    sector=None,
    market_regime=None,
    vix_at_entry=None,

    # Risk management
    stop_loss=None,
    take_profit=None,

    # Options metadata
    dte_at_entry=None
):

    position_id = db.create_position(

        # Core position info
        symbol=symbol,
        option_symbol=option_symbol,

        signal_id=signal_id,

        option_type=option_type,
        strike_price=strike_price,
        expiration_date=expiration_date,

        quantity=quantity,

        entry_price=entry_price,
        current_price=entry_price,

        # Risk management
        stop_loss=stop_loss,
        take_profit=take_profit,

        # Trend / entry analytics
        trend_score=trend_score,
        entry_score=entry_score,

        entry_rsi=entry_rsi,
        entry_atr=entry_atr,

        relative_volume=relative_volume,
        distance_from_ema20=distance_from_ema20,

        # Market context
        sector=sector,
        market_regime=market_regime,
        vix_at_entry=vix_at_entry,

        # Options metadata
        dte_at_entry=dte_at_entry
    )

    event_value = entry_price * quantity
    event_id = db.create_position_event(
        position_id=position_id,
        event_type="ENTRY",
        event_value=event_value,
        quantity=quantity,
        price=entry_price,
        message=f"Entered trade at {entry_price}"
    )

    return position_id

def exit_trade(position_id, exit_price):
    db.update_position_price(position_id, exit_price)
    db.update_position_status(position_id, "CLOSED")

    quantity = db.get_position(position_id)["quantity"]
    event_value = exit_price * quantity
    event_id = db.create_position_event(
        position_id=position_id,
        event_type="EXIT",
        event_value=event_value,
        quantity=quantity,
        price=exit_price,
        message=f"Exited trade at {exit_price}"
    )

def update_position(position_id, current_price, quantity=None):
    #quantity is quanitiy sold
    starting_quantity = db.get_position(position_id)["quantity"]
    event_value = current_price * starting_quantity

    if quantity is not None:
        new_quantity = max(starting_quantity - quantity, 0)
        quantity_sold = starting_quantity - new_quantity
        if new_quantity == 0:
            status = "CLOSED"
            db.create_position_event(position_id=position_id, event_type="EXIT", event_value=event_value, quantity=quantity_sold, price=current_price, message=f"Exited trade at {current_price}")
        else:
            status = "PARTIAL"
            event_value = quantity_sold * current_price
            db.create_position_event(position_id=position_id, event_type="PARTIAL EXIT", event_value=event_value, quantity=quantity_sold, price=current_price, message=f"Partial exited trade at {current_price}")
        
        db.update_position_quantity(position_id, new_quantity, status)
        db.update_position_price(position_id, current_price)
        
    else:
        # If quantity is None, we assume it's just a price update without a trade event
        db.update_position_price(position_id, current_price)

def get_all_positions():
    return db.get_open_positions()