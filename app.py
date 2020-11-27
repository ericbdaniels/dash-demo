import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
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
    Output("url", "pathname"),
    [
        Input("single-select-dropdown", "value"),
        Input("multi-select-submit", "n_clicks"),
    ],
    State("multi-select-dropdown", "value"),
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
                dbc.Row(
                    dbc.Col(
                        [
                            dcc.Markdown(
                                """# Dash-Demo: A simple multipage Dash app"""
                            ),
                            dcc.Markdown(
                                """This basic app demonstrates a handful of Dash features described in the blog post linked below."""
                            ),
                            dcc.Markdown(
                                "[geostats.dev](https://geostats.dev/python/plotly/dash/flask/dash%20bootstrap%20components/2020/11/26/dash-post.html)"
                            ),
                        ]
                    )
                ),
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Label("Select Single Distribution:   "),
                                    width=3,
                                ),
                                dbc.Col(single_select, width=4),
                            ],
                        ),
                        dbc.Row(dbc.Col(html.P("OR", className="display-4"))),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Label("Select Multiple Distributions:   "),
                                    width=3,
                                ),
                                dbc.Col(multi_select, width=4),
                                dbc.Col(multi_select_submit, width=2),
                            ]
                        ),
                    ],
                    className="m-5 p-5 shadow border mx-auto bg-light",
                ),
            ]
        )
    )


@router.route("/univariate/<distribution_name>")
def univariate_stats(distribution_name):
    return template_layout(
        dcc.Graph(
            figure=plots.histogram(distribution_name=data[distribution_name]),
            style={"height": "80vh"},
            config={
                "displaylogo": False,
            },
        )
    )


@router.route("/multivariate")
def multivariate_stats(**kwargs):
    data_to_plot = {v: data[v] for k, v in kwargs.items()}
    return template_layout(
        dcc.Graph(
            figure=plots.histogram(**data_to_plot),
            style={"height": "80vh"},
            config={
                "displaylogo": False,
            },
        )
    )


if __name__ == "__main__":
    app.run_server(debug=True)
