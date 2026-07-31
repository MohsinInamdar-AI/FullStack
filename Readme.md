
# AI Image Generator

Streamlit + OpenAI DALL-E (Images API) + SQLite.

## Setup

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```powershell
$env:OPENAI_API_KEY="sk-xxxxxxxxxxxx"
streamlit run app.py
```

Open http://localhost:8501, paste your OpenAI API key in the sidebar if not set via env var, enter a prompt, and click **Generate Image**. Past generations are saved in `generations.db` and shown under the **History** tab.
