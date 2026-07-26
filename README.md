# DataBo — Data Analyst Telegram Bot

DataBo is a Telegram bot that acts as an autonomous data-analysis agent. 
When messaged a data-analysis question — whether it embeds data inline or 
references a public dataset (e.g. MOSPI) — the bot reasons through the 
problem using an LLM and replies with a single, precisely-shaped JSON object.

## How it works
1. **bot.py** — listens for incoming Telegram messages via polling, 
   maintains per-chat conversation history for multi-turn questions, 
   and forwards each query to the agent.
2. **agent.py** — the reasoning core. Sends the question (plus any 
   prior conversation context) to an LLM (Cerebras' Llama 3.3 70B), 
   extracts a clean JSON object from the model's response, and logs 
   every step of the run to `run.jsonl`.

## Tech stack
- Python 3
- `python-telegram-bot` for Telegram integration
- Cerebras Cloud SDK for LLM inference
- `python-dotenv` for environment configuration

## Setup
1. Clone this repo
2. `pip install -r requirements.txt`
3. Create a `.env` file with:
