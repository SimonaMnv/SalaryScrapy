from dash import dcc
import dash_bootstrap_components as dbc

import plotly.express as px
from datetime import date
from dash import html

from salaryscrape.utils.dynamo_data import DynamoData

# get data from Amazon DynamoDB
data = DynamoData()
START_DATE = date(2022, 5, 15)  # The date the data started being collected. Used on the date-picker too


def build_banner():
    """  top banner """
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


# def salary_map():
#     salary_data = data.get_dynamodb_data()
#
#     salary_data["lon"] = pd.to_numeric(salary_data["lon"])
#     salary_data["lat"] = pd.to_numeric(salary_data["lat"])
#
#     #  px.choropleth
#     fig = go.Figure(px.scatter_mapbox(salary_data, lat="lat", lon="lon", hover_name="country",
#                                       color_discrete_sequence=["red"], zoom=5, height=450))
#     fig.update_layout(
#         mapbox_style="white-bg",
#         mapbox_layers=[
#             {
#                 "below": 'traces',
#                 "sourcetype": "raster",
#                 "sourceattribution": "United States Geological Survey",
#                 "source": [
#                     "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#                 ]
#             }
#         ])
#     fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#
#     return dcc.Graph(id="map_chart", figure=fig)


def get_unique_jobs():
    salary_data = data.get_dynamodb_data()
    return set(salary_data["job_title"])


def salary_chart_bar(end_date, start_date, selected_job_title=None):
    """
    Normalize the values to be per week if they are not.
    Plot the bar-chart based on the selected profession from the dd.
    """
    if selected_job_title:
        selected_job_data = data.get_dynamodb_data("job_title", "updated_at", selected_job_title, end_date, start_date)

        selected_job_data['job_median_to_eur'] = selected_job_data.apply(
            lambda x: float(x['job_median_to_eur']) / 12
            if x['pay_period'] == 'yr'
            else float(x['job_median_to_eur']), axis=1)

        return px.bar(
            data_frame=selected_job_data,
            x="country",
            y="job_median_to_eur",
            color='updated_at',
            barmode='group',
            text='sample_size'
        ).update_layout(
            {
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font_color': '#fff'
            }
        )


def layout_creation():
    return html.Div(
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
                                min_date_allowed=START_DATE,
                                max_date_allowed=date.today(),
                                initial_visible_month=date.today(),
                                display_format='Y-MM-DD',
                                start_date=START_DATE,
                                end_date=date.today()
                            ),
                        ],
                    ),
                    html.Div([
                        dbc.Alert(
                            "You must select a job",
                            id='job-missing-alert',
                            color="danger",
                            is_open=False
                        )
                    ]),
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
