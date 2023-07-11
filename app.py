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
    return render_template('index.html')
    
@app.route("/liked")
def liked():
    return render_template('liked.html')

@app.route("/products")
def products():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port = 8001)