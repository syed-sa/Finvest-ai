import string
from src.core.config import settings
from mcp.client.sse import sse_client
from mcp import ClientSession
import httpx
import asyncio
import re
import logging

logger: logging.Logger = logging.getLogger(__name__)


async def mcp_gateway(messsage:string,session_id:int) -> str:

    gateway_url = "http://localhost:8080/sse"
    async with sse_client(gateway_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            print("Available tools through gateway:")
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")

            tool_name = "search"
            args = {"query": "What is stocks?", "max_results": 5}

            print(f"\nCalling tool '{tool_name}' with arguments {args}...")
            result = await session.call_tool(tool_name, args)

            for content in result.content:
                if getattr(content, "type", None) == "text":
                    print(content.text)
                    break


async def cloud_llm(messsage:string,session_id:int) -> str:

    """
    Routes the query to the appropriate tool using the Gemini API.
    Includes full error handling, safe response parsing, and logging.
    """
 
 #need to add prompt or COT later for better response

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": messsage}]
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


    return "The cloud response has been choosed"