from urllib import request
from flask import Flask, render_template, url_for, flash, redirect,request
from flask_behind_proxy import FlaskBehindProxy
from main_ebay import Ebay_21
from zappos import Zappos
import requests
import secrets

key = secrets.token_hex(16)
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = key


@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search')
        flash(f"Search Query: {search_query}")
        ebay = Ebay_21(name=search_query)
        zappos_data = Zappos(search_query)
        # Use the ebay object as needed
        #flash(f"Search Query: {search_query}")
        return f"<table>{zappos_data.returnDatabase()}</table>"
        #return redirect(url_for('liked'))  # Redirect back to the index page after form submission
    return render_template('base.html')
    
@app.route("/liked")
def liked():
    return render_template('liked.html')

@app.route("/products")
def products():
    return render_template('products.html')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port = 8001)