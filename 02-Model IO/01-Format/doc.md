在 LangChain 中，提示模板（Prompt Templates）是用于生成高质量提示的核心组件。它们提供了结构化的方式来构建输入给语言模型的文本。以下是 LangChain 中几种不同类型的提示模板：

---

## 1. 基础提示模板

### `PromptTemplate`
**作用**：最基础的字符串模板，使用 `{}` 作为变量占位符。

**示例**：
```python
from langchain_core.prompts import PromptTemplate

template = "请用{style}的风格写一篇关于{topic}的文章。"
prompt_template = PromptTemplate.from_template(template)

result = prompt_template.invoke({"style": "幽默", "topic": "人工智能"})
print(result.text)
# 输出：请用幽默的风格写一篇关于人工智能的文章。
```

---

## 2. 聊天提示模板

### `ChatPromptTemplate`
**作用**：专门为聊天模型设计，可以包含多条不同角色的消息。

**消息类型**：
- `SystemMessagePromptTemplate` - 系统消息
- `HumanMessagePromptTemplate` - 用户消息  
- `AIMessagePromptTemplate` - AI 助手消息
- `ToolMessagePromptTemplate` - 工具消息

**示例**：
```python
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

system_template = SystemMessagePromptTemplate.from_template(
    "你是一个专业的{role}助手。请用{language}回答。"
)
human_template = HumanMessagePromptTemplate.from_template(
    "请帮我{task}"
)

chat_prompt = ChatPromptTemplate.from_messages([
    system_template,
    human_template
])

result = chat_prompt.invoke({
    "role": "技术", 
    "language": "中文",
    "task": "解释一下机器学习"
})
print(result.messages)
```

---

## 3. 少量示例提示模板

### `FewShotPromptTemplate`
**作用**：包含示例的提示模板，帮助模型更好地理解任务。

**示例**：
```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {"input": "高兴", "output": "今天天气真好，心情特别愉快！"},
    {"input": "悲伤", "output": "雨一直下，心情也跟着低落起来。"}
]

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="输入: {input}\n输出: {output}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="根据情感生成相应的句子：",
    suffix="输入: {input}\n输出:",
    input_variables=["input"]
)

result = few_shot_prompt.invoke({"input": "惊讶"})
print(result.text)
```

---

## 4. 结构化输出提示模板

### `StructuredOutputPromptTemplate`
**作用**：生成要求模型返回结构化数据（如 JSON）的提示。

**示例**：
```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StructuredOutputParser, ResponseSchema

response_schemas = [
    ResponseSchema(name="answer", description="问题的答案"),
    ResponseSchema(name="confidence", description="回答的置信度", type="float")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

template = """
回答以下问题，并按照指定格式返回：

问题: {question}

{format_instructions}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions}
)

result = prompt.invoke({"question": "地球的年龄是多少？"})
print(result.text)
```

---

## 5. 管道提示模板

### `PipelinePromptTemplate`
**作用**：将多个提示模板组合成管道。

**示例**：
```python
from langchain_core.prompts import PipelinePromptTemplate, PromptTemplate

full_template = """
{introduction}

{example}

{start}
"""

introduction_prompt = PromptTemplate.from_template("你是一个{role}助手。")
example_prompt = PromptTemplate.from_template("例如：{example}")
start_prompt = PromptTemplate.from_template("请开始：{query}")

pipeline_prompt = PipelinePromptTemplate(
    final_prompt=PromptTemplate.from_template(full_template),
    pipeline_prompts=[
        ("introduction", introduction_prompt),
        ("example", example_prompt),
        ("start", start_prompt)
    ]
)

result = pipeline_prompt.invoke({
    "role": "技术",
    "example": "解释神经网络",
    "query": "什么是深度学习？"
})
print(result.text)
```

---

## 6. 自定义提示模板

**作用**：创建满足特定需求的模板。

**示例**：
```python
from langchain_core.prompts import BasePromptTemplate
from langchain_core.prompts.utils import get_template_variables

class CustomPromptTemplate(BasePromptTemplate):
    def format(self, **kwargs):
        # 自定义格式化逻辑
        formatted = f"自定义前缀: {kwargs['content']} - 自定义后缀"
        return formatted
    
    def invoke(self, input, config=None):
        return self.format(**input)

custom_prompt = CustomPromptTemplate(input_variables=["content"])
result = custom_prompt.invoke({"content": "测试内容"})
print(result)  # 输出: 自定义前缀: 测试内容 - 自定义后缀
```

---

## 7. 多模态提示模板

**作用**：支持文本和图像等多模态输入。

**示例**：
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

# 多模态提示（需要支持多模态的模型）
multimodal_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个能够理解图像和文本的助手。"),
    ("human", [
        {"type": "text", "text": "请描述这张图片：{image_description}"},
        {"type": "image_url", "image_url": {"url": "{image_url}"}}
    ])
])

# 实际使用时需要支持多模态的模型
```

---

## 8. 条件提示模板

**作用**：根据条件动态选择不同的提示。

**示例**：
```python
from langchain_core.prompts import ConditionalPromptTemplate, PromptTemplate

base_template = PromptTemplate.from_template("基本提示: {input}")
advanced_template = PromptTemplate.from_template("高级提示: {input} - 详细分析")

def condition_fn(data):
    return data.get("is_advanced", False)

conditional_prompt = ConditionalPromptTemplate(
    condition=condition_fn,
    on_true=advanced_template,
    on_false=base_template,
    input_variables=["input", "is_advanced"]
)

# 使用基本模板
result1 = conditional_prompt.invoke({"input": "测试", "is_advanced": False})
print(result1.text)  # 输出: 基本提示: 测试

# 使用高级模板  
result2 = conditional_prompt.invoke({"input": "测试", "is_advanced": True})
print(result2.text)  # 输出: 高级提示: 测试 - 详细分析
```

---

## 总结对比

| 模板类型 | 主要用途 | 特点 |
|---------|---------|------|
| `PromptTemplate` | 基础文本提示 | 简单字符串格式化 |
| `ChatPromptTemplate` | 聊天对话 | 支持多角色消息 |
| `FewShotPromptTemplate` | 少样本学习 | 包含示例数据 |
| `StructuredOutputPromptTemplate` | 结构化输出 | 要求特定格式返回 |
| `PipelinePromptTemplate` | 复杂流程 | 多个模板组合 |
| 自定义模板 | 特殊需求 | 完全自定义逻辑 |
| 多模态模板 | 多模态输入 | 支持文本+图像 |
| 条件模板 | 动态选择 | 根据条件选择不同模板 |

这些提示模板可以根据具体需求灵活组合使用，构建出适合各种场景的高质量提示。