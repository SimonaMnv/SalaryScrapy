from dash import no_update, State
import dash as dash

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask import jsonify

import datetime
from subprocess import call

from flask_apscheduler import APScheduler

from salaryscrape.salaryscrape.utils.secrets_config import config

from dash_utils import layout_creation, salary_chart_bar

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

server = app.server

# scheduler and crawling part of the Flask App
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def run_spider():
    """ runs the spider inside the heroku container """
    call(["scrapy", 'crawl', 'glassdoor_spider'], cwd='/app/salaryscrape')


@server.route('/scheduled_crawl')
def add_tasks():
    """ create a scheduler to execute the spider monthly - one unique id running at a time """
    app.apscheduler.add_job(func=run_spider, trigger='cron', day='2nd wed', hour='09', minute='20',
                            id='glassdoor_spider_crawl_job')
    return jsonify({str(datetime.datetime.now()): 'scheduled crawl job started'}), 200


# todo[1]: add to the top right: 1) update rate 2) last updated


app.layout = layout_creation()


@app.callback(
    [
        Output('salary-chart-bar', 'figure'),
        Output('salary-chart-bar', 'style'),
        Output('job-missing-alert', 'is_open')
    ],
    [
        Input("profession_type", 'value'),
        Input('btn-submit', 'n_clicks'),
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date')
    ],
    [
        State('job-missing-alert', 'is_open')
    ]
)
def update_values_and_charts(job_type, btn, start_date, end_date, is_open):
    """ if button is clicked, unhide and generate bar chart based on selected options, if not then return an empty and
    hidden bar-chart. Also, if a job is not selected then return a popup message """
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn-submit' in changed_id:
        if job_type:
            try:
                return salary_chart_bar(end_date, start_date, job_type), {'width': "100%",
                                                                          'display': 'inline-block'}, False
            except KeyError:
                return no_update, no_update, no_update
        else:
            return no_update, no_update, True
    else:
        return no_update


if __name__ == '__main__':
    debug = False if config['ENV'] == 'prod' else True
    app.run_server(debug=debug)
