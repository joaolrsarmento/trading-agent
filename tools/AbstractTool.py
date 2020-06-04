class AbstractTool(object):
    """
    This is a abstract class to represent a tool.

    """
    def __init__(self, tool_name=None):
        """
        Class constructor

        @param tool_name: tool name for debugging purposes
        @@type tool_name: string
        """
        self.tool_name = tool_name

    def execute(self, agent):
        """
        Executes the main method of the tool.

        @param agent: the agent the method should be executed on.
        @@type agent: class Agent
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes.")

    