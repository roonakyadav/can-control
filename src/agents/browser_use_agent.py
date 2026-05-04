from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import Browser, BrowserConfig
from src.config import (
    logger,
    OPEN_ROUTER_API_KEY,
    MODEL_NAME,
    OPEN_ROUTER_BASE_URL,
    HEADLESS
)

class BrowserAgent:
    def __init__(self, task, on_step_callback=None):
        self.task = task
        self.on_step_callback = on_step_callback
        
        # Initialize LLM
        if not OPEN_ROUTER_API_KEY:
            raise ValueError("OPEN_ROUTER_API_KEY is missing. Please check your .env file.")
            
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            api_key=OPEN_ROUTER_API_KEY,
            base_url=OPEN_ROUTER_BASE_URL,
        )
        
        # Browser configuration
        # NOTE: Headless mode can be inconsistent depending on the website's bot detection.
        self.browser_config = BrowserConfig(headless=HEADLESS)
        self.browser = Browser(config=self.browser_config)

    async def run(self, max_steps=15):
        logger.info(f"Starting browser agent with task: {self.task}")
        
        try:
            agent = Agent(
                task=self.task,
                llm=self.llm,
                browser=self.browser,
                register_new_step_callback=self.on_step_callback,
            )
            
            history = await agent.run(max_steps=max_steps)
            result = history.final_result()
            
            if not result:
                return "Agent completed but no specific result was extracted."
            return result
            
        except Exception as e:
            logger.error(f"Error during agent execution: {str(e)}")
            raise
        finally:
            await self.browser.close()
