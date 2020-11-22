import plotly.graph_objs as go


def histogram(*args):
    f = go.Figure()
    for a in args:
        f.add_histogram(x=a)
    return f