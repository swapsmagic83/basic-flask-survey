from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_survey_page():
    responses.clear()
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions, responses=responses)

@app.route('/question/<int:index>')
def get_new_question(index):
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    if index == len(responses):
        question = satisfaction_survey.questions[index].question
        choices= satisfaction_survey.questions[index].choices
        return render_template('questions.html',question=question,choices=choices,index=index+1)
    if index > len(responses):
        flash('You are trying to access an invalid question')
        return redirect('/question/'+ str(len(responses)))
    if index < len(responses):
        flash('Visit question in order')
        return redirect('/question/' + str(len(responses)))
    
@app.route('/answer/<int:index>', methods=["POST"])
def post_choice(index):
    if index < len(satisfaction_survey.questions):
        response = request.form["choice"]
        responses.append(response)
        return redirect('/question/'+ str(index))
    if index >= len(satisfaction_survey.questions):
        response = request.form["choice"]
        responses.append(response)
        return redirect('/complete')
    
@app.route('/complete')
def survey_complete():
    return render_template('result.html', responses=responses)
    


