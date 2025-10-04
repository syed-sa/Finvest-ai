from src.core.config import settings
import httpx
import asyncio
import re



async def AgentRouter(query: str) -> str:
    prompt = f"""
You are an intelligent agent with the following tools:
1. KnowledgeTool — use for general knowledge or explanations.
2. MCPTool — use for live stock or market data.

Rules:
- You MUST respond ONLY in the exact format below.
- Do not include explanations, reasoning, or markdown.
- Do not output anything outside the format.
- Do not change field names.

REQUIRED RESPONSE FORMAT:
User Query: "<original user query>"
Action: <KnowledgeTool | MCPTool>
Action Input: "<the specific input or query sent to the tool>"
Response: "<your answer or explanation based on the chosen tool>"

Now process the following query:

User Query: {query}
"""

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {"X-Goog-Api-Key": settings.GOOGLE_API_KEY, "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(settings.GOOGLE_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Extract the model's text output
        try:
            return data["results"][0]["content"][0]["text"]
        except (KeyError, IndexError):
            return None
        

def handleLLMResponseText(data: str) -> str:
    """
    Extracts the value of 'Action' from the LLM response text.
    
    Example input:
    "User Query: What is Stock price of TCS
     Action: MCPTool
     Action Input: TCS
     Response: I am sorry ..."
     
    Returns: "MCPTool"
    """
    match = re.search(r"Action:\s*(\w+)", data)
    if match:
        return match.group(1).strip()
    return ""