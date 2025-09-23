# Hisband Voice (by HisbandHR.AI)

Hinglish AI Calling MVP for SMBs (builders first, later recruiters/clinics).  
**Upload leads → Auto-call → Book site visits → WhatsApp confirm → Track in dashboard.**

---

## 🚀 What’s inside (MVP stack)
- **API:** FastAPI (Python 3.11) – `/health`, `/ask` demo
- **Web:** Next.js (React 18) – basic dashboard page
- **Dev Env:** GitHub **Codespaces** (browser-based IDE)
- **Runtime (optional):** Docker Compose (api + web; DB/Redis add later)
- **Config:** `.env` for keys (OpenAI etc.)

> Goal: Get a working dev environment in **Codespaces in minutes**, then plug telephony/ASR/TTS later.

---

## ✅ Quick Start (GitHub Codespaces)

1) **Open in Codespaces**
   - GitHub → your repo → **Code** ➜ **Create codespace on main**

2) **Create env file**
   ```bash
   cp .env.example .env
   # Open .env and paste your real keys (at minimum OPENAI_API_KEY)
# hisband-voice
