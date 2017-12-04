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
        
        video_name = request.form['video_name']
        channel_title = request.form['channel_title']
        video_category = request.form['video_category']
        description = request.form['description']

        print(video_name)
        if video_name is None:
            video_name = ""
        if channel_title is None:
            channel_title = ""
        if video_category is None:
            video_category = ""
        if description is None:
            description = ""
        recommend_tags = rec.initializeAndFetchRecommendations(video_name, channel_title, video_category, description)
        print("\n\n", recommend_tags)
        return render_template('form.html', video_name = video_name, channel_title = channel_title, video_category = video_category, description = description, recommendation = recommend_tags)


if __name__ == '__main__':
    app.run(debug = True)