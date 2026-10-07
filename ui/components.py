import streamlit as st


def render_metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_verified_result(result):
    answer = result.get("answer", "N/A")
    confidence = result.get("confidence", 0)

    st.markdown(
        f"""
        <div class="verified-card">
            <div class="verified-title">✓ VERIFIED ANSWER</div>
            <div class="answer-value">{answer}</div>
            <div>
                Confidence:
                <strong>{confidence}%</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success("Code executed successfully")
    st.success("Independent verification passed")

    warnings = result.get("warnings", [])

    if warnings:
        for warning in warnings:
            st.warning(warning)


def render_cannot_determine(result):
    reason = result.get(
        "reason",
        "The available data is insufficient to answer this question reliably.",
    )

    st.markdown(
        f"""
        <div class="warning-card">
            <div class="warning-title">⚠ CANNOT DETERMINE</div>
            <p>{reason}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_verification_failed(result):
    reason = result.get(
        "reason",
        "The generated calculation failed independent verification.",
    )

    st.markdown(
        f"""
        <div class="failed-card">
            <div class="failed-title">✕ VERIFICATION FAILED</div>
            <p>{reason}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_evidence(result):
    st.markdown("### Evidence")

    evidence = result.get("evidence", [])

    if not evidence:
        st.info("Evidence will appear here after analysis.")
        return

    for item in evidence:
        st.markdown(
            f"""
            <div class="evidence-card">
                <strong>Source:</strong> {item.get("source", "Unknown")}<br>
                <strong>Sheet/Table:</strong> {item.get("table", "N/A")}<br>
                <strong>Rows:</strong> {item.get("rows", "N/A")}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_code(result):
    code = result.get("code")

    if not code:
        return

    st.markdown("### Calculation Code")
    st.code(code, language="python")