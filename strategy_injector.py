class StrategyInjector:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.strategies = []

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def execute_strategies(self):
        results = []
        for strategy in self.strategies:
            result = strategy.execute(self.data_manager)
            if result:
                results.append(result)
        return results

