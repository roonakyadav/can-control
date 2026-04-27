import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
)

task = """
You are a hackathon finder agent. Find free hackathons, not coding contests for a student in Bangalore. Im talking about hackathons where we build with AI and has no registration fee.

Search these websites one by one:
1. https://devfolio.co/hackathons
2. https://unstop.com/hackathons
3. https://hackerearth.com/challenges/hackathon
4. https://dare2compete.com/hackathons

Criteria - include hackathon if ANY match:
- Located in Bangalore/Bengaluru
- Fully online or has online round
- Organized by IIT, NIT, IIIT, Scaler, Polaris, Newton School of Technology, or big tech companies

Exclude any hackathon with entry fee.

For each hackathon extract:
- Name
- Date
- Location
- Organizer
- FULL registration URL (always prefix with the website domain)
- Prize money

After visiting ALL 4 websites, return the complete results as plain text.
"""

async def main():
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=False,
    )
    result = await agent.run()

    # Save to file
    with open("hackathons.txt", "w") as f:
        f.write(result.final_result())
    
    print("\n✅ Saved to hackathons.txt")

asyncio.run(main())
