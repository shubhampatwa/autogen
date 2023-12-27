import autogen
from autogen import AssistantAgent, UserProxyAgent


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

print(config_list)

#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
# create an AssistantAgent instance named "assistant"
# assistant = AssistantAgent(name="assistant")
assistant = AssistantAgent(name="assistant", llm_config={
  "cache_seed": 42,
  # "api_key": "4964a05f4a3c48feaa296f8bb2f260fc",
  "config_list": config_list,
  "temperature": 0,
  })
print("assistant: ", assistant)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
  )

print("user_proxy: ", user_proxy)

user_proxy.initiate_chat(
    assistant,
    message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
)

user_proxy.send(
    recipient=assistant,
    message="""Plot a chart of their stock price change YTD and save to stock_price_ytd.png.""",
)