from agents.BasicAgent import BasicAgent
from tools.BacktestTool import BacktestTool

agent = BasicAgent()
backtest = BacktestTool(initial_date="2020-01-01", final_date="2020-06-01")
agent.run_tool(backtest, save_log=True)
