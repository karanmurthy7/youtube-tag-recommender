from flask import Flask, render_template, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import Recommendation_Algo_Modular as rec


app = Flask(__name__)


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])


@app.route('/', methods = ['GET', 'POST'])
def print_form():
	return render_template('form.html')


@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    if request.method == 'POST':
    	user_input = request.form['name']
    	x = rec.helper()
    	return render_template('form.html', user_input = user_input, recommendation = x)


@app.route("/tuna/<username>")
def tuna(username):
	return "Hey there, %s" % username


@app.route("/tuna/<int:post_id>")
def tuna_post(post_id):
	return "Post ID:, %s" % post_id


if __name__ == '__main__':
    app.run(debug = True)