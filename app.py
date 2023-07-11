from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy
import secrets

key = secrets.token_hex(16)
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = key


@app.route("/")
@app.route("/index")
def index():
    return redirect(url_for('index'))
    
@app.route("/liked")
def liked():
    return redirect(url_for('liked'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port = 8001)