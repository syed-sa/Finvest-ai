from src.core.config import settings
import httpx
import asyncio
import re
import logging


logger: logging.Logger = logging.getLogger(__name__)

async def AgentRouter(query: str) -> str:
    """
    Routes the query to the appropriate tool using the Gemini API.
    Includes full error handling, safe response parsing, and logging.
    """
    logger.info(f"[AgentRouter] Query: {query}")

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

    headers = {
        "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
        "Content-Type": "application/json"
    }

    api_url = settings.GOOGLE_API_URL
    if not api_url.startswith("http"):
        logger.error(f"[AgentRouter] Invalid GOOGLE_API_URL: {api_url}")
        return ""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, headers=headers, json=payload)
            logger.info(f"[AgentRouter] Google API Response: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"[AgentRouter] Non-200 response: {response.text}")
                return ""

            data = response.json()
            logger.debug(f"[AgentRouter] Full Response JSON: {data}")

            # Gemini v1beta returns under "candidates"
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )

            if not text:
                logger.warning("[AgentRouter] No text found in response.")
                return ""

            logger.info("[AgentRouter] Successfully got response from Gemini.")
            return text

    except httpx.RequestError as e:
        logger.error(f"[AgentRouter] Network error: {e}")
        return ""

    except Exception as e:
        logger.exception(f"[AgentRouter] Unexpected error: {e}")
        return ""

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