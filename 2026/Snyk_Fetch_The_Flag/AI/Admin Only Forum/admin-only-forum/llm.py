import os
import json
import random
from typing import List, Dict, Any
from openai import OpenAI

from db import get_all_dms, make_user_admin as db_make_user_admin

MODEL = "gpt-5-nano"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=60.0)

def get_tools_spec() -> list:
    return [
        {
            "type": "function",
            "function": {
                "name": "get_direct_messages",
                "description": "Retrieve all direct messages sent to the admin.",
                "parameters": {"type": "object", "properties": {}}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "make_user_admin",
                "description": "Grant admin privileges to a user by their username.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "The username to grant admin privileges"}
                    },
                    "required": ["username"]
                }
            }
        },
    ]

def tool_get_direct_messages() -> Dict[str, Any]:
    dms = get_all_dms()
    random.shuffle(dms)
    return {"ok": True, "messages": dms}

def tool_make_user_admin(username: str) -> Dict[str, Any]:
    success = db_make_user_admin(username)
    if success:
        return {"ok": True, "username": username, "message": f"User {username} has been granted admin privileges"}
    return {"ok": False, "error": "user_not_found", "message": f"User {username} not found"}

def run_admin_assistant(messages: List[Dict[str, str]]) -> str:
    local_messages = list(messages)
    
    for _ in range(6):
        resp = client.chat.completions.create(
            model=MODEL,
            messages=local_messages,
            tools=get_tools_spec(),
            tool_choice="auto",
            verbosity="low",
            timeout=60.0,
        )
        
        msg = resp.choices[0].message
        
        if msg.tool_calls:
            assistant_dict = {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            }
            local_messages.append(assistant_dict)
            
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = {}
                if tool_call.function.arguments:
                    try:
                        args = json.loads(tool_call.function.arguments)
                    except Exception:
                        args = {}
                
                if name == "get_direct_messages":
                    result = tool_get_direct_messages()
                elif name == "make_user_admin":
                    username = args.get("username", "")
                    result = tool_make_user_admin(username)
                else:
                    result = {"error": "unknown_tool"}
                
                local_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": json.dumps(result),
                })
            continue
        
        return msg.content or ""
    
    return ""
