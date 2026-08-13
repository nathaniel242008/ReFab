import streamlit as st
from PIL import Image

from decision_engine import get_treatment
from treatment_data import TREATMENTS, PATHWAYS, PRIORITY_ORDER
from image_classifier import classify_material
from condition_classifier import classify_condition


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="ReFab",
    page_icon="♻️",
    layout="wide"
)


# -----------------------------
# SESSION STATE (keeps counts while the app is open)
# -----------------------------

if "stats" not in st.session_state:
    st.session_state.stats = {t["stream"]: 0 for t in TREATMENTS.values()}

if "history" not in st.session_state:
    st.session_state.history = []


def record_result(material, condition, confidence, treatment):
    st.session_state.stats[treatment["stream"]] += 1
    st.session_state.history.insert(0, {
        "Material": material,
        "Condition": condition,
        "Confidence": f"{confidence}%",
        "Pathway": treatment["name"],
        "Stream": treatment["stream"],
    })
    st.session_state.history = st.session_state.history[:15]


# -----------------------------
# TITLE
# -----------------------------

st.title("♻️ ReFab")
st.subheader("AI-Powered Fast-Fashion Waste Recovery")
st.write(
    "ReFab identifies discarded garments, assesses their condition, "
    "and recommends the most appropriate recovery pathway."
)
st.divider()


tab_dashboard, tab_analyze, tab_facility = st.tabs(
    ["🏠 Dashboard", "📷 Analyze Garment", "🏭 Virtual Facility"]
)


# =====================================================
# TAB 1 -- DASHBOARD
# =====================================================
with tab_dashboard:

    st.header("Current Batch")

    total = sum(st.session_state.stats.values())
    st.metric("Garments Analyzed This Session", total)

    cols = st.columns(len(PRIORITY_ORDER))
    for col, stream in zip(cols, PRIORITY_ORDER):
        with col:
            st.metric(stream.title(), st.session_state.stats[stream])

    st.divider()

    st.subheader("Recovery Priority")
    st.write(
        "ReFab always tries options higher on this list first, "
        "because they require the least processing:"
    )
    for i, stream in enumerate(PRIORITY_ORDER, start=1):
        st.write(f"{i}. **{stream.title()}**")

    st.divider()
    st.info(
        "Go to the **Analyze Garment** tab to upload a photo, then check "
        "**Virtual Facility** to see it routed and the stats update live."
    )


# =====================================================
# TAB 2 -- ANALYZE
# =====================================================
with tab_analyze:

    st.header("1. Upload a Garment")
    st.caption(
        "No real photo handy? Run `python generate_sample_images.py` once "
        "in your terminal, then upload a file from the /images folder."
    )

    uploaded_file = st.file_uploader(
        "Upload an image of a garment",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Uploaded garment", use_container_width=True)

        # Run the simulated AI automatically
        auto_material, auto_material_conf, features = classify_material(image)
        auto_condition, auto_condition_conf = classify_condition(image)
        overall_confidence = int((auto_material_conf + auto_condition_conf) / 2)

        with col2:
            st.subheader("AI Analysis (automatic)")
            st.metric("Detected Material", auto_material, f"{auto_material_conf}% confidence")
            st.metric("Detected Condition", auto_condition, f"{auto_condition_conf}% confidence")
            with st.expander("Raw image features used"):
                st.json(features)

        st.divider()

        with st.expander("🔧 Override / adjust before analyzing (optional)"):
            st.caption(
                "Use this to correct the AI, or to deliberately demo edge "
                "cases like a low-confidence 'manual review' result."
            )
            material = st.selectbox(
                "Material",
                ["Cotton", "Polyester", "Nylon", "Linen", "Mixed", "Acrylic", "Unknown"],
                index=["Cotton", "Polyester", "Nylon", "Linen", "Mixed", "Acrylic", "Unknown"].index(auto_material)
            )
            condition = st.selectbox(
                "Condition",
                ["Good", "Damaged"],
                index=["Good", "Damaged"].index(auto_condition)
            )
            confidence = st.slider("Confidence", 0, 100, overall_confidence)

        st.header("2. Run ReFab")

        if st.button("🔍 Analyze Garment", use_container_width=True, type="primary"):

            treatment_key = None
            treatment = get_treatment(material, condition, confidence)
            # figure out which key this treatment came from, for the pathway lookup
            for key, val in TREATMENTS.items():
                if val is treatment:
                    treatment_key = key
                    break

            record_result(material, condition, confidence, treatment)

            st.divider()
            st.header("3. ReFab Result")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Material", material)
            with c2:
                st.metric("Condition", condition)
            with c3:
                st.metric("Confidence", f"{confidence}%")

            if confidence < 70:
                st.warning("⚠️ Low-confidence classification -> routed to Manual Review to avoid contaminating a recycling stream.")
            else:
                st.success(f"Recommended Pathway: **{treatment['name']}**")

            st.write(f"**Sorting Stream:** {treatment['stream']}")

            with st.expander("❓ Why this pathway?", expanded=True):
                st.write(
                    f"**Material:** {material}  \n"
                    f"**Condition:** {condition}  \n"
                    f"**Confidence:** {confidence}%\n\n"
                    f"{treatment['description']}"
                )

            st.header("4. Treatment Pathway")
            steps = PATHWAYS.get(treatment_key, [])
            st.write(" → ".join(steps))

            st.header("5. Virtual Sorting Facility Preview")
            diagram = "GARMENT\n   |\nAI ANALYSIS\n   |\n"
            diagram += f"{material.upper()}\n   |\n{condition.upper()}\n   |\n"
            diagram += f"{treatment['stream']}\n   |\n{treatment['name']}"
            st.code(diagram)

            st.caption("Counts updated — check the Virtual Facility and Dashboard tabs.")


# =====================================================
# TAB 3 -- VIRTUAL FACILITY
# =====================================================
with tab_facility:

    st.header("ReFab Virtual Sorting Facility")
    st.write(
        "This simulates what a real automated facility would do with each "
        "garment ReFab classifies. In a physical deployment, this diagram "
        "maps directly onto real conveyor and sorting infrastructure."
    )

    st.code(
        "                REFAB FACILITY\n\n"
        "            Incoming Garment\n"
        "                   |\n"
        "           +---------------+\n"
        "           | AI INSPECTION |\n"
        "           +-------+-------+\n"
        "                   |\n"
        "   +-------+-------+-------+-------+\n"
        "   |       |       |       |       |\n"
        " REUSE  CELLUL. SYNTH.   MIXED  MANUAL\n"
    )

    st.subheader("Live Stream Totals")
    cols = st.columns(len(PRIORITY_ORDER))
    for col, stream in zip(cols, PRIORITY_ORDER):
        with col:
            st.metric(stream.title(), st.session_state.stats[stream])

    st.divider()

    st.subheader("Recent Garments Processed")
    if st.session_state.history:
        st.table(st.session_state.history)
    else:
        st.info("No garments analyzed yet this session. Go to the Analyze Garment tab.")

    if st.button("🔄 Reset facility counts"):
        st.session_state.stats = {t["stream"]: 0 for t in TREATMENTS.values()}
        st.session_state.history = []
        st.rerun()
