import json


from plotly.subplots import make_subplots
import plotly.graph_objs as go


def get_items_mapping(filepath):
    """Decode JSON w/ items mapping"""
    mapping = {}
    with open(filepath, "r") as fp:
        mapping = json.load(fp)

    return mapping


def visualize_metrics(metrics):
    figure = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "indicator"}, {"type": "indicator"}]]  # for the second gauge (perhaps @k)
    )

    figure.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=metrics["current_f1"],
            title={"text": "F1 Score"},
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={"axis": {"range": [0, 1]}},
            delta={"reference": metrics["prev_f1"]},
        ),
        row=1,
        col=2
    )

    return figure
