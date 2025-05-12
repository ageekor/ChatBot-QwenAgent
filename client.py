import pprint
import json5
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print
import os
from dotenv import load_dotenv
from tools import MyImageGen, MySQLQueryTool, RAGSearchTool

# Load environment variables from .env file
load_dotenv()

# Step 2: Configure the LLM you are using.
llm_cfg = {
    # Use the model service provided by DashScope:
    'model': 'qwen3-235b-a22b',
    'model_server': 'dashscope',
    'api_key': os.getenv('DASHSCOPE_API_KEY'),  # Get API key from environment variable
    # It will use the `DASHSCOPE_API_KEY' environment variable if 'api_key' is not set here.

    # Use a model service compatible with the OpenAI API, such as vLLM or Ollama:
    # 'model': 'Qwen2.5-7B-Instruct',
    # 'model_server': 'http://localhost:8000/v1',  # base_url, also known as api_base
    # 'api_key': 'EMPTY',

    # (Optional) LLM hyperparameters for generation:
    'generate_cfg': {
        'top_p': 0.8
    }
}

llm_cfg = {
    # Use the OpenAI-compatible model service provided by DashScope:
    'model': 'deepseek-r1',
    'model_server': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    'api_key': os.getenv('DASHSCOPE_API_KEY'),  # Get API key from environment variable

    # 'generate_cfg': {
    #     # When using Dash Scope OAI API, pass the parameter of whether to enable thinking mode in this way
    #     'extra_body': {
    #         'enable_thinking': False
    #     },
    # },
}

# Step 3: Create an agent. Here we use the `Assistant` agent as an example, which is capable of using tools and reading files.
system_instruction = '''你是智能助手小菁。'''
tools = [
    {'mcpServers': {  # You can specify the MCP configuration file
            'time': {
                'command': 'uvx',
                'args': ['mcp-server-time', '--local-timezone=Asia/Shanghai']
            }
        }
    },
    {"mcpServers": {
            "fetch": {
            "type": "sse",
            "url": "https://mcp.api-inference.modelscope.cn/sse/6b613ec734124a"
            }
        }
    },
    'my_image_gen', 
    'code_interpreter', 
    'mysql_query',
    'rag_search',
]
files = ['./examples/resource/doc.pdf']  # Give the bot a PDF file to read.
bot = Assistant(llm=llm_cfg,
                system_message=system_instruction,
                function_list=tools,
                # files=files
                )
def run_webui():
    from qwen_agent.gui import WebUI
    WebUI(bot, chatbot_config={'user.name': '', 'user.avatar': './assets/user.jpeg', 'agent.avatar': './assets/agent.jpeg'}).run()  # bot is the agent defined in the above code, we do not repeat the definition here for saving space.

def run_client():
    # Step 4: Run the agent as a chatbot.
    messages = []  # This stores the chat history.
    while True:
        # For example, enter the query "draw a dog and rotate it 90 degrees".
        query = input('\nuser query: ')
        # Append the user query to the chat history.
        messages.append({'role': 'user', 'content': query})
        response = []
        response_plain_text = ''
        print('bot response:')
        for response in bot.run(messages=messages):
            # Streaming output.
            response_plain_text = typewriter_print(response, response_plain_text)
        # Append the bot responses to the chat history.
        messages.extend(response)

if __name__ == '__main__':
    run_webui()
    # run_client()