# langchain_agent_example.py

# -----------------------------
# Install required packages first (run in terminal if needed)
# pip install langchain openai
# -----------------------------

# Import necessary classes from LangChain
from langchain.agents import Tool, initialize_agent  # Tool: define callable tools; initialize_agent: create routing agent
from langchain.chat_models import ChatOpenAI        # ChatOpenAI: wrapper for OpenAI chat models (e.g., GPT-3.5)

# -----------------------------
# Mock functions for tools
# -----------------------------
def knowledge_llm(query):
    """
    Simulates a knowledge-based LLM response.
    Input: query string
    Output: formatted string pretending to be an LLM answer
    """
    return f"LLM Answer: This is a knowledge-based response to '{query}'"

def mcp_gateway(query):
    """
    Simulates an external API (MCP) response.
    Input: query string
    Output: formatted string pretending to fetch live data
    """
    return f"MCP Gateway Answer: This is API-based response for '{query}'"

# -----------------------------
# Define LangChain tools
# -----------------------------
tools = [
    Tool(
        name="Knowledge LLM",               # Tool name
        func=knowledge_llm,                 # Function to call when this tool is chosen
        description="Use this for general knowledge or explanation queries."  # Agent reads this to decide
    ),
    Tool(
        name="MCP Gateway",                 # Tool name
        func=mcp_gateway,                   # Function to call for API/live data
        description="Use this for queries that require live data, like stock prices or searches."
    )
]


llm = ChatOpenAI(
    temperature=0,          # deterministic output (no randomness)
    model_name="gpt-3.5-turbo"  # model used to decide which tool to call
)


agent = initialize_agent(
    tools,                  # list of tools the agent can call
    llm,                    # LLM that routes queries
    agent="zero-shot-react-description"  # zero-shot agent reads tool descriptions and chooses dynamically
)

queries = [
    "Explain reinforcement learning",  # general knowledge query → should use Knowledge LLM
    "Get the current price of AAPL stock"  # live/API data query → should use MCP Gateway
]

# Run queries through the agent
for q in queries:
    response = agent.run(q)             # Agent decides which tool to call and returns the tool's output
    print(f"Query: {q}")                # Print original query
    print(f"Response: {response}\n")    # Print agent's response, \n adds a blank line for readability
