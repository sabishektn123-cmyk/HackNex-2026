import streamlit as st
import pandas as pd

from ui.components import (
    render_metric_card,
    render_verified_result,
    render_cannot_determine,
    render_verification_failed,
    render_evidence,
    render_code,
)


def render_header():
    st.markdown(
        '<div class="verity-title">VERITYAI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="verity-subtitle">'
        "Proof-Carrying Data Intelligence · "
        "AI that doesn't just answer — it proves."
        "</div>",
        unsafe_allow_html=True,
    )


def load_uploaded_file(uploaded_file):
    """
    Load CSV or Excel files into pandas.

    PDF handling will be connected to the document
    processing module later.
    """

    try:
        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):
            return pd.read_csv(uploaded_file)

        if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            return pd.read_excel(uploaded_file)

    except Exception as error:
        st.error(f"Could not read {uploaded_file.name}: {error}")

    return None


def calculate_quality(df):
    """Calculate basic dataset quality metrics."""

    if df is None or df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "missing": 0,
            "missing_percent": 0,
            "duplicates": 0,
            "completeness": 0,
        }

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = int(df.isna().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    completeness = 0

    if total_cells > 0:
        completeness = round(
            ((total_cells - missing_cells) / total_cells) * 100,
            1,
        )

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing": missing_cells,
        "missing_percent": round(
            (missing_cells / total_cells) * 100,
            1,
        )
        if total_cells
        else 0,
        "duplicates": duplicate_rows,
        "completeness": completeness,
    }


def render_sidebar():
    with st.sidebar:

        st.markdown("## VERITYAI")

        st.caption(
            "Proof-Carrying Data Intelligence"
        )

        st.divider()

        st.markdown("### Data Sources")

        uploaded_files = st.file_uploader(
            "Upload data files",
            type=["csv", "xlsx", "xls", "pdf"],
            accept_multiple_files=True,
            help="Upload CSV, Excel or PDF datasets.",
        )

        st.divider()

        st.markdown("### Data Quality")

        if uploaded_files:
            st.success(
                f"{len(uploaded_files)} file(s) loaded"
            )
        else:
            st.caption("No data loaded")

        st.divider()

        st.caption("VERITYAI MVP")
        st.caption("Proof before prediction.")

    return uploaded_files


def render_data_overview(uploaded_files):

    st.markdown(
        '<div class="section-title">Dataset Overview</div>',
        unsafe_allow_html=True,
    )

    total_files = len(uploaded_files) if uploaded_files else 0

    combined_rows = 0
    total_columns = 0
    total_missing = 0
    total_cells = 0
    total_duplicates = 0

    datasets = []

    if uploaded_files:

        for uploaded_file in uploaded_files:

            df = load_uploaded_file(uploaded_file)

            if df is not None:

                quality = calculate_quality(df)

                combined_rows += quality["rows"]
                total_columns += quality["columns"]
                total_missing += quality["missing"]

                total_cells += (
                    quality["rows"]
                    * quality["columns"]
                )

                total_duplicates += quality["duplicates"]

                datasets.append(
                    {
                        "file": uploaded_file.name,
                        "df": df,
                        "quality": quality,
                    }
                )

    completeness = 0

    if total_cells > 0:

        completeness = round(
            (
                (total_cells - total_missing)
                / total_cells
            )
            * 100,
            1,
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card(
            "Files",
            total_files,
        )

    with col2:
        render_metric_card(
            "Rows",
            f"{combined_rows:,}",
        )

    with col3:
        render_metric_card(
            "Columns",
            f"{total_columns:,}",
        )

    with col4:
        render_metric_card(
            "Completeness",
            f"{completeness}%",
        )

    # -----------------------------
    # Data quality details
    # -----------------------------

    if datasets:

        st.markdown(
            '<div class="section-title">Data Quality</div>',
            unsafe_allow_html=True,
        )

        q1, q2, q3, q4 = st.columns(4)

        with q1:
            render_metric_card(
                "Missing Cells",
                f"{total_missing:,}",
            )

        with q2:
            render_metric_card(
                "Potential Duplicates",
                f"{total_duplicates:,}",
            )

        with q3:
            render_metric_card(
                "Currency Conflicts",
                "Pending",
            )

        with q4:
            render_metric_card(
                "Date Warnings",
                "Pending",
            )

        # -----------------------------
        # File information
        # -----------------------------

        st.markdown(
            '<div class="section-title">Loaded Sources</div>',
            unsafe_allow_html=True,
        )

        for dataset in datasets:

            file_name = dataset["file"]
            df = dataset["df"]
            quality = dataset["quality"]

            st.markdown(
                f"""
                <div class="file-card">
                    <div class="file-name">
                        {file_name}
                    </div>

                    <div class="file-meta">
                        {quality["rows"]:,} rows ·
                        {quality["columns"]:,} columns ·
                        {quality["completeness"]}% complete
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # -----------------------------
        # Preview
        # -----------------------------

        st.markdown(
            '<div class="section-title">Data Preview</div>',
            unsafe_allow_html=True,
        )

        selected_file = st.selectbox(
            "Select dataset",
            [
                dataset["file"]
                for dataset in datasets
            ],
        )

        selected_dataset = next(
            dataset
            for dataset in datasets
            if dataset["file"] == selected_file
        )

        st.dataframe(
            selected_dataset["df"].head(10),
            use_container_width=True,
            hide_index=True,
        )

    return datasets


def render_question_box():

    st.markdown(
        '<div class="section-title">Ask Your Data</div>',
        unsafe_allow_html=True,
    )

    question = st.text_area(
        "Natural language question",
        placeholder=(
            "Example: What was the total laptop "
            "revenue in Q3?"
        ),
        height=100,
        label_visibility="collapsed",
    )

    analyze = st.button(
        "ANALYZE",
        type="primary",
        use_container_width=True,
    )

    return question, analyze


def render_result(result):

    if not result:
        return

    status = result.get(
        "status",
        "UNKNOWN",
    )

    if status == "VERIFIED":

        render_verified_result(result)

    elif status == "CANNOT_DETERMINE":

        render_cannot_determine(result)

    elif status == "VERIFICATION_FAILED":

        render_verification_failed(result)

    else:

        st.warning(
            f"Unknown result status: {status}"
        )

    render_evidence(result)

    if status == "VERIFIED":

        render_code(result)