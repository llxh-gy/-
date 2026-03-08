# AI 测试用例生成与缺陷分析助手

## 项目简介
针对传统手工编写测试用例效率低、易遗漏边界场景的问题，本项目基于大语言模型（MiniMax M2.5）开发了一款智能化测试辅助工具。通过自然语言处理技术，实现从需求文档自动生成结构化测试用例，并对缺陷报告进行根因分类，旨在提升测试工程师的工作效率。

## 技术栈
- 后端：Python + Flask
- AI 模型：MiniMax API（兼容 OpenAI 格式）
- 前端：HTML + CSS（Jinja2 模板）
- 其他：Git、Markdown、Prompt Engineering

## 核心功能
- **测试用例自动生成**：输入需求描述，AI 自动生成包含正常、异常、边界值、安全场景的测试用例表（Markdown 格式）。
- **缺陷智能分析**：输入缺陷描述，AI 给出分类（前端/后端/数据/环境）及排查步骤建议。
- **Web 交互界面**：通过 Flask 提供简洁的 Web 页面，实时展示生成结果。

## 快速开始
1. 克隆仓库：`git clone https://github.com/llxh-gy/-.git`
2. 安装依赖：`pip install -r requirements.txt`
3. 设置环境变量 `MINIMAX_API_KEY`
4. 运行：`python app.py`
5. 访问 `http://127.0.0.1:5000`前往用例设计
6. 访问 `http://127.0.0.1:5000/defect`前往缺陷分析

## 效果示例
<img width="2549" height="1403" alt="微信图片_20260308105406_169_15" src="https://github.com/user-attachments/assets/f046581f-e032-4469-9104-b87f2fbdeeab" />
<img width="2549" height="1403" alt="微信图片_20260308105435_170_15" src="https://github.com/user-attachments/assets/a826250b-5273-4bc9-ba10-6a8410d334db" />
<img width="2549" height="1403" alt="微信图片_20260308105448_171_15" src="https://github.com/user-attachments/assets/a2e4a61b-bead-48ff-8e95-567743841d70" />
<img width="2549" height="1403" alt="微信图片_20260308105500_172_15" src="https://github.com/user-attachments/assets/7b1d9f41-176e-4aac-b14e-0697d502c09a" />
<img width="2549" height="1403" alt="微信图片_20260308110230_173_15" src="https://github.com/user-attachments/assets/71b8d096-d5b5-4b14-9c36-d33840a8d684" />
<img width="2549" height="1403" alt="微信图片_20260308110241_174_15" src="https://github.com/user-attachments/assets/f72f400f-c6c1-4696-9ed1-5ad36cd68d5f" />
<img width="2549" height="1403" alt="微信图片_20260308110251_175_15" src="https://github.com/user-attachments/assets/965aefcb-61fd-4e47-9b4a-f165b1499564" />
<img width="2549" height="1403" alt="微信图片_20260308110302_176_15" src="https://github.com/user-attachments/assets/16f872b7-96c0-4c9e-ac99-2c2b327bc23a" />
<img width="2481" height="237" alt="微信图片_20260308110312_177_15" src="https://github.com/user-attachments/assets/04ffe0f1-12f7-4341-b480-b02e1532d50d" />

## 项目结构
.
├── app.py # Flask 主程序
├── ai_utils.py # API 调用与 Prompt 封装
├── templates/ # HTML 模板
│ ├── index.html # 用例生成页面
│ └── defect.html # 缺陷分析页面
├── requirements.txt # 依赖列表
└── README.md # 本文件
