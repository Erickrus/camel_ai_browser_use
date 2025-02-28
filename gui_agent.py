import os


from camel.agents.chat_agent import ChatAgent
from camel.messages.base import BaseMessage
from camel.models import ModelFactory
# from camel.societies.workforce import Workforce
from camel.tasks.task import Task
from camel.types import ModelPlatformType, ModelType
from camel.configs import DeepSeekConfig
from camel.toolkits import FunctionTool, SearchToolkit

# Notice:
# You may need integrate this file into the camelai's package
from camel.toolkits.browser_use_toolkit import BrowserUseToolkit

def main():
    print("camel agent with BrowserUseToolkit() ")
    toolkit = BrowserUseToolkit()
    gui_agent_model = ModelFactory.create(
        model_platform=ModelPlatformType.DEEPSEEK,
        model_type=ModelType.DEEPSEEK_CHAT,
    )

    gui_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name="You are a UI Tester",
            content="You are a UI tester, you are experienced in working with UI test."
            " You can break the goals into numbered list of action." 
            " And you know how to use BrowserUseTool and run the tool with your detailed output",
        ),
        model=gui_agent_model,
        tools=[FunctionTool(BrowserUseToolkit().execute_browser_task)],
    )
    print(gui_agent.role_name)
    print(gui_agent._original_system_message.content)
    usr_msg = """Task:
  To access http://localhost:8089; login with x_name and x_password; place an order there with brand: Brand-A, size: XXL, qty:10 . Finally logout. You need use BrowserUseTool to execute these steps and check the output from the tool.

expected_output:
  The order is placed successfully and the browser use exit
"""
    print(usr_msg)
    response = gui_agent.step(input_message=usr_msg, response_format=None)

    print(response.msgs[0].content)


if __name__ == "__main__":
    main()

