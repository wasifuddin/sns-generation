import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io
import base64
import os
import re


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Page Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="SNS AI Creator",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Custom CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
}

/* ── Dark background ─────────────────────────────────── */
.stApp {
    background: linear-gradient(145deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%);
}

/* ── Hero header ─────────────────────────────────────── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-wrap h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: .3rem;
}
.hero-wrap p {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 400;
}

/* ── Section headers ─────────────────────────────────── */
.section-hdr {
    color: #e2e8f0;
    font-weight: 700;
    font-size: 1.15rem;
    margin-bottom: .4rem;
}

/* ── Caption card ────────────────────────────────────── */
.caption-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(12px);
    transition: transform .2s, border-color .2s;
}
.caption-card:hover {
    transform: translateY(-2px);
    border-color: rgba(167,139,250,0.4);
}
.caption-card .card-label {
    font-size: .75rem;
    font-weight: 700;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: .5rem;
}
.caption-card .card-text {
    color: #e2e8f0;
    font-size: .97rem;
    line-height: 1.65;
}

/* ── Style pills ─────────────────────────────────────── */
.pill-grid {
    display: flex;
    flex-wrap: wrap;
    gap: .55rem;
    margin-bottom: .75rem;
}
.pill {
    padding: .45rem 1rem;
    border-radius: 999px;
    font-size: .82rem;
    font-weight: 600;
    border: 1.5px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.05);
    color: #cbd5e1;
    cursor: pointer;
    transition: all .2s;
    user-select: none;
}
.pill:hover {
    border-color: #a78bfa;
    color: #fff;
}
.pill.active {
    background: linear-gradient(135deg, #7c3aed, #6366f1);
    border-color: transparent;
    color: #fff;
}

/* ── Buttons ─────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: .7rem 1.5rem !important;
    transition: opacity .2s, transform .15s !important;
}
.stButton > button:hover {
    opacity: .9 !important;
    transform: translateY(-1px) !important;
}

/* ── Download button ─────────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669, #10b981) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

/* ── Tabs ─────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: .5rem;
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: .35rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #94a3b8;
    font-weight: 600;
    padding: .6rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
    color: #fff !important;
}

/* ── File uploader ───────────────────────────────────── */
.stFileUploader {
    border: 2px dashed rgba(167,139,250,0.35) !important;
    border-radius: 14px !important;
}

/* ── Image container ─────────────────────────────────── */
.gen-image-wrap {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
    margin: 1rem 0;
}
.gen-image-wrap img {
    width: 100%;
    display: block;
}

/* ── Sidebar ─────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #111827;
}

/* ── Word count badge ────────────────────────────────── */
.wc-badge {
    display: inline-block;
    font-size: .78rem;
    font-weight: 600;
    padding: .2rem .65rem;
    border-radius: 999px;
    margin-top: .3rem;
}
.wc-ok { background: rgba(52,211,153,0.15); color: #34d399; }
.wc-over { background: rgba(248,113,113,0.15); color: #f87171; }
</style>
""",
    unsafe_allow_html=True,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Helper Functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def get_api_key() -> str | None:
    """Return the Gemini API key from sidebar, env var, or Streamlit secrets."""
    if st.session_state.get("api_key_input"):
        return st.session_state["api_key_input"]
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


def count_words(text: str) -> int:
    return len(text.split()) if text.strip() else 0


def parse_captions(raw: str) -> list[str]:
    """Extract exactly 3 captions from the model response."""
    # Pattern: CAPTION 1: …
    matches = re.findall(
        r"CAPTION\s*\d+\s*[:\-]\s*(.*?)(?=CAPTION\s*\d+|$)",
        raw,
        re.DOTALL | re.IGNORECASE,
    )
    captions = [m.strip().strip('"').strip("'") for m in matches if m.strip()]
    if len(captions) >= 3:
        return captions[:3]

    # Fallback – numbered list
    matches = re.findall(r"(?:^|\n)\s*\d+[\.\)]\s*(.*?)(?=\n\s*\d+[\.\)]|$)", raw, re.DOTALL)
    captions = [m.strip().strip('"').strip("'") for m in matches if m.strip()]
    if len(captions) >= 3:
        return captions[:3]

    # Fallback – double‑newline split
    parts = [p.strip() for p in raw.split("\n\n") if p.strip()]
    if len(parts) >= 3:
        return parts[:3]

    return [raw.strip()]


def generate_captions(client, image_bytes: bytes, mime_type: str, context: str, length: str) -> list[str]:
    """Call Gemini to produce 3 caption suggestions."""
    length_guide = {
        "Short": "a very brief, catchy, 1-line caption (max ~15 words).",
        "Medium": "a balanced, expressive 2-3 line caption (~30-50 words).",
        "Long": "a detailed, emotional / storytelling caption (~60-100 words, not overly long).",
    }
    ctx_line = f"Additional context from the user: {context}" if context.strip() else "No extra context."

    prompt = (
        "You are a creative social media content writer.\n"
        "Analyze the uploaded image and generate exactly 3 different caption suggestions "
        "for SNS / social media platforms (Instagram, Facebook, LinkedIn, etc.).\n\n"
        f"Caption style: {length_guide[length]}\n"
        f"{ctx_line}\n\n"
        "Rules:\n"
        "- Sound natural, engaging, human-written.\n"
        "- Avoid robotic or overly formal language.\n"
        "- Use relevant emojis where appropriate.\n"
        "- Each caption must be unique with a different tone or angle.\n"
        "- Do NOT include hashtags unless they fit very naturally.\n\n"
        "Format your response EXACTLY like this:\n\n"
        "CAPTION 1:\n[first caption]\n\n"
        "CAPTION 2:\n[second caption]\n\n"
        "CAPTION 3:\n[third caption]"
    )

    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[prompt, image_part],
    )
    return parse_captions(response.text)


def generate_image_from_prompt(client, user_prompt: str, style: str) -> bytes:
    """Call Imagen via the Gemini API to generate an image."""
    style_detail = {
        "Realistic": "highly realistic, natural lighting, photorealistic textures, professional photography",
        "Meme": "meme-style, humorous composition, bold expressive visuals, internet culture aesthetic",
        "Cartoon": "cartoon illustration, vibrant colors, clean outlines, playful 2D art",
        "Anime": "anime art style, Japanese animation aesthetic, manga-inspired, vibrant palette",
        "Cinematic": "cinematic composition, dramatic lighting, moody film-like atmosphere, widescreen",
        "Product Photo": "professional product photography, clean white background, studio lighting, sharp focus",
        "Digital Art": "digital art, creative illustration, modern artistic rendering, high detail",
        "Minimalist": "minimalist design, clean composition, limited color palette, elegant negative space",
        "Poster": "poster design, bold graphic composition, eye-catching layout, promotional quality",
        "Social Media Banner": "social media banner, wide format, engaging visual, modern branding style",
    }

    final_prompt = (
        f"Create a {style_detail[style]} social media image of: {user_prompt}. "
        "High resolution, professional composition, highly detailed, visually stunning, "
        "suitable for an SNS/social media post, high-quality output."
    )

    response = client.models.generate_images(
        model="imagen-3.0-fast-generate-001",
        prompt=final_prompt,
        config=types.GenerateImagesConfig(number_of_images=1),
    )
    return response.generated_images[0].image.image_bytes


def render_caption_card(idx: int, text: str):
    """Display a single caption inside a styled card with a copy button."""
    st.markdown(
        f"""
        <div class="caption-card">
            <div class="card-label">Caption {idx}</div>
            <div class="card-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.code(text, language=None)



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Header
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(
    '<div class="hero-wrap">'
    "<h1>✨ SNS AI Creator</h1>"
    "<p>Create stunning social media captions &amp; images powered by AI</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API key gate
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
api_key = get_api_key()
if not api_key:
    st.info("👈 Enter your **Gemini API key** in `.streamlit/secrets.toml` to get started.")
    st.stop()

client = genai.Client(api_key=api_key)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Tabs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_caption, tab_image = st.tabs(["📝 Generate Caption", "🎨 Generate Image"])

# ── Tab 1 : Caption Generator ───────────────────────────────────
with tab_caption:
    st.markdown('<p class="section-hdr">📸 Upload an Image</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG",
    )

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Image Preview", width="stretch")

        st.markdown('<p class="section-hdr">✏️ Add Context (Optional)</p>', unsafe_allow_html=True)
        context = st.text_area(
            "Describe the mood, occasion, or any details",
            placeholder="e.g., Weekend getaway with friends, celebrating success…",
            max_chars=350,
            key="ctx_box",
        )
        wc = count_words(context)
        if wc > 50:
            st.markdown(
                f'<span class="wc-badge wc-over">⚠️ {wc}/50 words – too long</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<span class="wc-badge wc-ok">📝 {wc}/50 words</span>',
                unsafe_allow_html=True,
            )

        st.markdown('<p class="section-hdr">📏 Caption Length</p>', unsafe_allow_html=True)
        length = st.radio(
            "Choose caption style",
            ["Short", "Medium", "Long"],
            horizontal=True,
            help="Short = 1 line • Medium = 2-3 lines • Long = storytelling",
        )

        if st.button("✨ Generate Captions", width="stretch", type="primary", key="btn_cap"):
            if wc > 50:
                st.error("Please reduce your context to 50 words or fewer.")
            else:
                with st.spinner("🎨 Crafting your captions…"):
                    try:
                        img_bytes = uploaded.getvalue()
                        mime = uploaded.type or "image/jpeg"
                        captions = generate_captions(client, img_bytes, mime, context, length)
                        st.success("Here are your captions!")
                        for i, cap in enumerate(captions, 1):
                            render_caption_card(i, cap)
                    except Exception as exc:
                        st.error(f"Something went wrong: {exc}")
    else:
        st.info("Upload an image above to get started.")

# ── Tab 2 : Image Generator ─────────────────────────────────────
STYLES = [
    "Realistic",
    "Meme",
    "Cartoon",
    "Anime",
    "Cinematic",
    "Product Photo",
    "Digital Art",
    "Minimalist",
    "Poster",
    "Social Media Banner",
]

with tab_image:
    st.markdown('<p class="section-hdr">💬 Describe Your Image</p>', unsafe_allow_html=True)
    img_prompt = st.text_area(
        "What image do you want to create?",
        placeholder="e.g., A young entrepreneur working late at night on a laptop…",
        key="img_prompt_box",
    )

    st.markdown('<p class="section-hdr">🎭 Choose a Style</p>', unsafe_allow_html=True)

    if "selected_style" not in st.session_state:
        st.session_state.selected_style = "Realistic"

    cols = st.columns(5)
    for idx, style in enumerate(STYLES):
        col = cols[idx % 5]
        is_selected = st.session_state.selected_style == style
        if col.button(
            f"{'✅ ' if is_selected else ''}{style}",
            key=f"style_{style}",
            width="stretch",
        ):
            st.session_state.selected_style = style
            st.rerun()

    st.caption(f"Selected style: **{st.session_state.selected_style}**")

    if st.button("🖼️ Generate Image", width="stretch", type="primary", key="btn_img"):
        if not img_prompt.strip():
            st.error("Please describe the image you want to generate.")
        else:
            with st.spinner("🎨 Generating your image… this may take a moment"):
                try:
                    img_data = generate_image_from_prompt(
                        client, img_prompt, st.session_state.selected_style
                    )
                    st.success("Your image is ready!")
                    st.image(img_data, caption="Generated Image", width="stretch")
                    st.download_button(
                        label="⬇️ Download Image",
                        data=img_data,
                        file_name="sns_ai_generated.png",
                        mime="image/png",
                        width="stretch",
                    )
                except Exception as exc:
                    st.error(f"Image generation failed: {exc}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Footer
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#64748b;font-size:.82rem;">'
    "Built with ❤️ using Streamlit &amp; Google Gemini"
    "</p>",
    unsafe_allow_html=True,
)
