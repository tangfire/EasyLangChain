import os

import dotenv
from langchain_openai import ChatOpenAI


# 调用非对话模型:
# llms = OpenAI(...)

dotenv.load_dotenv() # 加载当前目录下的.env文件

os.environ["ARK_API_KEY"] = os.getenv("ARK_API_KEY")
os.environ["MODEL"] = os.getenv("MODEL")
os.environ["BASE_URL"] = os.getenv("BASE_URL")


# 调用对话模型:
chat_model =  ChatOpenAI(
    model_name=os.environ['MODEL'],
    base_url=os.environ['BASE_URL'],
    api_key=os.environ['ARK_API_KEY']
)

response =   chat_model.invoke("什么是LangChain?")

print(response.content)

