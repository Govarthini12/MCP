import asyncio
import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

# Optional: Uncomment to enable detailed debug logs
logging.basicConfig(level=logging.DEBUG)

async def run_memory_chat():
    """Run a chat using MCPAgent with built-in memory."""
    load_dotenv()
    
    # Ensure the environment variable is loaded from the .env file
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        logging.error("GROQ_API_KEY is not set in environment variables!")
        return

    os.environ["GROQ_API_KEY"] = groq_api_key

    config_file = "browser_mcp.json"
    print("Initializing chat...")

    try:
        # Create the MCP client
        client = MCPClient.from_config_file(config_file)

        # Initialize the LLM
        llm = ChatGroq(model_name="qwen-qwq-32b")  # Confirm the model name is correct

        # Initialize the agent
        agent = MCPAgent(
            client=client,
            llm=llm,
            max_steps=15,
            memory_enabled=True,
        )

        print("\n====== Interactive MCP Chat =================")
        print("Type 'clear' to clear memory.")
        print("Type 'exit' to end the chat.\n")

        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting chat...")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_memory()
                print("Memory cleared.")
                continue

            print("\nAssistant: ", end="", flush=True)

            try:
                # Await the agent response
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\n❌ Error: {e}")
                if hasattr(e, "failed_generation"):
                    print("🔍 Failed Generation Details:")
                    print(e.failed_generation)

    except Exception as e:
        logging.error(f"Failed to initialize the chat or client: {e}")
    finally:
        # Ensure that sessions are closed gracefully
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())



# import asyncio

# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from mcp_use import MCPAgent, MCPClient
# import os

# async def run_memory_chat():
#     """Run a chat with using MCPAgent's built in conversation memory."""
#     load_dotenv()
#     os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    

#     config_file = "browser_mcp.json"

#     print("Initializing chat..")
    
#     # Create the MCP client
#     client = MCPClient.from_config_file(config_file)
#     llm = ChatGroq(model_name="llama-3.3-70b-versatile")
    
#     # Initialize the agent
#     agent = MCPAgent(
#         client=client,
#         llm=llm,
#         max_steps=15,
#         memory_enabled=True,
#     )

    
#     print("\n====== Interactive MCP Chat =================")
#     print("Type 'clear' to clear the memory.")
#     print("Type 'exit' to end the chat.")

#     try:
#         while True:
#             user_input = input("You: ")
#             if user_input.lower() in ["exit", "quit"]:
#                 print("Exiting chat...")
#                 break

#             if user_input.lower() == "clear":
#                 agent.clear_conversation_memory()
#                 print("Memory cleared.")
#                 continue

            
#             print("\nAssistant: ", end="", flush=True) 

#             try:
#                 response = await agent.run(user_input)
#                 print(response)
#             except Exception as e:
#                 print(f"Error: {e}")

#     finally:
#         if client and client.sessions:
#             await client.close_all_sessions()

# if __name__ == "__main__":
#     asyncio.run(run_memory_chat())
    
    
    