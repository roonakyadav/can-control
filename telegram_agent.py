import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from browser_use import Agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
)

MY_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only respond to you
    if update.message.chat_id != MY_CHAT_ID:
        return

    task = update.message.text
    await update.message.reply_text(f"🤖 Got it! Working on: {task}")

    try:
        agent = Agent(
            task=task,
            llm=llm,
            use_vision=False,
        )
        result = await agent.run()
        answer = result.final_result()
        await update.message.reply_text(f"✅ Done!\n\n{answer}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running... Send a message on Telegram!")
    app.run_polling()

if __name__ == "__main__":
    main()
