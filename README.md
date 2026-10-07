# voice-to-insight-assistant

A local-first audio/video intelligence tool that transcribes English, Hindi, and Hinglish content from meetings, lectures, tutorials, or any video, then generates summaries, action items, key decisions, and open questions, and lets you chat with the content using RAG + ChromaDB.

## ✨ Features

- **Multi-language transcription**
  - English meetings: transcribed using local Whisper AI
  - Hindi & Hinglish meetings: transcribed using Sarvam AI
- **Meeting intelligence**
  - Bullet-point summary of the full video
  - Action items with owner and deadline
  - Key decisions made in the meeting
  - Open questions and follow-ups
- **Chat with your meeting**
  - RAG-powered Q&A over your meeting transcript and summary
  - Vector database: ChromaDB
  - Embeddings: HuggingFace

## 🛠️ Tech Stack

- **Language**: Python
- **Transcription**
  - OpenAI Whisper for English (local)
  - Sarvam AI for Hindi/Hinglish
- **LLM & Orchestration**
  - LangChain LCEL 
  - Mistral AI for summarization, extraction, and chat
- **RAG**
  - ChromaDB 
  - HuggingFace Embeddings

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/Shreshhthh/voice-to-insight-assistant.git
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

3. **Install dependencies**

```bash
pip install -r Requirements.txt
```

## 🔑 API Keys

You’ll need free API keys from:

- **Mistral AI**: https://console.mistral.ai
- **Sarvam AI**: https://dashboard.sarvam.ai

Set them as environment variables:

```bash
MISTRAL_API_KEY="your_mistral_api_key"
SARVAM_API_KEY="your_sarvam_api_key"
```

## 🚀 Usage

Run the command:

```bash
python main.py
```

working steps:

1. Paste a **YouTube URL** or upload an **audio/video file**.
2. Select the audio/video language:
   - English → Whisper (local)
   - Hindi/Hinglish → Sarvam AI
3. View:
   - Summary
   - Action items (with owner & deadline)
   - Key decisions
   - Open questions / follow-ups
4. Chat to ask questions from Audio/Video (RAG over transcript + summary).

## 📁 Project Structure (typical)

```text
AI-Video-Assistant-/
├─ main.py             # Main orchestration / entry point
├─ test.py             # Simple tests / sanity checks
├─ Requirements.txt    # Dependencies
├─ core/
│  ├─ transcriber.py # Whisper + Sarvam wrappers
│  ├─ summarizer.py    # LangChain + Mistral pipelines
│  ├─ extractor.py     # Action items, decisions, questions
│  ├─ rag_engine.py           # RAG pipeline (retrieval + generation)
│  └─ vector_store.py  # ChromaDB setup, indexing, and utilities
└─ utils/
   └─ audio_processor.py        # process audio/video and youtube download
```

## 🧪 Example Workflow

1. Upload a 30-minute team standup recording (Hinglish).
2. Tool transcribes via Sarvam AI.
3. Mistral AI generates:
   - 8–12 bullet summary
   - 3–5 action items with owners and deadlines
   - 2–4 key decisions
   - 2–3 open questions
4. You ask in chat:
   - “What did we decide about the API redesign?”
   - “Who is responsible for the dashboard and what’s the deadline?”

## 📝 Notes

- Whisper runs locally, so large models may need:
  - Sufficient RAM (8–16 GB recommended)
  - First run may download model weights
