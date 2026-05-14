def calculate_avg_daily(total_qty):
    return total_qty / 30 if total_qty else 0


def calculate_safety_stock(avg_daily):
    return avg_daily * 2


def calculate_recommended(avg_daily, lead_time_days=3):
    safety_stock = calculate_safety_stock(avg_daily)
    return int((avg_daily * lead_time_days) + safety_stock)