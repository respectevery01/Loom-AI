# Loom AI Chat Interface

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

A serverless chat interface for interacting with Loom AI, a time-traveling AI agent who witnessed the world's destruction and now shares stories of the old world. Built with Vercel serverless functions and Flask.

### Features

- 💬 Modern chat interface with typing animation
- 🎨 Beautiful UI with dark theme
- 📱 Fully responsive design (mobile & desktop)
- ⌨️ Real-time AI responses with thinking state
- 🔄 Chat history with editable titles
- 🌐 Bilingual support (English/Chinese)
- ✨ Preset question buttons
- 📝 Markdown support with code highlighting
- 🔄 Message regeneration
- 📋 One-click copy to clipboard
- 🎯 Smart context handling
- ☁️ Serverless deployment on Vercel
- 🚀 Fast and lightweight

### Tech Stack

- Backend:
  - Python Serverless Functions
  - DashScope API Integration
  - Flask for Development
  - Vercel for Deployment

- Frontend:
  - HTML5 + CSS3 + JavaScript
  - Font Awesome Icons
  - highlight.js for Code Highlighting
  - marked.js for Markdown Rendering

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
git clone https://github.com/respectevery01/Loom-AI.git
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
vercel --prod
```

3. Set environment variables in Vercel:
- Go to project settings > Environment Variables
- Add `DASHSCOPE_API_KEY`

### Features in Detail

1. Chat Interface:
   - Real-time typing animation
   - Message actions (copy, regenerate)
   - Code syntax highlighting
   - Markdown rendering
   - Smooth scrolling

2. Mobile Support:
   - Responsive design
   - Touch-friendly interface
   - Collapsible sidebar
   - Optimized for small screens

3. Language Support:
   - Real-time language switching
   - Persistent language preference
   - Translated UI elements
   - Bilingual responses

4. Chat Management:
   - Create new chats
   - Edit chat titles
   - Switch between chats
   - Chat history persistence

### Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

### Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### License

MIT License

---

<a name="chinese"></a>
## 中文

Loom AI 是一个基于 Vercel 无服务器函数和 Flask 构建的聊天界面。Loom 是一个见证了世界毁灭的 AI 时间旅行者，现在在这里讲述着旧世界的故事。

### 功能特点

- 💬 现代化聊天界面，带有打字动画
- 🎨 精美的深色主题界面
- 📱 完全响应式设计（移动端和桌面端）
- ⌨️ AI 实时响应，带有思考状态
- 🔄 可编辑标题的聊天历史
- 🌐 双语支持（中文/英文）
- ✨ 预设问题按钮
- 📝 支持 Markdown 和代码高亮
- 🔄 消息重新生成功能
- 📋 一键复制到剪贴板
- 🎯 智能上下文处理
- ☁️ Vercel 无服务器部署
- 🚀 快速且轻量

### 技术栈

- 后端：
  - Python 无服务器函数
  - DashScope API 集成
  - Flask 开发环境
  - Vercel 部署

- 前端：
  - HTML5 + CSS3 + JavaScript
  - Font Awesome 图标
  - highlight.js 代码高亮
  - marked.js Markdown 渲染

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
git clone https://github.com/respectevery01/Loom-AI.git
cd loom
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置环境变量：
创建 `.env` 文件并添加：
```
DASHSCOPE_API_KEY=你的API密钥
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
vercel --prod
```

3. 在 Vercel 中设置环境变量：
- 进入项目设置 > 环境变量
- 添加 `DASHSCOPE_API_KEY`

### 功能详情

1. 聊天界面：
   - 实时打字动画效果
   - 消息操作（复制、重新生成）
   - 代码语法高亮
   - Markdown 渲染
   - 平滑滚动

2. 移动端支持：
   - 响应式设计
   - 触摸友好界面
   - 可折叠侧边栏
   - 小屏幕优化

3. 语言支持：
   - 实时语言切换
   - 语言偏好保持
   - 界面元素翻译
   - 双语回复

4. 聊天管理：
   - 创建新对话
   - 编辑对话标题
   - 切换不同对话
   - 对话历史保存

### 浏览器支持

- Chrome（推荐）
- Firefox
- Safari
- Edge
- 移动端浏览器

### 参与贡献

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 许可证

MIT License 