class Trade:
    def __init__(self,trade_id,symbol,quantity,price):
        self.trade_id = trade_id
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
    
    def __str__(self):
        return f"Trade {self.trade_id} : {self.quantity} x {self.symbol} @ ${self.price:.2f}"
    def total_value(self):
        total = self.quantity * self.price
        return round(total,2)
    
    def calculate_del(self):
        discount = 0
        total = self.total_value()
        if self.price > 100:
            discount =  round(total * 0.10,2)
        
        final_price = total - discount
        return discount,final_price
        

        
    

trades = [
    Trade("T001", "AAPL", 10, 154.54),
    Trade("T002", "TSLA", 15, 123.65),
    Trade("T003", "GOOG", 5, 420.45),
    Trade("T004", "MSFT", 12, 223.25),
    Trade("T005", "AMZN", 15, 23.15), # Changed to AMZN
    Trade("T006", "NFLX", 8, 42.65)   # Changed to NFLX
]
for trade in trades:
    disc,final = trade.calculate_del()
    print(trade)
    print(f"Selected stock is {trade.symbol}, stock value is {trade.price}$ and selected quantity is {trade.quantity}")
    print(f"Total:{trade.total_value()}$ for your stock {trade.symbol}")
    print(f"Discount for this {trade.symbol} is {disc}$")
    print(f"Final price is {final}$\n")

larger_trades = [ trade for trade in trades if trade.total_value() > 1000]
for trade in larger_trades:
    print(trade)


