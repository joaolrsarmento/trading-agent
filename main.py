from models.indicators.SimpleMovingAverageCrossover import SimpleMovingAverageCrossover
from tools.BacktestTool import BacktestTool

model = SimpleMovingAverageCrossover()
backtest = BacktestTool()
model.run_tool(backtest)
