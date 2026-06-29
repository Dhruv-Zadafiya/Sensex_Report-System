from data.db import save_stock_data

result = save_stock_data(
    open_price=77160.67,
    close_price=77904.07,
    date_str="2026-06-22"
)

print("Inserted ID:", result)