import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from browser_use import Agent
from browser_use.llm import ChatGroq
from browser_use.browser import BrowserProfile, BrowserSession

load_dotenv()

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY"),
)

MY_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

SYSTEM_PROMPT = """You are a helpful agent. Important rules:
- NEVER use Google to search, Google blocks you with CAPTCHA
- Go DIRECTLY to websites like cricbuzz.com, unstop.com, devfolio.co, wikipedia.org, bbc.com
- Always extract content and return a clear text summary
- If you see captcha anywhere just switch to a different source
- Never return None or empty results"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != MY_CHAT_ID:
        return

    task = update.message.text
    await update.message.reply_text(f"🤖 Starting: {task}")

    step_counter = {"count": 0}

    async def on_step(state, output, error):
        step_counter["count"] += 1
        goal = ""
        if output and hasattr(output, "current_state"):
            goal = output.current_state.next_goal or ""
        await context.bot.send_message(
            chat_id=MY_CHAT_ID,
            text=f"⚙️ Step {step_counter['count']}: {goal}"
        )

    try:
        profile = BrowserProfile(headless=True)
        session = BrowserSession(browser_profile=profile)

        agent = Agent(
            task=SYSTEM_PROMPT + "\n\nUser task: " + task,
            llm=llm,
            browser_session=session,
            register_new_step_callback=on_step,
        )

        history = await agent.run(max_steps=10)
        answer = history.final_result()

        if not answer:
            answer = "Agent completed but couldn't extract results. Try being more specific."

        await context.bot.send_message(
            chat_id=MY_CHAT_ID,
            text=f"✅ Done!\n\n{answer}"
        )

    except Exception as e:
        await context.bot.send_message(
            chat_id=MY_CHAT_ID,
            text=f"❌ Error: {str(e)}"
        )

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
