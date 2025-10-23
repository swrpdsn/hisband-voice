# Hisband Voice (by HisbandHR.AI)

**Hinglish AI Calling MVP for SMBs** (builders first, later recruiters/clinics).

## Overview
Hisband Voice is an AI-powered calling platform that combines a Next.js frontend with a Python FastAPI backend to automate lead management and calling workflows.

## Features
- 📤 Upload leads → Auto-call → Book site visits
- 💬 WhatsApp confirm → Track in dashboard
- 🚀 Powered by Nari.ai/Exotel for intelligent calling
- 🎯 Built for SMBs, recruiters, and clinics

## Tech Stack
- **Frontend**: Next.js, React
- **Backend**: Python, FastAPI
- **AI**: Nari.ai integration
- **Telephony**: Exotel API

## Quick Start

### GitHub Codespaces (Recommended)
1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Install dependencies:
   ```bash
   npm install
   cd api && pip install -r requirements.txt
   ```
3. Run development servers:
   ```bash
   npm run dev  # Frontend on port 3000
   cd api && python main.py  # Backend API
   ```

### Local Setup
1. Clone the repository
2. Install Node.js dependencies: `npm install`
3. Install Python dependencies: `cd api && pip install -r requirements.txt`
4. Run both servers as shown above

## Project Structure
```
/
├── api/              # Python FastAPI backend
│   ├── main.py       # Main API server
│   └── requirements.txt
├── index.html        # Frontend entry point
└── README.md         # This file
```

## License
See LICENSE file for details.
