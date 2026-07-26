import os
import json
import time
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
import re

load_dotenv()

client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

LOG_PATH="run.jsonl"

def log_step(step_type, content):
    with open(LOG_PATH,"a") as f:
        f.write(json.dumps({"timestamp": time.time(),"type": step_type,"content": content})+"\n")

async def run_agent(history):
    latestq=history[-1]["content"]
    log_step("input",latestq)

    prompt="""You are an expert Data Analyst. You are given with a data analysis task, possibly with an earlier context. Work out the correct answer based on your knowledge and reasoning.  The question will specify an exact 
        JSON shape to reply with and you MUST reply with ONLY that JSON object,and nothing else: no markdown, no explanation, no code fences."""
    system_instruction=input
    conv="\n".join(f"{m['role'].upper()} : {m['content']}" for m in history)
    full_prompt=f"{system_instruction}\n\nConversation so far:\n{conv}\n\nYour reply (JSON only):"
    completion = client.chat.completions.create(
        model="gpt-oss-120b",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Conversation so far:\n{conv}\n\nYour reply (JSON only):"}
        ]
    )
    response=completion.choices[0].message.content.strip()
    log_step("raw_llm_output",response)

    clean_json=extract_json(response)
    log_step("final_output",clean_json)
    return clean_json

def extract_json(object):
    match = re.search(r'\{.*\}',object,re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")
    obj=json.loads(match.group())
    if "log_url" not in obj:
        obj["log_url"] = "https://your-public-log-url-here/run.jsonl"
    return json.dumps(obj)
