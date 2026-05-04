import subprocess
import sys
import os

print("🔧 Setting up browser-agent environment...")

# Install uv if not present
subprocess.run("curl -LsSf https://astral.sh/uv/install.sh | sh", shell=True)

# Add uv to path
os.environ["PATH"] = f"{os.path.expanduser('~')}/.local/bin:{os.environ['PATH']}"

# Create venv
subprocess.run("uv venv .venv", shell=True)

# Install packages
packages = [
    "browser-use==0.1.40",
    "langchain-groq",
    "langchain-openai",
    "langchain-core",
    "python-dotenv",
    "playwright",
]

print("📦 Installing packages...")
subprocess.run(f"uv pip install {' '.join(packages)}", shell=True)

# Install playwright browser
print("🌐 Installing Chromium...")
subprocess.run(".venv/bin/python3 -m playwright install chromium", shell=True)

# Create .env if it doesn't exist
if not os.path.exists(".env"):
    key = input("🔑 Enter your GROQ API key: ")
    with open(".env", "w") as f:
        f.write(f"GROQ_API_KEY={key}\n")
    print("✅ .env file created")
else:
    print("✅ .env already exists")

print("\n✅ Setup complete! Now run:")
print("   source .venv/bin/activate")
print("   python3 agent.py")
