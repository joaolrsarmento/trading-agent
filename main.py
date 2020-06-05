from models.indicators.SimpleMovingAverageCrossover import SimpleMovingAverageCrossover
from tools.BacktestTool import BacktestTool

model = SimpleMovingAverageCrossover()
backtest = BacktestTool(initial_date="2020-01-01", final_date="2020-06-01")
model.run_tool(backtest)
