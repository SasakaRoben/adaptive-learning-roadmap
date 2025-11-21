# adaptive-learning-roadmap

An AI-powered adaptive learning platform that creates personalized learning roadmaps with progress tracking and intelligent recommendations.

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/SasakaRoben/adaptive-learning-roadmap.git
cd adaptive-learning-roadmap

# Run the quick start script
./quickstart.sh
```

### Manual Setup

See the [Deployment Guide](DEPLOYMENT.md) for detailed instructions.

## 📚 Documentation

- **[Deployment Guide](DEPLOYMENT.md)** - Complete deployment instructions for various platforms
- **[Deploy Folder](deploy/README.md)** - Alternative deployment configurations

## 🏗️ Architecture

- **Frontend**: Static HTML/CSS/JavaScript application
- **Backend**: FastAPI (Python) with PostgreSQL database
- **AI Features**: Google Gemini integration for personalized learning recommendations

## 🛠️ Deployment Options

1. **Docker Compose** - One-command local deployment
2. **Railway + Vercel** - Backend on Railway, Frontend on Vercel
3. **Render** - All-in-one platform deployment
4. **Custom Docker** - Deploy to any Docker-compatible host

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.

## 📦 Features

- 🎯 Personalized learning paths
- 📊 Progress tracking and analytics
- 🤖 AI-powered recommendations
- 📝 Assessment system
- 💬 Interactive chatbot assistance

## 🔧 Development

```bash
# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload

# Serve frontend (in another terminal)
cd frontend
python -m http.server 8080
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.
