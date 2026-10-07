import streamlit as st
from pathlib import Path
import tempfile
import time

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TAMPERGUARD AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# FORCE DARK AI THEME
# =========================================================

st.markdown("""
<style>

/* ================================
   MAIN APPLICATION
   ================================ */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 255, 255, 0.08), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(120, 0, 255, 0.10), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(0, 180, 255, 0.06), transparent 35%),
        #050816 !important;
    color: #e8f1ff !important;
}

/* Main content area */
.main {
    background: transparent !important;
}

/* Force text colors */
p, span, label, div {
    color: inherit;
}

h1, h2, h3, h4 {
    color: #f5f7ff !important;
}

/* ================================
   SIDEBAR
   ================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #080d1d 0%,
            #0a1024 50%,
            #050816 100%
        ) !important;

    border-right: 1px solid rgba(0, 255, 255, 0.18);
}

section[data-testid="stSidebar"] * {
    color: #dce8ff !important;
}

/* ================================
   HEADER
   ================================ */

header[data-testid="stHeader"] {
    background: rgba(5, 8, 22, 0.95) !important;
}

/* ================================
   TITLE
   ================================ */

.hero-title {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: 3px;
    margin-bottom: 4px;

    background: linear-gradient(
        90deg,
        #00f5ff,
        #7c4dff,
        #00ffb3
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #8fa8c9 !important;
    font-size: 18px;
    letter-spacing: 1px;
    margin-bottom: 25px;
}

/* ================================
   STATUS BAR
   ================================ */

.status-box {
    background: rgba(10, 20, 40, 0.8);
    border: 1px solid rgba(0, 255, 200, 0.25);
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(0, 255, 200, 0.06);
}

/* ================================
   CARDS
   ================================ */

.ai-card {
    background:
        linear-gradient(
            145deg,
            rgba(15, 25, 52, 0.95),
            rgba(7, 13, 30, 0.95)
        );

    border: 1px solid rgba(0, 220, 255, 0.18);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 20px;

    box-shadow:
        0 10px 40px rgba(0, 0, 0, 0.35),
        inset 0 0 30px rgba(0, 150, 255, 0.025);
}

/* ================================
   METRICS
   ================================ */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            rgba(14, 25, 52, 0.95),
            rgba(6, 12, 28, 0.95)
        );

    border: 1px solid rgba(0, 220, 255, 0.20);
    border-radius: 15px;
    padding: 18px;

    box-shadow: 0 0 25px rgba(0, 180, 255, 0.06);
}

div[data-testid="stMetricLabel"] {
    color: #8ea7c9 !important;
}

div[data-testid="stMetricValue"] {
    color: #00f5ff !important;
    font-weight: 800;
}

/* ================================
   UPLOADER
   ================================ */

section[data-testid="stFileUploader"] {
    background: rgba(9, 18, 40, 0.9) !important;
    border: 1px dashed rgba(0, 240, 255, 0.45) !important;
    border-radius: 16px !important;
    padding: 10px !important;
}

section[data-testid="stFileUploader"] * {
    color: #dce8ff !important;
}

/* ================================
   BUTTON
   ================================ */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(0, 255, 255, 0.55);

    background:
        linear-gradient(
            90deg,
            #006d77,
            #4934a8
        );

    color: white !important;
    font-weight: 800;
    letter-spacing: 1px;
    padding: 14px;

    box-shadow:
        0 0 20px rgba(0, 220, 255, 0.15);

    transition: 0.25s;
}

.stButton > button:hover {
    border-color: #00f5ff;

    box-shadow:
        0 0 30px rgba(0, 245, 255, 0.35);

    transform: translateY(-2px);
}

/* ================================
   PROGRESS BAR
   ================================ */

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(
        90deg,
        #00f5ff,
        #7c4dff,
        #00ffb3
    );
}

/* ================================
   TABS
   ================================ */

button[data-baseweb="tab"] {
    color: #91a7c6 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #00f5ff !important;
}

/* ================================
   EXPANDER
   ================================ */

details {
    background: rgba(8, 17, 38, 0.9) !important;
    border: 1px solid rgba(0, 220, 255, 0.16) !important;
    border-radius: 12px !important;
}

/* ================================
   ALERT BOXES
   ================================ */

div[data-testid="stAlert"] {
    background: rgba(10, 20, 40, 0.92) !important;
    border-radius: 14px;
}

/* ================================
   IMAGE
   ================================ */

img {
    border-radius: 14px;
}

/* ================================
   FOOTER
   ================================ */

.footer {
    text-align: center;
    color: #647895 !important;
    margin-top: 45px;
    padding: 25px;
    border-top: 1px solid rgba(100, 150, 200, 0.12);
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🛡️ TAMPERGUARD")

    st.markdown("---")

    st.markdown("### 🤖 AI SYSTEM")

    st.success("● AI ENGINE ONLINE")

    st.markdown("""
    **Detection Modules**

    🧠 CNN Classification  
    📊 Probability Analysis  
    🔍 Image Pattern Analysis  
    ⚡ AI Prediction Engine
    """)

    st.markdown("---")

    st.markdown("### 📡 SYSTEM STATUS")

    st.write("🟢 Model Loaded")
    st.write("🟢 AI Engine Ready")
    st.write("🟢 Prediction System Ready")

    st.markdown("---")

    st.caption("AI & ML Image Integrity System")
    st.caption("Academic Project")

# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="hero-title">🛡️ TAMPERGUARD AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    '⚡ Intelligent Image Tampering Detection System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status-box">🟢 <b>AI ENGINE ONLINE</b> '
    '&nbsp;&nbsp; | &nbsp;&nbsp; '
    'Neural Image Classification System Ready'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# DASHBOARD METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🤖 AI ENGINE", "ONLINE")

with col2:
    st.metric("🧠 MODEL", "CNN")

with col3:
    st.metric(
        "🔬 ANALYSES",
        st.session_state.analysis_count
    )

with col4:
    st.metric("⚡ STATUS", "READY")

st.markdown("")

# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown("## 📤 Upload Image")

st.markdown(
    '<div class="ai-card">',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose an image for AI analysis",
    type=["jpg", "jpeg", "png"],
    help="Upload a JPG, JPEG, or PNG image."
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# IMAGE PREVIEW
# =========================================================

if uploaded_file is not None:

    left, right = st.columns([1.4, 1])

    with left:

        st.markdown("### 🖼️ Image Preview")

        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True
        )

    with right:

        st.markdown("### 🧠 AI Analysis Engine")

        st.markdown("""
        **Active Detection Modules**

        ☑ CNN Image Classification  
        ☑ Probability Estimation  
        ☑ Pattern Recognition  
        ☑ Tampering Classification
        """)

        st.info(
            "The AI model will classify the image as "
            "**REAL** or **TAMPERED**."
        )

        detect = st.button(
            "⚡ START AI DETECTION",
            use_container_width=True
        )

    # =====================================================
    # DETECTION
    # =====================================================

    if detect:

        from src.predict import predict_tampering

        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_image_path = temp_file.name

        # Progress display
        progress = st.progress(0)

        status = st.empty()

        status.info("🔄 Loading image into AI engine...")
        progress.progress(20)
        time.sleep(0.4)

        status.info("🧠 Running neural network prediction...")
        progress.progress(50)
        time.sleep(0.4)

        status.info("📊 Calculating prediction probabilities...")
        progress.progress(75)
        time.sleep(0.4)

        # REAL MODEL PREDICTION
        result = predict_tampering(temp_image_path)

        progress.progress(100)
        status.success("✅ AI ANALYSIS COMPLETE")

        st.session_state.analysis_count += 1
        st.session_state.last_result = result

        time.sleep(0.5)

        # =================================================
        # RESULT
        # =================================================

        st.markdown("---")

        st.markdown("## 🎯 AI Detection Result")

        label = result["label"]
        confidence = result["confidence"] * 100
        probability = result["probability"] * 100

        if label == "TAMPERED":

            st.error(
                "🚨 TAMPERED IMAGE DETECTED"
            )

        else:

            st.success(
                "✅ IMAGE CLASSIFIED AS REAL"
            )

        # Result metrics
        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric(
                "Classification",
                label
            )

        with r2:
            st.metric(
                "AI Confidence",
                f"{confidence:.2f}%"
            )

        with r3:
            st.metric(
                "Tampering Probability",
                f"{probability:.2f}%"
            )

        # Probability bar
        st.markdown("### 📊 Tampering Probability")

        st.progress(
            min(max(probability / 100, 0), 1)
        )

        if probability >= 70:

            st.warning(
                f"⚠️ High tampering probability: "
                f"{probability:.2f}%"
            )

        elif probability >= 40:

            st.info(
                f"ℹ️ Moderate tampering probability: "
                f"{probability:.2f}%"
            )

        else:

            st.success(
                f"🟢 Low tampering probability: "
                f"{probability:.2f}%"
            )

        # =================================================
        # TECHNICAL DETAILS
        # =================================================

        with st.expander(
            "🔬 View AI Prediction Details"
        ):

            st.write(
                "**Model Classification:**",
                label
            )

            st.write(
                "**Confidence Score:**",
                f"{confidence:.2f}%"
            )

            st.write(
                "**Tampering Probability:**",
                f"{probability:.2f}%"
            )

            st.write(
                "**Input Image:**",
                uploaded_file.name
            )

            st.write(
                "**AI Engine:**",
                "CNN Image Classification Model"
            )

# =========================================================
# AI PIPELINE
# =========================================================

st.markdown("---")

st.markdown("## 🧠 AI Detection Pipeline")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.markdown("### 01")
    st.write("📤")
    st.write("Image Upload")

with p2:
    st.markdown("### 02")
    st.write("🧠")
    st.write("CNN Processing")

with p3:
    st.markdown("### 03")
    st.write("📊")
    st.write("Probability Analysis")

with p4:
    st.markdown("### 04")
    st.write("🎯")
    st.write("AI Classification")

# =========================================================
# PROJECT INFORMATION
# =========================================================

st.markdown("---")

tab1, tab2, tab3 = st.tabs(
    [
        "🤖 AI Architecture",
        "📊 Model Information",
        "🎓 Project Highlights"
    ]
)

with tab1:

    st.markdown("### 🤖 AI Architecture")

    st.write("""
    The system uses a trained deep-learning image
    classification model to identify whether an uploaded
    image is classified as REAL or TAMPERED.
    """)

    st.code("""
IMAGE
  ↓
PREPROCESSING
  ↓
CNN MODEL
  ↓
FEATURE EXTRACTION
  ↓
CLASSIFICATION
  ↓
PROBABILITY SCORE
  ↓
REAL / TAMPERED
""")

with tab2:

    st.markdown("### 📊 Model Information")

    st.write("**Model Type:** CNN")
    st.write("**Framework:** TensorFlow / Keras")
    st.write("**Task:** Binary Image Classification")
    st.write("**Output:** REAL / TAMPERED")
    st.write("**Prediction:** Confidence + Probability")

with tab3:

    st.markdown("### 🎓 Project Highlights")

    st.write("""
    • Artificial Intelligence  
    • Machine Learning  
    • Deep Learning  
    • Computer Vision  
    • Image Classification  
    • Probability-based Prediction  
    • Interactive Streamlit Interface
    """)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    '🛡️ TAMPERGUARD AI &nbsp;|&nbsp; '
    'AI & ML Image Tampering Detection System'
    '<br><br>'
    'Built for Academic Demonstration'
    '</div>',
    unsafe_allow_html=True
)