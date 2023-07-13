from urllib import request
from flask import Flask, render_template, url_for, flash, redirect,request
from flask_behind_proxy import FlaskBehindProxy
from main_ebay import Ebay_21
from zappos import Zappos
import requests
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

key = secrets.token_hex(16)
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Liked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(120), unique=False, nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.description}', '{self.url}')"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}')"

class SaveLiked(FlaskForm):
    submit = SubmitField('Liked')

class SaveHistory(FlaskForm):
    submit = SubmitField('Search')

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route("/",methods=['GET', 'POST'])
@app.route("/index",methods=['GET', 'POST'])
def index():
    form = SaveHistory()
    form2 = SaveLiked()
    print('hi')
    if form2.is_submitted() and request.form.get('search') is None:
        print('works')
        saved_liked(24, "hat", "cat") # do something
        print('data')
        print(db.session.query(Liked).all())
        print(form.validate_on_submit)
        print(form2.validate_on_submit)
    if form.validate_on_submit() and request.form.get('search') is not None:
        search_query = request.form.get('search')
        flash(f"Search Query: {search_query}")
        ebay = Ebay_21(name=search_query)
        zappos_data = Zappos(search_query)
        # Use the ebay object as needed
        #flash(f"Search Query: {search_query}")
        saved_history(search_query)
        print(db.session.query(History).all())

        ebay_products = ebay.retrieve_data_from_database()[:20]
        zappos_products = zappos_data.returnDatabase()[:20]

        # print(ebay_products[0])
        print(zappos_products)

        return render_template('products.html', ebay_data=ebay_products, zappos_data=zappos_products)
        #return redirect(url_for('liked'))  # Redirect back to the index page after form submission
    return render_template('base.html', form=form, form2=form2)


@app.route("/liked")
def liked():
    return render_template('liked.html')

# @app.route("/products")
# def products():
#     return render_template('products.html', ebay_data=ebay_products, zappos_data=zappos_products)

@app.route("/history")
def history():
    history= db.session.query(History).all()
    return render_template('history.html', history=history)

def saved_liked(id, description, url):
    liked = Liked(id=id, description=description, url=url) 
    db.session.add(liked)
    db.session.commit()

def saved_history(name):
    history=History(name=name)
    db.session.add(history)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port = 8001)