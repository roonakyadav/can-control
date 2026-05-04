import asyncio
import sys
from src.config import logger, validate_config
from src.agents import BrowserAgent

async def run_task(task_description):
    if not validate_config():
        logger.error("Invalid configuration. Please check your .env file.")
        return

    try:
        agent = BrowserAgent(task=task_description)
        result = await agent.run(max_steps=15)
        print(f"\n--- RESULT ---\n{result}\n--------------")
    except Exception as e:
        logger.error(f"Failed to execute task: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_cli.py 'your task description here'")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    asyncio.run(run_task(task))
