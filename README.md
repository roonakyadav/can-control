# Browser Agent MVP 🤖

A lightweight browser automation agent triggered via Telegram. Built for hackathons and rapid prototyping.

## 📝 Overview
This project allows you to control a browser agent through a Telegram bot. You send a natural language task (e.g., "Find the latest news on SpaceX"), and the agent uses a Large Language Model (LLM) to navigate the web, extract information, and report back to you.

## 🚀 Features
- **Telegram Integration**: Send tasks and receive real-time step updates directly in Telegram.
- **LLM-Powered Navigation**: Uses `browser-use` and OpenRouter (GPT-4o-mini) to handle complex web tasks.
- **Single Task CLI**: Run tasks directly from your terminal for testing.
- **Structured Logging**: All actions and errors are logged for easy debugging.

## ⚠️ Limitations & Known Issues (Honest MVP)
- **Headless Mode Inconsistency**: Some websites detect headless browsers as bots and block them with CAPTCHAs. If a task fails, try setting `HEADLESS=false` in your `.env`.
- **CAPTCHA Handling**: The agent is not designed to solve CAPTCHAs. It will attempt to find alternative sources if blocked.
- **Step Limits**: Tasks are currently capped at 10-15 steps to prevent infinite loops and excessive API costs.
- **Single User**: Currently whitelisted to a single Telegram Chat ID for security.

## 🛠️ Architecture
- **`src/main.py`**: The entry point for the Telegram bot.
- **`src/agents/`**: Contains the core `BrowserAgent` logic.
- **`src/config/`**: Centralized configuration and logging setup.
- **`run_cli.py`**: A CLI tool for testing individual tasks.

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- An OpenRouter API Key (from [openrouter.ai](https://openrouter.ai/))

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd browser-agent

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Configuration
Copy the example environment file and fill in your keys:
```bash
cp .env.example .env
```
Edit `.env` and provide:
- `OPEN_ROUTER_API_KEY`
- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID` (Use [@userinfobot](https://t.me/userinfobot) to find yours)

### 4. Running the Project

**Start the Telegram Bot:**
```bash
python3 -m src.main
```

**Run a single task via CLI:**
```bash
python3 run_cli.py "What is the current stock price of NVIDIA?"
```

## 🗺️ Future Roadmap
- [ ] Add support for multiple concurrent users.
- [ ] Implement a web dashboard for monitoring agent actions.
- [ ] Improve CAPTCHA avoidance strategies.
- [ ] Add support for local LLMs (Ollama).

---
*Built with ❤️ for the Hackathon.*
