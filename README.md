# 🤖 Agentic Recruiter Bot #

An intelligent, voice-based AI recruiter powered by Mistral LLM, Fast Whisper STT, and gTTS TTS — designed to simulate job interviews, ask personalized questions, evaluate responses, and generate a professional interview report.


## 📁 Project Structure


## 🚀 Features

- 🎤 **Voice-Based Interviewing**  
  Transcribe candidate responses via Fast Whisper and respond using gTTS.

- 🧠 **LLM-Powered Evaluation**  
  Use Mistral to generate smart, personalized questions and evaluate answers with scoring and follow-ups.

- 📄 **Automated PDF Report**  
  Each response is summarized, scored, and compiled into a structured PDF.

- ⚠️ **Edge Case Detection**  
  Detects short, uncertain, or empty responses and asks for clarification.

- 🔗 **Mock Zoom Integration**  
  Simulates scheduling and joining a Zoom call via the browser.

---

## ⚙️ Setup Instructions

### 🧪 Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔐 Set Up Environment Variables

Create a `.env` file in the root directory with the following:

```ini
MISTRAL_API_KEY=your_mistral_api_key_here
```

---

### ▶️ Run the Application

```bash
python main.py
```

---

## 📚 Requirements

- `faster-whisper`
- `gTTS`
- `speechrecognition`
- `fpdf`
- `python-dotenv`
- `mistralai`
- `platform` 
- `tempfile` 

✅ All dependencies are listed in `requirements.txt`

---

## 📄 Sample Output

A sample interview report is saved as `interview_report.pdf` once the session ends.  
It includes:

- The interview questions  
- Candidate answers  
- Scores and comments  
- Summaries for each response  

---

## 🛠️ Future Improvements

- Integrate real Zoom API for meeting scheduling  
- Parse resumes from PDF/DOCX (not just `.txt`)  
- Add a web dashboard with Flask or Streamlit  
- Enable long-term candidate profiling or CRM integrations  

---


