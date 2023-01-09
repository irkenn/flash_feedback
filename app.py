from flask import Flask, render_template, redirect, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LoginUserForm, AddFeedbackForm
from tools import Tools, FeedbackTools
from werkzeug.exceptions import Unauthorized, NotFound

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SECRET KEY'] = "There's_no_spoon"
app.config['SECRET_KEY'] = "There's_no_spoon"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """Redirects to /register"""

    return redirect('/register')

@app.route('/register', methods=['POST', 'GET'])
def register_page():
    """Sends a form to create a user"""
    form = AddUserForm()
    if form.validate_on_submit():
        return Tools.register_user_from_form(form)
    else:
        return render_template('register-form.html', form=form)

@app.route('/users/<username>')
def secret_page(username):
    """Secret page (to be modify)"""
    
    if "user_username" in session:
        return Tools.login_handling(username)
    else:
        raise NotFound()
        

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Shows a form to login a user and processes the form to authenticate"""
    form = LoginUserForm()
    if form.validate_on_submit():
        return Tools.validate_user(form)     
    
    else:
        return render_template('login-form.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    """Logs user out and redirects to homepage"""
    session.pop('user_username')

    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def authenticate_and_delete(username):
    """"Authenticates that only the same user can delete its account and 
    deletes it from the database"""
    return Tools.delete_user(username)

###### F E E D B A C K   S E C T I O N  #########

@app.route('/users/<username>/feedback/add', methods=['POST', 'GET'])
def add_feedback(username):
    """Renders a form to the user, authenticates the form, the users
    and adds the feedback to the database
    Redirects to the user homepage"""
    form = AddFeedbackForm()
    if form.validate_on_submit():
        return FeedbackTools.add_feedback(username, form)
    else:
        return render_template('add-feedback.html', form=form, username=username)

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def feedback_update(feedback_id):
    """Renders a form to the user, authenticates the form and updates the 
    fields in the database"""
    current_feedback = Feedback.query.get_or_404(feedback_id)
    if session['user_username'] and current_feedback:
        form = AddFeedbackForm(obj=current_feedback)
        if form.validate_on_submit() and current_feedback:
            return FeedbackTools.modify_feedback(current_feedback, form)
        else:
            return render_template('modify-form.html', form=form)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def feedback_delete(feedback_id):
    """Checks the users from the session and deletes the feedback"""
    return FeedbackTools.eliminate_feedback(feedback_id)



