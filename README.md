# RAG AI Chatbot

A modern AI-powered knowledge assistant chatbot featuring an AskDisha 2.0 inspired UI with floating animation and voice input capabilities.

## 🚀 Features

- **AI-Powered Chat** - Google Gemini integration for intelligent responses
- **Modern UI** - AskDisha 2.0 inspired floating widget design with animated avatar
- **Voice Input** - Speech recognition support
- **Mobile Responsive** - Works on all devices
- **Easy Embedding** - Drop-in widget for any website
- **Real-time Chat** - Instant responses and typing indicators

## 🏗️ Architecture

### Backend (FastAPI) - **DEPLOYED** ✅
- **FastAPI** - Modern Python web framework
- **PostgreSQL + pgvector** - Vector database for embeddings
- **Google Gemini** - AI model for generating responses
- **Sentence Transformers** - Text embedding generation
- **Deployed URL**: `https://ai-chat-bot-ote0.onrender.com`

### Frontend (Vanilla JS)
- **Pure HTML/CSS/JS** - No frameworks, fast loading
- **Floating Widget** - Non-intrusive chat interface with animated avatar
- **Real-time Chat** - Smooth user experience
- **Voice Integration** - Speech recognition API

## 🌐 Live Backend API

**Base URL**: `https://ai-chat-bot-ote0.onrender.com`

### Available Endpoints:
- `GET /` - Health check
- `GET /health` - Service status  
- `POST /chat` - Send chat messages
- `POST /documents` - Add documents (backend only)
- `DELETE /documents` - Clear documents (backend only)

## 🔧 Local Development

### Frontend Setup
```bash
cd frontend
python -m http.server 8080
# Or use Node.js
npm install
npm start
```

Visit: `http://localhost:8080`

## 💡 Widget Integration

### Add to Any Website
Simply include these files in your webpage:

```html
<!-- Add CSS -->
<link rel="stylesheet" href="widget.css">

<!-- Add Widget HTML Structure -->
<div class="rag-chatbot-toggle" id="ragChatbotToggle">
    <svg viewBox="0 0 24 24">
        <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
    </svg>
</div>

<!-- Full widget structure (copy from index.html) -->
<div class="rag-chatbot-widget" id="ragChatbotWidget">
    <!-- Widget content -->
</div>

<!-- Add JavaScript -->
<script src="widget.js"></script>
<script>
    // Widget auto-initializes with deployed backend
    const chatbot = new RAGChatbotWidget({
        apiBaseUrl: 'https://ai-chat-bot-ote0.onrender.com'
    });
</script>
```

### Custom Configuration
```javascript
window.ragChatbot = new RAGChatbotWidget({
    apiBaseUrl: 'https://ai-chat-bot-ote0.onrender.com',
    position: 'bottom-right'
});
```

## 🎨 UI Features

- **Floating Avatar Animation** - The girl icon in the header has a smooth floating animation
- **Clean Design** - Minimalist interface focused on chat interaction
- **Voice Input Button** - Click microphone icon for speech recognition
- **Responsive Layout** - Adapts to mobile and desktop screens
- **Smooth Transitions** - Polished animations and hover effects

## 📱 Mobile Support

- Responsive design that adapts to mobile screens
- Touch-friendly interface with proper button sizing
- Voice input works on mobile devices
- Full-screen chat on smaller devices

## 🔒 Security

- Backend properly deployed with environment variables
- CORS configured for frontend integration
- Input validation and sanitization
- No sensitive data exposed in frontend code

## 🚀 Deployment Status

### Backend - ✅ DEPLOYED
- **URL**: https://ai-chat-bot-ote0.onrender.com
- **Status**: Live and operational
- **Database**: PostgreSQL with pgvector on Neon
- **AI Model**: Google Gemini integrated

### Frontend - 📁 LOCAL
- Ready for deployment to any static hosting
- Can be embedded in any website
- No build process required - pure HTML/CSS/JS

## 🎯 How It Works

1. **User opens chat** - Clicks the blue floating chat button
2. **Welcome message** - AI greets user as knowledge assistant
3. **User asks questions** - Types or uses voice input
4. **AI responds** - Gemini processes and returns intelligent answers
5. **Continuous chat** - Real-time conversation experience

## 🔧 Customization

### Styling
- Modify `widget.css` for visual changes
- Update colors, fonts, and animations
- Customize avatar image URL
- Adjust widget size and positioning

### Functionality  
- Extend `widget.js` for new features
- Modify welcome messages
- Add custom chat commands
- Integrate with other APIs

## 📄 File Structure

```
rag-chatbot-project/
├── backend/              # Deployed FastAPI backend
│   ├── main.py          # Main application
│   ├── requirements.txt # Dependencies
│   └── Dockerfile       # Container config
└── frontend/            # Chat widget
    ├── index.html       # Demo page
    ├── widget.css       # Widget styles
    ├── widget.js        # Widget functionality
    └── server.js        # Development server
```

## 📄 License

MIT License - feel free to use in your projects!

---

**Ready to use!** The backend is deployed and the frontend widget can be embedded anywhere. Just copy the widget files and you're good to go! 🚀