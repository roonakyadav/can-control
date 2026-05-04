import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

task = """
Open me todays ongoing ipl match scorecard on cricbuzz.com or some other website.
If you see any captcha in your way then switch to another website or service.
Never try to solve captcha.
"""

async def main():
    agent = Agent(task=task, llm=llm, use_vision=False)
    result = await agent.run(max_steps=15)
    print(result.final_result())

asyncio.run(main())
