from flask import Flask, render_template

import reports

app = Flask(__name__)


@app.route('/')
def index():

    reporter = reports.Reporter(reports_dir='reports')
    reporter.generate_report()
    return render_template(
        'index.html',
        series=reporter.series,
        data_samples=len(reporter.data_samples),
        last_agents=reporter.latest_agents,
        last_update=reporter.last_update,
    )


app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
