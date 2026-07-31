
# AI Image Generator (Streamlit + Hugging Face + SQLite)

Generate images from text prompts using Hugging Face's Inference API, with a
Streamlit UI and a SQLite database that stores your generation history.

## Project structure

```
hf_image_gen/
├── app.py              # Streamlit frontend (main entry point)
├── hf_client.py         # Hugging Face Inference API wrapper
├── db.py                 # SQLite database layer
├── requirements.txt
├── generated_images/     # Saved output images (created automatically)
└── generations.db        # SQLite database (created automatically)
```

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Get a free Hugging Face API token:

   - Sign up at https://huggingface.co
   - Go to https://huggingface.co/settings/tokens and create a token (Read access is enough)
3. (Optional) Set it as an environment variable so it's pre-filled in the app:

   ```bash
   export HF_API_TOKEN=hf_xxxxxxxxxxxx   # Windows: set HF_API_TOKEN=hf_xxx
   ```

   You can also just paste it into the sidebar each time you run the app.

## Run

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## How it works

- **Frontend (`app.py`)**: Streamlit UI with a "Generate" tab (prompt input,
  model picker, image display) and a "History" tab (past generations pulled
  from SQLite, with delete support).
- **Hugging Face client (`hf_client.py`)**: Sends the prompt to the HF
  Inference API (`https://api-inference.huggingface.co/models/{model_id}`)
  and decodes the returned image bytes into a PIL Image. Handles the "model
  is loading" (503) case and other API errors.
- **Database (`db.py`)**: A single `generations` table storing prompt,
  negative prompt, model used, saved image path, and timestamp. Images
  themselves are saved to disk under `generated_images/`; the DB just tracks
  metadata + file path.

## Notes / things you may want to extend

- Swap the model dropdown for any text-to-image model on the HF Hub (some
  require a Pro/Inference Endpoints plan for fast responses).
- Add pagination to the History tab if it grows large.
- Add user accounts if you want per-user history instead of a single shared DB.
- For production use, consider moving off the free Inference API to a
  dedicated Inference Endpoint for reliability/speed, and store the API
  token in Streamlit secrets (`st.secrets`) instead of the sidebar input.
