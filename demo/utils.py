import json
import pandas as pd


from plotly.subplots import make_subplots
import plotly.graph_objs as go


def get_items_mapping(filepath):
    """Decode JSON w/ items mapping"""
    mapping = {}
    with open(filepath, "r") as fp:
        mapping = json.load(fp)

    return mapping

def itemtitle_to_itemdict(filepath, basket_todisp):
    """Decode list if item id to catalogue items (dict), in analogue as we extracted from json"""
    mapping = {}
    
    with open(filepath, "r") as fp:
        mapping0 = json.load(fp)    #know the whole dictionary 
        df0 = pd.DataFrame(mapping0).transpose()
        itemlist = df0[df0['title'].isin(basket_todisp)]
        itemlist_id = itemlist.index
        mapping = {my_key: mapping0[my_key] for my_key in itemlist_id}
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
