from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name: ', validators=[DataRequired()])
    location = StringField("Location: ", validators=[DataRequired()])
    map_url = StringField("Cafe Location on Google Maps (URL): ", validators=[DataRequired(), URL()])
    img_url = StringField("Image of Cafe (URL): ", validators=[DataRequired(), URL()])
    has_wifi = SelectField("Is Wifi Available: ", choices=["Yes", "No"], validators=[DataRequired()])
    has_sockets = SelectField("Is Charging Sockets Available: ", choices=["Yes", "No"], validators=[DataRequired()])
    can_take_calls = SelectField("Can you take calls: ", choices=["Yes", "No"], validators=[DataRequired()])
    has_toilet = SelectField("Is there a Washroom: ", choices=["Yes", "No"], validators=[DataRequired()])
    seats = StringField('Amount of seats e.g (10-20): ', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price: ', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    has_toilet = db.Column(db.Integer, nullable=True)
    has_wifi = db.Column(db.Integer, nullable=True)
    can_take_calls = db.Column(db.Integer, nullable=True)
    seats = db.Column(db.String(250), nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    all_cafes = Cafe.query.order_by(Cafe.id).all()
    return render_template("index.html", cafes=all_cafes)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(name=form.cafe.data,
                        map_url=form.map_url.data,
                        img_url=form.img_url.data,
                        location=form.location.data,
                        has_sockets=1 if form.has_sockets.data == 'Yes' else 0,
                        has_toilet=1 if form.has_toilet.data == 'Yes' else 0,
                        has_wifi=1 if form.has_wifi.data == 'Yes'  else 0,
                        can_take_calls=1 if form.can_take_calls.data == 'Yes' else 0,
                        seats=form.seats.data,
                        coffee_price=form.coffee_price.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route("/post/<int:id>")
def view(id):
    cafe = Cafe.query.filter_by(id=id).first()
    return render_template("view.html", cafe=cafe)


@app.route("/delete/<int:gone>")
def delete(gone):
    cafe = Cafe.query.filter_by(id=gone).first()
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
