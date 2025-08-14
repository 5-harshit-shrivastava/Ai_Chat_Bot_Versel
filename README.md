# RAG AI Chatbot

A modern RAG (Retrieval Augmented Generation) chatbot with document upload and Q&A capabilities, featuring an AskDisha 2.0 inspired UI.

## 🚀 Features

- **Document Upload & Processing** - Upload TXT, PDF, DOC files
- **Vector Search** - PostgreSQL with pgvector for semantic search
- **AI-Powered Chat** - Google Gemini integration for responses
- **Modern UI** - AskDisha 2.0 inspired floating widget design
- **Voice Input** - Speech recognition support
- **Mobile Responsive** - Works on all devices
- **Easy Embedding** - Drop-in widget for any website

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI** - Modern Python web framework
- **PostgreSQL + pgvector** - Vector database for embeddings
- **Google Gemini** - AI model for generating responses
- **Sentence Transformers** - Text embedding generation

### Frontend (Vanilla JS)
- **Pure HTML/CSS/JS** - No frameworks, fast loading
- **Floating Widget** - Non-intrusive chat interface
- **Real-time Chat** - WebSocket-like experience
- **Voice Integration** - Speech recognition API

## 📦 Deployment

### Backend Deployment (Render)

1. **Create Backend Service on Render:**
```bash
# Connect your GitHub repository
# Service Type: Web Service
# Environment: Python
# Build Command: pip install -r requirements.txt  
# Start Command: python main.py
```

2. **Environment Variables to Set:**
```
NEON_DATABASE_URL=postgresql://username:password@host:5432/database
GEMINI_API_KEY=your_google_gemini_api_key
PORT=8000
```

3. **Deploy Commands:**
```bash
cd backend
git add .
git commit -m "Backend ready for deployment"
git push origin main
```

### Frontend Deployment (Render)

1. **Create Frontend Service on Render:**
```bash
# Service Type: Static Site
# Build Command: npm install
# Publish Directory: ./
```

2. **Update Backend URL:**
- Edit `frontend/widget.js` line 27
- Replace `your-backend-name.onrender.com` with your actual backend URL

3. **Deploy Commands:**
```bash
cd frontend
npm install
git add .
git commit -m "Frontend ready for deployment"
git push origin main
```

## 🔧 Local Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export NEON_DATABASE_URL="your_postgres_url"
export GEMINI_API_KEY="your_gemini_key"

python main.py
```

### Frontend Setup
```bash
cd frontend
python -m http.server 8080
# Or use Node.js
npm install
npm start
```

Visit: `http://localhost:8080`

## 🌐 API Endpoints

### POST `/chat`
```json
{
  "query": "What is the capital of Canada?"
}
```

### POST `/documents`
```json
{
  "content": "Document text content...",
  "metadata": {"filename": "doc.txt"}
}
```

### DELETE `/documents`
Clears all documents from database.

## 💡 Usage

### Embed Widget on Any Website
```html
<!-- Add to your website -->
<link rel="stylesheet" href="https://your-frontend-url.onrender.com/widget.css">
<script src="https://your-frontend-url.onrender.com/widget.js"></script>

<!-- Widget will auto-initialize -->
```

### Custom Configuration
```javascript
window.ragChatbot = new RAGChatbotWidget({
    apiBaseUrl: 'https://your-backend.onrender.com',
    position: 'bottom-right'
});
```

## 🔒 Security

- CORS properly configured
- Input validation and sanitization
- Environment variables for sensitive data
- No API keys exposed in frontend

## 📱 Mobile Support

- Responsive design
- Touch-friendly interface
- Voice input on mobile devices
- Optimized for all screen sizes

## 🎨 Customization

- Modify `widget.css` for styling changes
- Update colors, fonts, animations
- Add custom branding and logos
- Extend functionality in `widget.js`

## 📄 License

MIT License - feel free to use in your projects!