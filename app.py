import streamlit as st

from ui.styles import apply_styles

from ui.dashboard import (
    render_header,
    render_sidebar,
    render_data_overview,
    render_question_box,
    render_result,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="VerityAI",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# APPLICATION
# =========================================================

apply_styles()

render_header()

uploaded_files = render_sidebar()

datasets = render_data_overview(
    uploaded_files
)

question, analyze = render_question_box()


# =========================================================
# TEMPORARY MOCK ANALYSIS
# =========================================================

if analyze:

    if not uploaded_files:

        st.warning(
            "Please upload at least one dataset before analyzing."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        # -------------------------------------------------
        # TEMPORARY MOCK RESULT
        #
        # This will later be replaced by the AI Agent,
        # Data Engine and Verification Engine.
        # -------------------------------------------------

        mock_result = {

            "status": "VERIFIED",

            "answer": "₹24,18,450",

            "confidence": 98.2,

            "code": (
                'result = df["revenue"].sum()\n'
                'print(result)'
            ),

            "evidence": [

                {
                    "source": uploaded_files[0].name,

                    "table": "Sales",

                    "rows": "102–842",
                }

            ],

            "warnings": [],
        }

        render_result(
            mock_result
        )