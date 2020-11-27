import plotly.graph_objs as go
import dash_core_components as dcc


def histogram(**kwargs):
    f = go.Figure(layout_template="none")
    for name, data in kwargs.items():
        f.add_histogram(x=data, name=name)
    return f