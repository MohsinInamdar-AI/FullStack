"""
app.py - Streamlit frontend for OpenAI powered image generation.
"""
import os
import uuid
from pathlib import Path

import streamlit as st

from db import init_db, add_generation, get_all_generations, delete_generation
from openai_client import generate_image, OpenAIImageError

IMAGES_DIR = Path(__file__).parent / "generated_images"
IMAGES_DIR.mkdir(exist_ok=True)

MODEL_OPTIONS = [
    "gpt-image-1",
    "dall-e-3",
    "dall-e-2",
]

SIZE_OPTIONS = [
    "1024x1024",
    "1024x1536",
    "1536x1024",
]

st.set_page_config(page_title="OpenAI Image Generator", page_icon="🎨", layout="wide")
init_db()

# --- Sidebar: settings ---
st.sidebar.title("⚙️ Settings")
api_key_input = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    value=os.environ.get("OPENAI_API_KEY", ""),
    help="Get a key at platform.openai.com/api-keys",
)
model_id = st.sidebar.selectbox("Model", MODEL_OPTIONS, index=0)
size = st.sidebar.selectbox("Image size", SIZE_OPTIONS, index=0)
st.sidebar.markdown("---")
st.sidebar.caption("Your API key is used only for this session and not stored.")

# --- Main layout ---
st.title("🎨 AI Image Generator")
st.caption("Streamlit frontend • OpenAI Images API • SQLite history")

tab_generate, tab_history = st.tabs(["Generate", "History"])

with tab_generate:
    col_input, col_output = st.columns([1, 1])

    with col_input:
        prompt = st.text_area("Prompt", placeholder="A watercolor painting of a mountain lake at sunrise", height=100)
        generate_btn = st.button("Generate Image", type="primary", use_container_width=True)

    with col_output:
        if generate_btn:
            if not api_key_input:
                st.error("Please provide an OpenAI API key in the sidebar.")
            elif not prompt.strip():
                st.error("Please enter a prompt.")
            else:
                with st.spinner(f"Generating with {model_id}..."):
                    try:
                        image = generate_image(
                            prompt=prompt,
                            model_id=model_id,
                            size=size,
                            api_key=api_key_input,
                        )
                        filename = f"{uuid.uuid4().hex}.png"
                        filepath = IMAGES_DIR / filename
                        image.save(filepath)

                        add_generation(
                            prompt=prompt,
                            negative_prompt="",
                            model_id=model_id,
                            image_path=str(filepath),
                        )

                        st.image(image, caption=prompt, use_container_width=True)
                        st.success("Image generated and saved to history.")
                    except OpenAIImageError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Unexpected error: {e}")
        else:
            st.info("Enter a prompt and click Generate to see your image here.")

with tab_history:
    st.subheader("Generation History")
    rows = get_all_generations(limit=100)

    if not rows:
        st.write("No generations yet.")
    else:
        for row in rows:
            with st.container(border=True):
                c1, c2 = st.columns([1, 3])
                with c1:
                    img_path = Path(row["image_path"])
                    if img_path.exists():
                        st.image(str(img_path), use_container_width=True)
                    else:
                        st.write("Image file missing")
                with c2:
                    st.write(f"**Prompt:** {row['prompt']}")
                    st.write(f"**Model:** {row['model_id']}")
                    st.write(f"**Created:** {row['created_at']}")
                    if st.button("Delete", key=f"del_{row['id']}"):
                        delete_generation(row["id"])
                        st.rerun()