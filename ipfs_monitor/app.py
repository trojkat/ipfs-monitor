from pathlib import Path

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
    )


app.run(port=5000, debug=False, use_reloader=False)
