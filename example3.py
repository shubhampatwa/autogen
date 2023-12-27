# Accepted file formats for that can be stored in 
# a vector database instance
import autogen
from autogen.retrieve_utils import TEXT_FORMATS

# print("Accepted file formats for `docs_path`:")
# print(TEXT_FORMATS)

from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb
import os
import json

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path='.env', # If None the function will try to find in the working directory
    model_api_key_map={
        "dayzerov1": {
            "api_key_env_var": "AZURE_OPENAI_API_KEY",
            "api_version": "2023-07-01-preview",
            "base_url": "https://testingdayzero.openai.azure.com/",
            'api_type': 'azure',
        },
    },
    filter_dict={
        "model": {
            'dayzerov1',
        }
    }
)

# 1. create an RetrieveAssistantAgent instance named "assistant"
assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,
    },
)

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": [
            "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Examples/Integrate%20-%20Spark.md",
            "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Research.md",
            os.path.join(os.path.abspath(''), "..", "website", "docs"),
        ],
        "custom_text_types": ["mdx"],
        "chunk_token_size": 2000,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "embedding_model": "all-mpnet-base-v2",
        "get_or_create": True,  # set to False if you don't want to reuse an existing collection, but you'll need to remove the collection manually
    },
    code_execution_config=False, # set to False if you don't want to execute the code
)

# assistant.reset()

# code_problem="How can I use FLAML to perform a classification task and use spark to do parallel training. Train 30 seconds and force cancel jobs if time limit is reached."
# ragproxyagent.initiate_chat(assistant, problem=code_problem, search_string="spark")


# assistant.reset()

# qa_problem = "Who is the author of FLAML?"
# ragproxyagent.initiate_chat(assistant, problem=qa_problem)


# assistant.reset()

# ragproxyagent.human_input_mode = "ALWAYS"
# code_problem = "how to build a time series forecasting model for stock price using FLAML?"
# ragproxyagent.initiate_chat(assistant, problem=code_problem)


assistant.reset()

# set `human_input_mode` to be `ALWAYS`, so the agent will ask for human input at every step.
# ragproxyagent.human_input_mode = "ALWAYS"
# qa_problem = "Is there a function named `tune_automl` in FLAML?"
# ragproxyagent.initiate_chat(assistant, problem=qa_problem)

corpus_file = "https://huggingface.co/datasets/thinkall/NaturalQuestionsQA/resolve/main/corpus.txt"

# Create a new collection for NaturalQuestions dataset
# `task` indicates the kind of task we're working on. In this example, it's a `qa` task.
ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "qa",
        "docs_path": corpus_file,
        "chunk_token_size": 2000,
        "model": "gpt-35-turbo",
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "collection_name": "natural-questions1",
        "chunk_mode": "one_line",
        "embedding_model": "all-MiniLM-L6-v2",
    },
)

queries = """{"_id": "ce2342e1feb4e119cb273c05356b33309d38fa132a1cbeac2368a337e38419b8", "text": "what is non controlling interest on balance sheet", "metadata": {"answer": ["the portion of a subsidiary corporation 's stock that is not owned by the parent corporation"]}}
{"_id": "3a10ff0e520530c0aa33b2c7e8d989d78a8cd5d699201fc4b13d3845010994ee", "text": "how many episodes are in chicago fire season 4", "metadata": {"answer": ["23"]}}
{"_id": "fcdb6b11969d5d3b900806f52e3d435e615c333405a1ff8247183e8db6246040", "text": "what are bulls used for on a farm", "metadata": {"answer": ["breeding", "as work oxen", "slaughtered for meat"]}}
{"_id": "26c3b53ec44533bbdeeccffa32e094cfea0cc2a78c9f6a6c7a008ada1ad0792e", "text": "has been honoured with the wisden leading cricketer in the world award for 2016", "metadata": {"answer": ["Virat Kohli"]}}
{"_id": "0868d0964c719a52cbcfb116971b0152123dad908ac4e0a01bc138f16a907ab3", "text": "who carried the usa flag in opening ceremony", "metadata": {"answer": ["Erin Hamlin"]}}
"""
queries = [json.loads(line) for line in queries.split("\n") if line]
questions = [q["text"] for q in queries]
answers = [q["metadata"]["answer"] for q in queries]
print(questions)
print(answers)

for i in range(len(questions)):
    print(f"\n\n>>>>>>>>>>>>  Below are outputs of Case {i+1}  <<<<<<<<<<<<\n\n")

    # reset the assistant. Always reset the assistant before starting a new conversation.
    assistant.reset()
    
    qa_problem = questions[i]
    ragproxyagent.initiate_chat(assistant, problem=qa_problem, n_results=30)