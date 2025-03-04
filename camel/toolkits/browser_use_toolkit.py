import json
import os
import logging
import requests
import time
from dotenv import load_dotenv

load_dotenv()

from camel.toolkits import FunctionTool
from camel.toolkits.base import BaseToolkit

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Keep BrowserUseAPI class unchanged as per instructions
class BrowserUseAPI:
    def __init__(self, url):
        self.url = url

    def submit_task(self, browser_use_objective):
        """Submit a task and get a task_id."""
        try:
            logger.info(f"{self.url}/submit")
            response = requests.post(
                f"{self.url}/submit",
                json={"browser_use_objective": browser_use_objective}
            )
            if response.status_code == 202:
                return response.json().get("task_id")
            else:
                logger.error(f"Request failed with status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            return None

    def query_task_status(self, task_id):
        """Query the status of a task using task_id."""
        try:
            logger.info(f"{self.url}/query/{task_id}")
            response = requests.get(f"{self.url}/query/{task_id}")
            if response.status_code == 200:
                return {"status": "completed", "message": "completed", "data": response.json()}
            elif response.status_code == 202:
                return {"status": "processing", "message": "processing"}
            else:
                logger.error(f"Request failed with status code: {response.status_code}")
                return {"status": "error", "message": f"Unexpected status code: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

# Define the BrowserUseToolkit for CAMEL AI
class BrowserUseToolkit(BaseToolkit):
    r"""A toolkit for executing browser automation tasks via an external API.

    This toolkit provides a tool to perform automation tasks in a web browser based on specified objectives.
    The API URL for the browser automation service must be set in the environment variable `BROWSER_USE_API_URL`.

    Args:
        None: This toolkit does not require any parameters for __init__().
    """
    def __init__(self):
        """Initialize the BrowserUseToolkit with the API URL from environment variables."""
        super().__init__()
        self.browser_use_api = BrowserUseAPI(url=os.environ["BROWSER_USE_API_URL"])

    def execute_browser_task(self, browser_use_objective: str) -> str:
        """Execute a browser automation task.

        Args:
            browser_use_objective (str): The objective description for the browser automation task,
                typically a detailed list of steps (e.g., numbered list: 1, 2, 3, ...) for web automation.

        Returns:
            str: A JSON string containing the task status, result, and message.
                Example on success: '{"status": "success", "result": {...}, "message": "Task completed"}'
                Example on error: '{"status": "error", "message": "Task timed out"}'
        """
        try:
            # Submit the task to the API
            task_id = self.browser_use_api.submit_task(browser_use_objective)
            if not task_id:
                return json.dumps({"status": "error", "message": "Failed to submit task"})

            # Polling loop to check task status
            start_time = time.time()
            timeout = 300  # 5 minutes
            check_interval = 2  # 2 seconds
            while time.time() - start_time < timeout:
                status = self.browser_use_api.query_task_status(task_id)
                if status.get("status") == "completed":
                    logger.info(status.get("results"))
                    return json.dumps({
                        "status": "success",
                        "result": status.get("results"),
                        "message": status.get("message", "Task completed")
                    })
                elif status.get("status") == "processing":
                    time.sleep(check_interval)
                else:
                    return json.dumps({
                        "status": "error",
                        "message": status.get("message", "Unknown status")
                    })
            return json.dumps({"status": "error", "message": "Task timed out"})
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return json.dumps({"status": "error", "message": f"An error occurred: {str(e)}"})

    def get_tools(self) -> list[FunctionTool]:
        """Return a list of tools provided by this toolkit.

        Returns:
            list[FunctionTool]: A list containing the execute_browser_task function as a FunctionTool.
        """
        return [FunctionTool(self.execute_browser_task)]
