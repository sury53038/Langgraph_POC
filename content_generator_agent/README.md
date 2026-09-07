# Content Generator AI Agent

A LangGraph-powered AI workflow that transforms raw content into polished, engaging, and localized output. The project uses a multi-stage pipeline to:

1. Clean and improve the raw input text
2. Convert it into a dynamic video-script style
3. Translate it into natural Hinglish for a more relatable audience

This project is built with Python, LangGraph, LangChain, Groq, and dotenv.

---

## Features

- Grammar and tone refinement
- Script generation for YouTube-style narration
- Hinglish localization for Indian audiences
- Sequential multi-step workflow using LangGraph
- Easy to extend for other content formats such as blogs, reels, or ads

---

## Tech Stack

- Python 3
- LangGraph
- LangChain
- Groq LLM
- python-dotenv

---

## Project Structure

```text
content_generator_agent/
├── app.py
├── nodes.py
├── states.py
├── requirements.txt
├── .env
└── .gitignore


Setup

1. Clone the project

git clone https://github.com/sury53038/Langgraph_POC.git
cd content_generator_agent

2. Create a virtual environment

python -m venv venv

On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate


3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root and add your Groq API key:

GROQ_API_KEY=your_api_key_here

5. Run the Project

python app.py