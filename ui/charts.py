import plotly.express as px


def create_quality_chart(complete, missing, duplicate):
    labels = [
        "Complete",
        "Missing",
        "Potential Duplicates",
    ]

    values = [
        complete,
        missing,
        duplicate,
    ]

    fig = px.bar(
        x=labels,
        y=values,
        title="Data Quality Overview",
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig