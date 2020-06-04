from models.indicators.SimpleMovingAverageCrossover import SimpleMovingAverageCrossover
from tools.BacktestTool import BacktestTool

model = SimpleMovingAverageCrossover()
backtest = BacktestTool()
data = backtest.get_data()
model.run_tool(backtest)
