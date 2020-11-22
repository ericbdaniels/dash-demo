import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from router import Router
from template import template_layout
import plots
import random

from urllib.parse import urlencode

app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
)

router = Router()
router.register_callbacks(app)

data = {
    "Gaussian": [random.normalvariate(0, 1) for i in range(2000)],
    "Lognormal": [random.lognormvariate(0, 1) for i in range(2000)],
    "Uniform": [random.uniform(-1, 1) for i in range(2000)],
}

single_select = dcc.Dropdown(
    id="single-select-dropdown",
    options=[{"label": k, "value": k} for k in data],
    placeholder="select univariate data",
)

multi_select = dcc.Dropdown(
    id="multi-select-dropdown",
    options=[{"label": k, "value": k} for k in data],
    multi=True,
)
multi_select_submit = html.Button(
    id="multi-select-submit", children="Submit", className="btn btn-primary"
)


@app.callback(
    dash.dependencies.Output("url", "pathname"),
    [
        dash.dependencies.Input("single-select-dropdown", "value"),
        dash.dependencies.Input("multi-select-submit", "n_clicks"),
    ],
    dash.dependencies.State("multi-select-dropdown", "value"),
)
def load_page(single_value, n_clicks, multi_values):
    trigger = dash.callback_context.triggered
    if len(trigger) > 1:
        return "/"
    elif trigger[0]["prop_id"] == "single-select-dropdown.value":
        return f"/univariate/{single_value}"
    elif trigger[0]["prop_id"] == "multi-select-submit.n_clicks":
        query_str = urlencode({k: k for k in multi_values})
        return f"/multivariate?{query_str}"


@router.route("/")
def index():
    return template_layout(
        dbc.Container(
            [
                dbc.Row(dbc.Col(single_select, width=2)),
                dbc.Row(
                    [
                        dbc.Col(multi_select, width=6),
                        dbc.Col(multi_select_submit, width=2),
                    ]
                ),
            ]
        )
    )


@router.route("/univariate/<column_name>")
def univariate_stats(column_name):
    return template_layout(dcc.Graph(figure=plots.histogram(data[column_name])))


@router.route("/multivariate")
def multivariate_stats(**kwargs):
    data_to_plot = [data[v] for k, v in kwargs.items()]
    return template_layout(dcc.Graph(figure=plots.histogram(*data_to_plot)))


if __name__ == "__main__":
    app.run_server(debug=True)
