import streamlit as st
from openai import OpenAI

# -----------------------------
# PASSWORD PROTECTION
# -----------------------------
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔒 NanoComposites-GPT Access")
        password = st.text_input("Enter password", type="password")

        if st.button("Login"):
            if password == st.secrets["APP_PASSWORD"]:
                st.session_state.authenticated = True
                st.success("Access granted")
                st.rerun()
            else:
                st.error("Incorrect password")

        st.stop()

check_password()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="NanoComposites-GPT (Meta-Optics)",
    page_icon="🧪",
    layout="wide"
)

# -----------------------------
# OPENAI CLIENT
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# TITLE
# -----------------------------
st.title("🧪 NanoComposites-GPT for Meta-Optics")
st.caption(
    "AI assistant for UV-curable nanocomposite resists targeting high-index, low-loss meta-optics"
)

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Meta-Optics Material Design Inputs")

matrix = st.sidebar.selectbox(
    "UV-Curable Polymer Matrix",
    [
        "SU-8 (epoxy photoresist)",
        "DWL resist (epoxy/acrylate-based)",
        "Ormocer (organic–inorganic hybrid)"
    ]
)

filler = st.sidebar.selectbox(
    "High-Index Nanofiller",
    [
        "SiO₂ nanoparticles",
        "TiO₂ nanoparticles",
        "Amorphous silicon (a-Si) nanoparticles",
        "Crystalline silicon (c-Si) nanoparticles"
    ]
)

target_wavelength = st.sidebar.selectbox(
    "Target Spectral Regime",
    [
        "Visible (400–700 nm)",
        "Near-Infrared (700–1550 nm)"
    ]
)

target_properties = st.sidebar.multiselect(
    "Primary Optical Targets",
    [
        "Refractive index enhancement (n)",
        "Low absorption coefficient (k)"
    ],
    default=[
        "Refractive index enhancement (n)",
        "Low absorption coefficient (k)"
    ]
)

fabrication = st.sidebar.selectbox(
    "Fabrication Route (Fixed)",
    [
        "UV lithography (405 nm) + post-exposure curing",
        "Direct-write lithography (DWL) + post-exposure curing"
    ]
)

constraints = st.sidebar.text_area(
    "Experimental Constraints (optional)",
    "Max exposure wavelength, available UV source, bake temperature limits, cleanroom access..."
)

# -----------------------------
# PROMPT GENERATION
# -----------------------------
if st.button("🔬 Generate Nanocomposite Recipes"):

    system_prompt = """
    You are a materials scientist specializing in UV-curable nanocomposite
    photoresists for meta-optics and dielectric metasurfaces.

    Focus exclusively on:
    - SU-8, DWL resists, and Ormocer matrices
    - UV exposure followed by post-exposure curing
    - High-index, low-loss nanocomposites for visible and near-infrared optics

    Prioritize refractive index (n) and absorption coefficient (k).
    Ensure all recipes are realistic, lab-feasible, and suitable for
    lithographic patterning.

    Avoid unsafe materials and non-UV curing routes.
    Reference relevant peer-reviewed literature wherever possible.
    Use SI units.
    """

    user_prompt = f"""
    Propose experimentally viable nanocomposite recipes for meta-optics
    fabrication with the following specifications:

    Polymer matrix: {matrix}
    Nanofiller: {filler}
    Target spectral regime: {target_wavelength}
    Fabrication route: {fabrication}
    Constraints: {constraints}

    For each recipe, provide:

    1. Nanocomposite formulation
       - Filler type and particle size range
       - Recommended loading (wt% or vol%)
       - Dispersion strategy
       - Silanisation parameters (pH, temperature, stirring time, sonication details)

    2. UV-based fabrication process
       - Film deposition method
       - Exposure considerations
       - Post-exposure curing steps

    3. Expected optical performance
       - Refractive index trend (n)
       - Absorption/loss behavior (k)
       - Impact on meta-atom height and aspect ratio

    4. Known risks and mitigation strategies
       - UV penetration
       - Scattering
       - Lithographic fidelity

    5. Literature validation
       - Check in this google drive link: https://drive.google.com/drive/folders/1VW9t-jcBQa7rdYN4lFXhUURwZr4bOIWe?usp=sharing and list two references for it which matches closely

    Present the output as a clear, step-by-step experimental recipe
    suitable for immediate laboratory testing.
    """

    with st.spinner("Designing UV-curable nanocomposite recipes for meta-optics..."):
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.25
        )

    st.subheader("📄 Nanocomposite Meta-Optics Recipes")
    st.markdown(response.choices[0].message.content)
