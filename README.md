# JevRoute POC

A small Python + Streamlit proof of concept that uses TypeSafe Jev through OpenRouter to select the most appropriate tool for a natural-language request.

## What the POC demonstrates

The model is used only for routing:

User query -> Jev -> selected tool + confidence + probabilities -> mock tool execution

The actual tools are mocked because the project is focused on tool selection rather than tool implementation.

## Setup

### 1. Create a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the application

```powershell
streamlit run app.py
```

Or double-click `run.bat` after the environment is created and dependencies are installed.

## API key

The app lets each user enter an OpenRouter API key in the sidebar.

Create a key here:

https://openrouter.ai/settings/keys

For local development you can also:

1. Copy `.env.example` to `.env`
2. Add your own key:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Never commit your real `.env` file.

## Model

`typesafe/jev-1.13`

## Included tools

- Calculator
- Web Search
- Code Generator
- Code Debugger
- Database
- Summarizer
- Translation
- Email Writer
- Document Writer
- Data Analysis
- Chart Generator
- File Reader
- Image Analysis
- Research
- Planning
- Reasoning
- General LLM
- Human Review

## Notes

The UI intentionally uses native Streamlit components instead of custom HTML/CSS. This avoids the blank or black-screen rendering issue that can occur when malformed HTML or CSS is injected into Streamlit.
