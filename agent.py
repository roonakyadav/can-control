import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent
from browser_use.llm import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY"),
)


email = os.getenv("GMAIL_EMAIL")
password = os.getenv("GMAIL_PASSWORD")

task = f"""
Go to scaler.com and login with email {email} and password {password}.
After logging in, find what classes have been happened in last 5 days, summarize everything that has heppend in last 5 days like which classes in which subjects, name of classes and read their notes and give me a summary of last 5 days

Return the results as plain text.
"""

async def main():
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=False,
    )
    result = await agent.run(max_steps=15)
    answer = result.final_result()
    if answer:
        print("\n✅ Result:\n")
        print(answer)
    else:
        print("❌ Could not extract results")

asyncio.run(main())
