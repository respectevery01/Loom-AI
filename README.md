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

2. Push your code to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push
```

3. Import to Vercel:
- Go to [Vercel Dashboard](https://vercel.com/dashboard)
- Click "Add New" > "Project"
- Select your GitHub repository
- Configure project:
  - Framework Preset: Other
  - Root Directory: ./
  - Build Command: None
  - Output Directory: static
  - Install Command: pip install -r requirements.txt

4. Set environment variables in Vercel:
- Go to project settings > Environment Variables
- Add the following variables:
  ```
  DASHSCOPE_API_KEY=your-api-key
  DASHSCOPE_APP_ID=your-app-id
  ```
- Click "Save"

5. Deploy:
```bash
vercel --prod
```

6. Verify API Configuration:
- After deployment, test the API endpoint:
  ```bash
  curl -X POST https://your-project.vercel.app/api/chat \
    -H "Content-Type: application/json" \
    -d '{"prompt":"Hello"}'
  ```
- Check Vercel Function Logs in dashboard if there are issues

### Troubleshooting Deployment

1. API Issues:
- Check Function Logs in Vercel Dashboard
- Verify environment variables are set correctly
- Ensure `api/chat.py` is in the correct location
- Check Python dependencies in `requirements.txt`

2. Static Files:
- Verify static files are in the `static` directory
- Check file paths in `vercel.json`
- Test local development with `vercel dev`

3. Common Problems:
- 500 Error: Check Function Logs and environment variables
- 404 Error: Verify API route in `vercel.json`
- CORS Issues: API handler includes correct headers

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

2. 将代码推送到 GitHub：
```bash
git add .
git commit -m "Initial commit"
git push
```

3. 导入到 Vercel：
- 访问 [Vercel 控制台](https://vercel.com/dashboard)
- 点击 "Add New" > "Project"
- 选择你的 GitHub 仓库
- 配置项目：
  - Framework Preset（框架预设）：Other
  - Root Directory（根目录）：./
  - Build Command（构建命令）：None
  - Output Directory（输出目录）：static
  - Install Command（安装命令）：pip install -r requirements.txt

4. 设置环境变量：
- 进入项目设置 > Environment Variables（环境变量）
- 添加以下变量：
  ```
  DASHSCOPE_API_KEY=你的API密钥
  DASHSCOPE_APP_ID=你的应用ID
  ```
- 点击 "Save"（保存）

5. 部署：
```bash
vercel --prod
```

6. 验证 API 配置：
- 部署完成后，测试 API 端点：
  ```bash
  curl -X POST https://your-project.vercel.app/api/chat \
    -H "Content-Type: application/json" \
    -d '{"prompt":"Hello"}'
  ```
- 如果有问题，查看 Vercel 控制台中的 Function Logs（函数日志）

### 部署故障排除

1. API 问题：
- 检查 Vercel 控制台中的函数日志
- 验证环境变量是否正确设置
- 确保 `api/chat.py` 在正确的位置
- 检查 `requirements.txt` 中的 Python 依赖

2. 静态文件：
- 验证静态文件是否在 `static` 目录中
- 检查 `vercel.json` 中的文件路径
- 使用 `vercel dev` 测试本地开发

3. 常见问题：
- 500 错误：检查函数日志和环境变量
- 404 错误：验证 `vercel.json` 中的 API 路由
- CORS 问题：确保 API 处理程序包含正确的头部

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