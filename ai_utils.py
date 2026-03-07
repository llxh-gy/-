import os
import requests
from typing import Optional

# 从环境变量读取 API Key
ACCESS_KEY = os.environ.get("MINIMAX_API_KEY")
if not ACCESS_KEY:
    raise ValueError("请设置环境变量 MINIMAX_API_KEY，例如：export MINIMAX_API_KEY='你的Key'")

# 国内版 API 地址
API_HOST = "https://api.minimax.chat"
CHAT_ENDPOINT = "/v1/chat/completions"  # 正确的端点

def call_minimax(
    prompt: str,
    model: str = "MiniMax-M2.5",
    max_tokens: int = 2000,
    temperature: float = 0.7
) -> Optional[str]:
    """
    调用 MiniMax 国内版 API（OpenAI 兼容格式）
    :param prompt: 用户输入的提示词
    :param model: 模型名称，可选 MiniMax-M2.5, MiniMax-M2.1-lightning 等
    :param max_tokens: 最大生成 token 数
    :param temperature: 温度参数，控制随机性
    :return: 模型生成的文本，失败返回 None
    """
    url = API_HOST + CHAT_ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_KEY}"
    }
    # 构建符合 OpenAI 格式的消息列表
    # 添加 system 提示词，让模型扮演测试工程师
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一位资深的测试工程师，擅长分析需求文档并设计高质量的测试用例，也能对缺陷报告进行根因分析。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.9,
        "stream": False  # 不使用流式输出
    }

    try:
        # 设置超时时间为 60 秒，避免长时间等待
        response = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试或增加超时时间。")
        return None
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
        return None

    # 处理 HTTP 错误状态码
    if response.status_code != 200:
        print(f"API 返回错误状态码 {response.status_code}")
        print("响应内容:", response.text)
        return None

    # 尝试解析 JSON 响应
    try:
        data = response.json()
    except ValueError:
        print("响应不是有效的 JSON 格式:", response.text)
        return None

    # 提取文本内容（OpenAI 兼容格式）
    if "choices" in data and len(data["choices"]) > 0:
        # 检查是否有 message 字段
        message = data["choices"][0].get("message")
        if message and "content" in message:
            return message["content"]
        else:
            # 可能 choices 中直接包含 text（某些模型）
            if "text" in data["choices"][0]:
                return data["choices"][0]["text"]
    # 如果返回格式不符合预期，打印完整响应以便调试
    print("API 返回格式异常，原始数据:", data)
    return None

# ========== Prompt 构建函数 ==========

def build_testcase_prompt(requirement_text: str) -> str:
    """构建测试用例生成的 Prompt"""
    return f"""
请根据以下需求描述，生成一份详细的测试用例表。

需求描述：
{requirement_text}

要求：
1. 覆盖正常场景、异常场景、边界值测试、安全测试。
2. 输出格式为 Markdown 表格，包含以下列：用例编号、测试类型、步骤、预期结果。
3. 用例编号格式为 TC_功能缩写_序号，例如 TC_LOGIN_001。
4. 测试类型可以是：正常流程、异常流程、边界值、安全等。

请开始生成：
"""

def build_defect_prompt(defect_description: str) -> str:
    """构建缺陷分析的 Prompt"""
    return f"""
请分析以下缺陷报告，判断可能的原因（前端问题、后端问题、数据问题、环境问题等），并给出排查步骤建议。

缺陷描述：
{defect_description}

请按以下格式输出：
- 缺陷分类：[前端/后端/数据/环境/不确定]
- 排查建议：
  1. ...
  2. ...
  3. ...

请开始分析：
"""

# ========== 对外接口 ==========

def generate_testcases(requirement: str) -> str:
    """生成测试用例（供 Flask 调用）"""
    prompt = build_testcase_prompt(requirement)
    response = call_minimax(prompt)
    if response:
        return response
    else:
        return "生成失败，请检查 API 调用或网络连接。"

def analyze_defect(defect: str) -> str:
    """分析缺陷（供 Flask 调用）"""
    prompt = build_defect_prompt(defect)
    response = call_minimax(prompt)
    if response:
        return response
    else:
        return "分析失败，请检查 API 调用或网络连接。"

# ========== 本地测试 ==========
if __name__ == "__main__":
    print("=== 测试用例生成 ===")
    req = "用户登录功能：支持手机号和密码登录，密码错误超过3次需输入验证码。"
    print(generate_testcases(req))

    print("\n=== 缺陷分析 ===")
    defect = "在弱网环境下，点击登录按钮，App闪退。"
    print(analyze_defect(defect))