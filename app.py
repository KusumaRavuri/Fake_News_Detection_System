import streamlit as st
import time
import random
import pickle
import re

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TruthLens · Fake News Detector",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- imports ---------- */
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

/* ---------- reset / base ---------- */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #0a0a0f !important;
    color: #e8e6e1 !important;
    font-family: 'Syne', sans-serif;
}

/* hide streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"]          { display: none !important; }
[data-testid="stSidebar"]             { display: none !important; }

/* main container */
.block-container {
    max-width: 780px !important;
    padding: 1rem 2rem 2rem !important;
}

/* ---------- hero ---------- */
.hero {
    text-align: center;
    padding: 1.5rem 0 1rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #5de0a0;
    border: 1px solid #5de0a020;
    background: #5de0a008;
    padding: 0.35rem 0.9rem;
    border-radius: 2px;
    margin-bottom: 1.6rem;
}
.hero h1 {
    font-size: clamp(2.4rem, 6vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #f0ede8;
    margin-bottom: 1rem;
}
.hero h1 span { color: #5de0a0; }
.hero p {
    font-size: 0.95rem;
    color: #6b6b7a;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.02em;
    max-width: 420px;
    margin: 0 auto;
}

/* ---------- divider ---------- */
.rule {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a3a, transparent);
    margin: 2.5rem 0;
}

/* ---------- label ---------- */
.field-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5de0a0;
    margin-bottom: 0.6rem;
    display: block;
}

/* ---------- text area ---------- */
textarea {
    background: #111118 !important;
    border: 1px solid #222230 !important;
    border-radius: 4px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    caret-color: #5de0a0 !important;
    resize: vertical !important;
    transition: border-color 0.2s ease !important;
}
textarea:focus {
    border-color: #5de0a050 !important;
    box-shadow: 0 0 0 3px #5de0a008 !important;
    outline: none !important;
}
textarea::placeholder { color: #33334a !important; }

/* ---------- text input ---------- */
input[type="text"] {
    background: #111118 !important;
    border: 1px solid #222230 !important;
    border-radius: 4px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s ease !important;
}
input[type="text"]:focus {
    border-color: #5de0a050 !important;
    box-shadow: 0 0 0 3px #5de0a008 !important;
    outline: none !important;
}

/* ---------- button ---------- */
.stButton > button {
    background: #5de0a0 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    padding: 0.75rem 2.2rem !important;
    cursor: pointer !important;
    transition: opacity 0.15s ease, transform 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ---------- result cards ---------- */
.verdict-card {
    border-radius: 5px;
    padding: 2rem 2rem 1.6rem;
    margin-top: 2rem;
    position: relative;
    overflow: hidden;
}
.verdict-real {
    background: #0d1f18;
    border: 1px solid #5de0a030;
}
.verdict-fake {
    background: #1f0d0d;
    border: 1px solid #e05d5d30;
}
.verdict-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.label-real    { color: #5de0a0; }
.label-fake    { color: #e05d5d; }

.verdict-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 1.2rem;
}
.title-real    { color: #5de0a0; }
.title-fake    { color: #e05d5d; }

.confidence-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.2rem;
}
.conf-bar-track {
    flex: 1;
    height: 4px;
    background: #1e1e2a;
    border-radius: 2px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.8s cubic-bezier(.16,1,.3,1);
}
.fill-real    { background: #5de0a0; }
.fill-fake    { background: #e05d5d; }

.conf-pct {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    min-width: 42px;
    text-align: right;
}



/* ---------- stats row ---------- */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin: 2.5rem 0 0;
}
.stat-card {
    background: #111118;
    border: 1px solid #1c1c28;
    border-radius: 4px;
    padding: 1.1rem;
    text-align: center;
}
.stat-num {
    font-size: 1.7rem;
    font-weight: 800;
    color: #5de0a0;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #44444e;
}

/* ---------- footer ---------- */
.footer {
    text-align: center;
    margin-top: 5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    color: #2a2a3a;
}

/* ---------- spinner override ---------- */
[data-testid="stSpinner"] > div {
    border-color: #5de0a040 !important;
    border-top-color: #5de0a0 !important;
}

/* ---------- selectbox ---------- */
[data-testid="stSelectbox"] > div > div {
    background: #111118 !important;
    border: 1px solid #222230 !important;
    color: #e8e6e1 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    border-radius: 4px !important;
}

/* tabs */
[data-testid="stTabs"] button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #44444e !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #5de0a0 !important;
    border-bottom-color: #5de0a0 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def analyze_news(text: str) -> dict:
    # Clean text (same as training)
    cleaned = text.lower()
    cleaned = re.sub(r'[^a-zA-Z ]', '', cleaned)

    # Transform
    vector = vectorizer.transform([cleaned])

    # Predict
    prediction = model.predict(vector)[0]
    prob = model.predict_proba(vector)[0]

    confidence = max(prob) * 100

    if prediction == 1:
        verdict = "REAL"
        summary = "The content appears to be legitimate based on learned patterns."
    else:
        verdict = "FAKE"
        summary = "The content shows patterns similar to misinformation."

    return {
        "verdict": verdict,
        "confidence": confidence,
        "summary": summary,
        "word_count": len(text.split()),
    }

def verdict_classes(v):
    m = {
        "REAL":      ("verdict-real",      "label-real",      "title-real",      "fill-real",      "#5de0a0"),
        "FAKE":      ("verdict-fake",      "label-fake",      "title-fake",      "fill-fake",      "#e05d5d"),
    }
    return m.get(v, m["FAKE"])

# ── UI ────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered · Real-time Analysis</div>
    <h1>Truth<span>Lens</span></h1>
    <p>Paste any article, headline, or claim. We'll tell you if it checks out.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

# ── Input tabs
tab_text, tab_url = st.tabs(["  PASTE TEXT  ", "  ENTER URL  "])

with tab_text:
    st.markdown('<span class="field-label">Article / Claim</span>', unsafe_allow_html=True)
    user_input = st.text_area(
        label="",
        placeholder="Paste the article text, headline, or claim you want to verify…",
        height=200,
        label_visibility="collapsed",
        key="text_input",
    )

with tab_url:
    st.markdown('<span class="field-label">Article URL</span>', unsafe_allow_html=True)
    url_input = st.text_input(
        label="",
        placeholder="https://example.com/article",
        label_visibility="collapsed",
        key="url_input",
    )
    if url_input:
        user_input = f"[URL submitted: {url_input}] — simulating content fetch for demo purposes."

st.markdown("<br>", unsafe_allow_html=True)

# ── Analyse button
analyze_clicked = st.button("⟶  Analyse Now")

# ── Result
if analyze_clicked:
    text_to_check = user_input.strip() if user_input else ""

    if not text_to_check:
        st.warning("Please paste some text or enter a URL first.")
    else:
        with st.spinner("Running analysis…"):
            result = analyze_news(text_to_check)

        v = result["verdict"]
        conf = result["confidence"]
        card_cls, lbl_cls, title_cls, fill_cls, accent = verdict_classes(v)

        icons = {"REAL": "✓", "FAKE": "✗"}


        st.markdown(f"""
        <div class="verdict-card {card_cls}">
            <div class="verdict-label {lbl_cls}">Verdict</div>
            <div class="verdict-title {title_cls}">{icons[v]} {v}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.8rem;color:#6b6b7a;margin-bottom:1rem;line-height:1.6;">
                {result["summary"]}
            </div>
            <div class="confidence-row">
                <span class="field-label" style="margin:0;white-space:nowrap;">Confidence</span>
                <div class="conf-bar-track">
                    <div class="conf-bar-fill {fill_cls}" style="width:{conf:.0f}%"></div>
                </div>
                <span class="conf-pct" style="color:{accent}">{conf:.0f}%</span>
            </div>

        </div>
        """, unsafe_allow_html=True)

        # word count note
        st.markdown(f"""
        <div style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#33334a;
                    text-align:right;margin-top:0.6rem;letter-spacing:0.08em;">
            {result["word_count"]} words analysed
        </div>
        """, unsafe_allow_html=True)
