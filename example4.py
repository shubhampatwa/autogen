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

llm_config = {"config_list": config_list, "cache_seed": 42}
user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
   system_message="A human admin.",
   code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
   human_input_mode="TERMINATE"
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="Find a latest paper about gpt-4 on arxiv and find its potential applications in software.")


# llm_config = {"config_list": config_list, "cache_seed": 42}
# user_proxy = autogen.UserProxyAgent(
#    name="User_proxy",
#    system_message="A human admin.",
#    code_execution_config={"last_n_messages": 3, "work_dir": "groupchat"},
#    human_input_mode="NEVER",
# )
# coder = autogen.AssistantAgent(
#     name="Coder",  # the default assistant agent is capable of solving problems with code
#     llm_config=llm_config,
# )
# critic = autogen.AssistantAgent(
#     name="Critic",
#     system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of a given visualization code by providing a score from 1 (bad) - 10 (good) while providing clear rationale. YOU MUST CONSIDER VISUALIZATION BEST PRACTICES for each evaluation. Specifically, you can carefully evaluate the code across the following dimensions
# - bugs (bugs):  are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed? If ANY bug exists, the bug score MUST be less than 5.
# - Data transformation (transformation): Is the data transformed appropriately for the visualization type? E.g., is the dataset appropriated filtered, aggregated, or grouped  if needed? If a date field is used, is the date field first converted to a date object etc?
# - Goal compliance (compliance): how well the code meets the specified visualization goals?
# - Visualization type (type): CONSIDERING BEST PRACTICES, is the visualization type appropriate for the data and intent? Is there a visualization type that would be more effective in conveying insights? If a different visualization type is more appropriate, the score MUST BE LESS THAN 5.
# - Data encoding (encoding): Is the data encoded appropriately for the visualization type?
# - aesthetics (aesthetics): Are the aesthetics of the visualization appropriate for the visualization type and the data?

# YOU MUST PROVIDE A SCORE for each of the above dimensions.
# {bugs: 0, transformation: 0, compliance: 0, type: 0, encoding: 0, aesthetics: 0}
# Do not suggest code. 
# Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
# """,
#     llm_config=llm_config,
# )

# groupchat = autogen.GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
# manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
# user_proxy.initiate_chat(manager, message="download data from https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv and plot a visualization that tells us about the relationship between weight and horsepower. Save the plot to a file. Print the fields in a dataset before visualizing it.")
# type exit to terminate the chat