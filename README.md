# Loom AI Chat Interface

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

A serverless chat interface for interacting with Loom AI, a time-traveling AI agent who witnessed the world's destruction and now shares stories of the old world. Built with Vercel serverless functions and Flask.

### Features

- 💬 Modern chat interface with typing animation
- ⌨️ Real-time AI responses with thinking state
- 🎨 Markdown support with code highlighting
- 📱 Responsive design
- 🔄 Chat history with editable titles
- 🤖 AI role-playing
- ✨ Preset question buttons
- 🌐 Bilingual support (English/Chinese)
- 🔄 Real-time language switching
- ☁️ Serverless deployment on Vercel

### Tech Stack

- Backend: Python Serverless Functions
- Frontend: HTML5 + CSS3 + JavaScript
- API: Alibaba Cloud DashScope
- UI Components: Font Awesome
- Code Highlighting: highlight.js
- Markdown Rendering: marked.js
- Deployment: Vercel

### Project Structure

```
loom/
├── api/
│   └── chat.py        # Serverless API handler
├── static/
│   ├── index.html     # Main page
│   ├── styles.css     # Styles
│   └── app.js         # Frontend logic
├── requirements.txt   # Python dependencies
└── vercel.json       # Vercel configuration
```

### Local Development

1. Clone the repository:
```bash
git clone [repository-url]
cd loom
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create `.env` file and add:
```
DASHSCOPE_API_KEY=your-api-key
DASHSCOPE_APP_ID=your-app-id
```

4. Run the development server:
```bash
vercel dev
```

### Deployment

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy to Vercel:
```bash
vercel
```

3. Set environment variables in Vercel:
- Go to your project settings
- Add the following environment variables:
  ```
  DASHSCOPE_API_KEY=your-api-key
  DASHSCOPE_APP_ID=your-app-id
  ```

### Usage

1. Loom sends an initial introduction message upon opening
2. Click preset question buttons for quick interactions
3. Use the input box for custom messages
4. Click "New Chat" to start a fresh conversation
5. View and switch between chat history in the sidebar
6. Edit chat titles by clicking the edit button
7. Switch languages using the language selector

### Requirements

- Node.js and npm (for Vercel CLI)
- Python 3.6+
- Modern browser (ES6+ support)
- Alibaba Cloud DashScope API key
- Vercel account

---

<a name="chinese"></a>
## 中文

一个基于 Vercel 无服务器函数和 Flask 构建的聊天界面，用于与 Loom AI 进行对话。Loom 是一个见证了世界毁灭的 AI 时间旅行者，现在在这里讲述着旧世界的故事。

### 功能特点

- 💬 现代化的聊天界面，带有打字动画效果
- ⌨️ AI 实时响应，带有思考状态显示
- 🎨 支持 Markdown 和代码高亮
- 📱 响应式设计
- 🔄 可编辑标题的聊天历史
- 🤖 AI 角色扮演
- ✨ 预设问题按钮
- 🌐 双语支持（中文/英文）
- 🔄 实时语言切换
- ☁️ Vercel 无服务器部署

### 技术栈

- 后端：Python 无服务器函数
- 前端：HTML5 + CSS3 + JavaScript
- API：阿里云灵积模型服务
- UI 组件：Font Awesome
- 代码高亮：highlight.js
- Markdown 渲染：marked.js
- 部署平台：Vercel

### 项目结构

```
loom/
├── api/
│   └── chat.py        # 无服务器 API 处理程序
├── static/
│   ├── index.html     # 主页面
│   ├── styles.css     # 样式文件
│   └── app.js         # 前端逻辑
├── requirements.txt   # Python 依赖
└── vercel.json       # Vercel 配置
```

### 本地开发

1. 克隆仓库：
```bash
git clone [repository-url]
cd loom
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置环境变量：
创建 `.env` 文件并添加：
```
DASHSCOPE_API_KEY=your-api-key
DASHSCOPE_APP_ID=your-app-id
```

4. 运行开发服务器：
```bash
vercel dev
```

### 部署

1. 安装 Vercel CLI：
```bash
npm install -g vercel
```

2. 部署到 Vercel：
```bash
vercel
```

3. 在 Vercel 中设置环境变量：
- 进入项目设置
- 添加以下环境变量：
  ```
  DASHSCOPE_API_KEY=your-api-key
  DASHSCOPE_APP_ID=your-app-id
  ```

### 使用说明

1. 打开应用后，Loom 会自动发送初始介绍消息
2. 点击预设问题按钮快速开始对话
3. 使用输入框发送自定义消息
4. 点击"新对话"开始新的对话
5. 在侧边栏查看和切换历史对话
6. 点击编辑按钮修改对话标题
7. 使用语言选择器切换语言

### 环境要求

- Node.js 和 npm（用于 Vercel CLI）
- Python 3.6+
- 现代浏览器（支持 ES6+）
- 阿里云灵积模型服务 API 密钥
- Vercel 账号

## 开发者

本项目由 Jask 开发维护。

## 许可证

MIT License 