import os
from volcenginesdkarkruntime import Ark
import dotenv
# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key

dotenv.load_dotenv() # 加载当前目录下的.env文件

os.environ["ARK_API_KEY"] = os.getenv("ARK_API_KEY")


client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key=os.environ.get("ARK_API_KEY"),
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
   # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-1-5-pro-32k-250115",
    messages=[
        {"role": "system", "content": "你是人工智能助手."},
        {"role": "user", "content": "你好"},
    ],
    # 免费开启推理会话应用层加密，访问 https://www.volcengine.com/docs/82379/1389905 了解更多
    extra_headers={'x-is-encrypted': 'true'},
)
print(completion.choices[0].message.content)

# Streaming:
# print("----- streaming request -----")
# stream = client.chat.completions.create(
#     model="doubao-1-5-pro-32k-250115",
#     messages=[
#         {"role": "system", "content": "你是人工智能助手."},
#         {"role": "user", "content": "你好"},
#     ],
#     # 免费开启推理会话应用层加密，访问 https://www.volcengine.com/docs/82379/1389905 了解更多
#     extra_headers={'x-is-encrypted': 'true'},
#     # 响应内容是否流式返回
#     stream=True,
# )
# for chunk in stream:
#     if not chunk.choices:
#         continue
#     print(chunk.choices[0].delta.content, end="")
# print()