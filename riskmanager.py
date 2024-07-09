class RiskManager:
    def __init__(self):
        # Initialize risk parameters
        self.max_exposure = 100000  # Example: maximum dollar exposure
        self.max_drawdown = 0.1  # Example: 10% maximum drawdown
        self.current_exposure = 0
        self.peak_portfolio_value = 0
        self.current_portfolio_value = 0

    def set_max_exposure(self, exposure):
        self.max_exposure = exposure

    def set_max_drawdown(self, drawdown):
        self.max_drawdown = drawdown

    def update_portfolio_value(self, current_value):
        self.current_portfolio_value = current_value
        if current_value > self.peak_portfolio_value:
            self.peak_portfolio_value = current_value

    def check_exposure(self):
        if self.current_exposure > self.max_exposure:
            self.reduce_exposure()

    def check_drawdown(self):
        current_drawdown = (self.peak_portfolio_value - self.current_portfolio_value) / self.peak_portfolio_value
        if current_drawdown > self.max_drawdown:
            self.stop_trading()

    def reduce_exposure(self):
        # Logic to reduce exposure
        print("Reducing exposure")
        # This could involve closing positions or reducing position sizes

    def stop_trading(self):
        # Logic to stop trading
        print("Stopping trading due to excessive drawdown")

    def evaluate_risks(self):
        self.check_exposure()
        self.check_drawdown()

# Example usage
if __name__ == "__main__":
    risk_manager = RiskManager()
    risk_manager.update_portfolio_value(120000)
    risk_manager.current_exposure = 110000  # Example current exposure
    risk_manager.evaluate_risks()