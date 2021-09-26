from flask import Flask, render_template, url_for
from SINFO import SINFO

app = Flask(__name__)

sysconf = SINFO()


@app.route('/')
def index():
    return render_template('index.html', sysconf=sysconf.get_info)


if __name__ == '__main__':
    app.run()
