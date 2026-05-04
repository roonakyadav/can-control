import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from src.config import logger, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, validate_config
from src.agents import BrowserAgent

# System prompt to guide the agent
SYSTEM_PROMPT = """You are a helpful browser automation agent. 
Rules:
1. Go DIRECTLY to relevant websites.
2. If you encounter a CAPTCHA, try an alternative source or website.
3. Provide a clear and concise summary of your findings.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Security: Only respond to the configured Chat ID
    if str(update.message.chat_id) != str(TELEGRAM_CHAT_ID):
        logger.warning(f"Unauthorized access attempt from Chat ID: {update.message.chat_id}")
        return

    user_task = update.message.text
    if not user_task:
        return

    await update.message.reply_text(f"🤖 Starting task: {user_task}")

    # Callback to send step-by-step updates to Telegram
    step_info = {"count": 0}
    async def on_step(state, output, error):
        step_info["count"] += 1
        goal = ""
        if output and hasattr(output, "current_state"):
            goal = output.current_state.next_goal or "Processing..."
        
        try:
            await context.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=f"⚙️ Step {step_info['count']}: {goal}"
            )
        except Exception as e:
            logger.error(f"Failed to send step update: {e}")

    try:
        # Initialize and run the agent
        agent = BrowserAgent(
            task=f"{SYSTEM_PROMPT}\n\nUser Task: {user_task}",
            on_step_callback=on_step
        )
        
        result = await agent.run(max_steps=10)
        
        await update.message.reply_text(f"✅ Task Completed!\n\n{result}")

    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    if not validate_config():
        logger.error("Invalid configuration. Please check your .env file.")
        return

    logger.info("Starting Telegram Bot...")
    
    try:
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.run_polling()
    except Exception as e:
        logger.critical(f"Bot failed to start: {e}")

if __name__ == "__main__":
    main()
