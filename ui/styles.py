import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        /* ---------- GLOBAL ---------- */

        .stApp {
            background: #080d19;
            color: #f8fafc;
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* ---------- SIDEBAR ---------- */

        section[data-testid="stSidebar"] {
            background: #0d1424;
            border-right: 1px solid #26334a;
        }

        section[data-testid="stSidebar"] * {
            color: #e5e7eb;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #ffffff;
        }

        /* ---------- BRAND ---------- */

        .verity-title {
            font-size: 44px;
            font-weight: 850;
            letter-spacing: -1.5px;
            color: #f8fafc;
            margin-bottom: 0;
        }

        .verity-subtitle {
            color: #8ea0ba;
            font-size: 16px;
            margin-top: 5px;
            margin-bottom: 32px;
        }

        /* ---------- METRIC CARDS ---------- */

        .metric-card {
            background: linear-gradient(145deg, #111a2b, #0d1525);
            border: 1px solid #25344d;
            border-radius: 16px;
            padding: 20px;
            min-height: 115px;
        }

        .metric-label {
            color: #8ea0ba;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.7px;
        }

        .metric-value {
            color: #f8fafc;
            font-size: 30px;
            font-weight: 750;
            margin-top: 8px;
        }

        /* ---------- FILE CARDS ---------- */

        .file-card {
            background: #101a2c;
            border: 1px solid #26364f;
            border-radius: 12px;
            padding: 14px 16px;
            margin-top: 8px;
        }

        .file-name {
            color: #f8fafc;
            font-weight: 650;
        }

        .file-meta {
            color: #8293ad;
            font-size: 13px;
            margin-top: 4px;
        }

        /* ---------- VERIFIED ---------- */

        .verified-card {
            background: linear-gradient(145deg, #0b241b, #0d1d19);
            border: 1px solid #1c754d;
            border-radius: 18px;
            padding: 28px;
            margin-top: 20px;
        }

        .verified-title {
            color: #4ade80;
            font-size: 18px;
            font-weight: 750;
        }

        .answer-value {
            color: #ffffff;
            font-size: 42px;
            font-weight: 850;
            margin: 12px 0;
        }

        /* ---------- CANNOT DETERMINE ---------- */

        .warning-card {
            background: linear-gradient(145deg, #2a1e0b, #21180a);
            border: 1px solid #946617;
            border-radius: 18px;
            padding: 28px;
            margin-top: 20px;
        }

        .warning-title {
            color: #fbbf24;
            font-size: 18px;
            font-weight: 750;
        }

        /* ---------- FAILED ---------- */

        .failed-card {
            background: linear-gradient(145deg, #2a1111, #210d0d);
            border: 1px solid #963838;
            border-radius: 18px;
            padding: 28px;
            margin-top: 20px;
        }

        .failed-title {
            color: #f87171;
            font-size: 18px;
            font-weight: 750;
        }

        /* ---------- EVIDENCE ---------- */

        .evidence-card {
            background: #101a2c;
            border: 1px solid #26364f;
            border-radius: 14px;
            padding: 18px;
            margin-top: 10px;
        }

        /* ---------- SECTION HEADERS ---------- */

        .section-title {
            color: #f8fafc;
            font-size: 22px;
            font-weight: 700;
            margin-top: 28px;
            margin-bottom: 12px;
        }

        /* ---------- STATUS ---------- */

        .status-ok {
            color: #4ade80;
            font-weight: 650;
        }

        .status-warning {
            color: #fbbf24;
            font-weight: 650;
        }

        .status-danger {
            color: #f87171;
            font-weight: 650;
        }

        /* ---------- BUTTON ---------- */

        .stButton > button {
            border-radius: 10px;
            font-weight: 700;
            min-height: 44px;
        }

        /* ---------- CODE ---------- */

        pre {
            border-radius: 12px !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )