# camel_ai_browser_use

## Overview
With the rise of Large Language Models (LLMs), AI agents are transforming productivity across various fields. Typically seen as standalone tools, these agents can achieve even more when working together. This repository explores the collaboration between two distinct agents: the [CamelAI](https://github.com/camel-ai/camel/) Framework, which excels in generation and planning, and the [Browser Use](https://github.com/browser-use/browser-use), specialized in GUI-based automation tasks. By connecting their strengths, we can create a powerful synergy where one agent's capabilities complement the other's limitations. This initial trial demonstrates how heterogeneous agents can work together seamlessly, unlocking new possibilities for complex tasks that require both creativity and precision.

## 1. Browser Use Toolkit 
BrowserUseToolkit (`browser_use_toolkit.py`) is a standard CamelAI toolkit implementation. It should be installed in CamelAI agent projects. This tool receives an instruction and sends it to the browser-use agent. Since GUI automation tasks can take a fairly long time, it submits the task and performs rolling polling to check if the task has finished and produced results.

## 2. Browser Use Service
BrowserUseService (`browser_use_service.py`) is the backend component responsible for executing web automation task. The service can only work on one specific task at a time. If other tasks are submitted, they will be pending until the current task is finished. 

```mermaid
sequenceDiagram
    participant CamelAI_Agent as CamelAI Agent
    participant BrowserUseService as Browser Use Service
    participant BrowserUseAgent as Browser Use Agent

    CamelAI_Agent->>BrowserUseService: Submit Task with Instructions
    BrowserUseService-->>CamelAI_Agent: Return task_id

    BrowserUseService->>BrowserUseAgent: Submit Task for Automation
    loop Every 2 seconds
        CamelAI_Agent->>BrowserUseService: Query Status with task_id
        alt Task is not completed
            BrowserUseService-->>CamelAI_Agent: Status: In Progress
        else Task is completed
            BrowserUseAgent-->>BrowserUseService: Return Results
            BrowserUseService-->>CamelAI_Agent: Status: Completed
            BrowserUseService-->>CamelAI_Agent: Return Results
        end
    end
```

### Customization

You may need do some customization by yourself, to set up .env file, the browser configuration etc. The service default port is `4999`.

Following is an example `.env` file of `browser_use_service.py`. Place them in the same folder. 
```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
USERNAME=user
PASSWORD=password
MODEL_NAME=gpt-4o-mini
```

### BrowserUse Installation

Please refer to the [Browser Use](https://github.com/browser-use/browser-use) page.

With pip (Python>=3.11):

```bash
pip install browser-use
```

install playwright:

```bash
playwright install
```



## 3. CamelAI Agent Demo Code
The code (`gui_agent.py`) demonstrates how to use the toolkit. 
