# ✉️ AI Cold Email Generator
AI-powered Cold Email Generator using LangChain and ChromaDB that intelligently matches job descriptions with portfolio projects via vector search to create personalized, professional cold emails for job applications with a Streamlit interface.


> **LangChain · ChromaDB · Groq LLaMA · Streamlit**  
> Paste a job description → get a personalized, portfolio-matched cold email in ~8 seconds.

---
## 📸 Interface Preview

![Cold Email Generator Interface](https://raw.githubusercontent.com/Tayyabah-Rehman/Cold-Email-Generator/main/Screenshots/1st.PNG)

*Screenshot of the Cold Email Generator showing job description input and generated email output.*

---

## 🚀 Quick Start (3 steps)

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/Tayyabah-Rehman/Cold-Email-Generator.git
cd Cold-Email-Generator

# Create virtual environment with Python 3.10
py -3.10 -m venv .venv

# Activate the environment
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # Mac/Linux

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

---

## 📁 Project Structure

```
cold_email_generator/
├── run.py                ← ONE-CLICK LAUNCHER (python run.py)
├── .env                  ← Your API keys (git-ignored)
├── .env.example          ← Template
├── requirements.txt
├── README.md
├── app/
│   ├── main.py           ← Streamlit UI
│   ├── chains.py         ← LangChain extraction + generation chains
│   └── portfolio.py      ← ChromaDB manager + custom embedder
└── data/
    └── portfolio.csv     ← Your projects (14 pre-loaded)
```

---

## 🔑 API Key Setup

Get a **free** Groq API key at [console.groq.com](https://console.groq.com) — no credit card needed.

**Option A (recommended) — .env file:**
```
GROQ_API_KEY=gsk_your_actual_key_here
```
The app loads it automatically. No typing it in the browser ever again.

**Option B — sidebar input:**
Just paste it in the sidebar each time you open the app.

---

## 📊 Portfolio CSV Format

Edit `data/portfolio.csv` to add your own projects:

| Tech Stack | Project Link | Project Title | Description |
|---|---|---|---|
| Python, YOLOv8, FastAPI | https://github.com/... | Vehicle Counting System | Multi-road vehicle tracking... |

The `Tech Stack` column drives ChromaDB matching — the more specific, the better the matches.

---

## 🎯 Included Portfolio Projects

| # | Project | Key Tech |
|---|---|---|
| 1 | AI Vehicle Counting & Traffic Analysis | YOLOv8, SORT, Optical Flow, FastAPI |
| 2 | License Plate Recognition (PaddleOCR) | YOLOv8, RealESRGAN, PaddleOCR |
| 3 | MPhil ALPR Thesis | DarkIR, HAT, RealESRGAN, EasyOCR, TrOCR |
| 4 | AI Resume Analyzer | LangChain, Groq, Streamlit |
| 5 | AI Cold Email Generator | LangChain, ChromaDB, Groq |
| 6 | Face Recognition Attendance | OpenCV, Deep Learning |
| 7 | Fire & Smoke Detection | TensorFlow, CNN |
| 8 | Video Caption Generation | LSTM, CNN |
| 9 | Image Captioning | ResNet-50, LSTM, Flickr8k |
| 10 | Optical Flow & Motion Segmentation | OpenCV, Scikit-learn |
| 11 | Human Activity Recognition | TensorFlow, Sensor Data |
| 12 | Feature Optimization (RFE) | Scikit-learn, XGBoost |
| 13 | Sign Language Classification | CNN, PyTorch |
| 14 | Transmission Tower Segmentation | Mask R-CNN, COCO |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM API | Groq (Llama 3.3 70B / Llama 3.1 8B / Mixtral / Gemma2) |
| NLP Pipeline | LangChain (chains, prompts, output parsers) |
| Vector DB | ChromaDB with custom hash embedder |
| UI | Streamlit |
| Data | Pandas + CSV |
| Config | python-dotenv |

---

## 💡 Usage Tips

- **Best results**: paste the full JD including responsibilities and requirements sections
- **Model choice**: `llama-3.3-70b` = best quality · `llama-3.1-8b` = fastest
- **Custom portfolio**: upload your own CSV via the sidebar file uploader
- **Download**: save generated emails as `.txt` with one click

---

## 📚 How to Test
- Load Portfolio: Click "Load Portfolio from CSV" button
- Paste Job Description: Copy any job description from LinkedIn or job portal
- Generate Email: Click "Generate Cold Email"
- Review: The AI will create a personalized email based on matching projects
  
---

## 👤 Author

**Tayyabah Rehman** · MPhil AI · University of the Punjab, Lahore  
[github.com/Tayyabah-Rehman](https://github.com/Tayyabah-Rehman)
