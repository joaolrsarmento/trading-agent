from agents.BasicAgent import BasicAgent
from tools.BacktestTool import BacktestTool

agent = BasicAgent(balance=1000, take_profit=0.03, stop_loss=0.01)
backtest = BacktestTool(initial_date="2020-01-01", final_date="2020-06-01")
agent.run_tool(backtest, save_log=True)
agent.plot()