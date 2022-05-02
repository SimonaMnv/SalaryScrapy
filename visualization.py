from datetime import date

import pandas as pd
from dash import dcc, no_update
import plotly.graph_objects as go
import dash as dash
from dash import html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from salaryscrape.utils.dynamo_data import DynamoData
from salaryscrape.utils.local_payment_to_eur import local_revenue_to_usd

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

# get data from Amazon DynamoDB
data = DynamoData()


# todo: add to the top right: 1) update rate 2) last updated
# todo: fix to show something when applying without a job selected
# todo: use local_revenue_to_usd when crawling to add a new colum called "currency_to_eur"


# top banner
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.Button(
                        id="learn-more-button", children="Glassdoor Salary Per Country", n_clicks=0
                    ),
                ],
            ),
        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


def salary_map():
    salary_data = data.get_dynamodb_data()

    salary_data["lon"] = pd.to_numeric(salary_data["lon"])
    salary_data["lat"] = pd.to_numeric(salary_data["lat"])

    #  px.choropleth
    fig = go.Figure(px.scatter_mapbox(salary_data, lat="lat", lon="lon", hover_name="country",
                                      color_discrete_sequence=["red"], zoom=5, height=450))
    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return dcc.Graph(id="map_chart", figure=fig)


def get_unique_jobs():
    salary_data = data.get_dynamodb_data()
    return set(salary_data["job_title"])


def salary_chart_bar(selected_job_title=None):
    """
    Normalize the values to be per week if they are not.
    Plot the bar-chart based on the selected profession from the dd.
    """
    if selected_job_title:
        selected_job_data = data.get_dynamodb_data("job_title", selected_job_title)

        selected_job_data['payment_per_week'] = selected_job_data.apply(
            lambda x: float(x['job_median_payment']) / 12
            if x['pay_period'] == 'yr'
            else float(x['job_median_payment']), axis=1)

        return px.bar(
            data_frame=selected_job_data,
            x="country",
            y="payment_per_week",
            color='sample_size'
        ).update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font_color': '#fff'
            }
        )


app.layout = html.Div(
    children=[
        html.Div(
            className="center-content",
            children=[
                build_banner(),  # this is the top part
                dcc.Interval(
                    id="interval-component",
                    interval=2 * 1000,  # in milliseconds
                    n_intervals=50,  # start at batch 50
                    disabled=True,
                ),
                html.Div(
                    id='date-filter',
                    children=[
                        generate_section_banner("Filter Per Date & Job"),
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=date(2022, 4, 20),  # start date of data is 2022-04-20
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            display_format='Y-MM-DD',
                            start_date=date(2022, 4, 20),
                            end_date=date.today()
                        ),
                    ],
                ),
                html.Div(
                    id='profession-filter-dd',
                    children=[
                        dcc.Loading(
                            id="loading-1",
                            color='#36505a',
                            type="cube",
                            children=[
                                dcc.Dropdown(
                                    id='profession_type',
                                    options=[job for job in get_unique_jobs()],
                                    clearable=False,
                                ),
                            ]
                        ),
                        html.Button('Apply Filters', id='btn-submit', n_clicks=0),
                    ]
                ),
                html.Div(
                    id="chart-bar-loading",
                    children=[
                        dcc.Loading(
                            id="loading-2",
                            type="cube",
                            color='#36505a',
                            children=[
                                generate_section_banner("Salaries Per Month Analysis"),
                                dcc.Graph(id="salary-chart-bar", style={'display': 'none'})
                            ],
                        ),
                    ],
                ),
                # html.Div(
                #     id="country-map",
                #     children=[
                #         generate_section_banner("Salary per country"),
                #         salary_map(),
                #     ], className="six columns"
                # ),
                # ],  # style={'display': 'none'}
            ]
        )
    ]
)


@app.callback(
    [
        Output('salary-chart-bar', 'figure'),
        Output('salary-chart-bar', 'style'),
    ],
    [
        Input("profession_type", "value"),
        Input('btn-submit', 'n_clicks'),
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date')
    ],
)
def update_values_and_charts(job_type, btn, start_date, end_date):
    """ if button is clicked, unhide and generate bar chart based on selected options, if not then return an empty and
    hidden bar-chart """
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn-submit' in changed_id:
        try:
            return salary_chart_bar(job_type), {'width': "100%", 'display': 'inline-block'}
        except KeyError:
            return no_update, no_update, no_update, no_update
    else:
        return no_update


if __name__ == '__main__':
    app.run_server(debug=True)
