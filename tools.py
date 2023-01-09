from flask import Flask, session, jsonify, redirect, flash, render_template
from models import db, connect_db, User, Feedback
from werkzeug.exceptions import Unauthorized


class Tools():
    """This will be used to keep app.py's code less cluttered"""

    @staticmethod
    def register_user_from_form(form):
        """This validates the form and creates a new model instance and updated its to the database"""
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['user_username'] = new_user.username
        return redirect(f'/users/{new_user.username}')

    @staticmethod
    def validate_user(form):
        """Checks if the user is in the database"""
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session['user_username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Incorrect username or incorrect password']
            return render_template('login-form.html', form=form)
    
    @staticmethod
    def login_handling(username):
        """Once the user has been logged in the page"""
        user = User.query.filter_by(username=username).first()
        if user and user.username == session["user_username"]:
            return render_template('secret.html', user=user)
        else:
            raise Unauthorized()
        
    @staticmethod
    def delete_user(username):
        """Only the session user can delete himself"""
        user = User.query.filter_by(username=username).first()
        if user and user.username == session["user_username"]:
            db.session.delete(user)
            db.session.commit()
            return redirect('/')
        else:
            raise Unauthorized()

class FeedbackTools():
    """This will be specific about dealing with Feedback class and keep app.py's
    less cluttered"""

    def add_feedback(username, form):
        """Validates the user and adds feedback to the database"""
        user = User.query.filter_by(username=username).first()
        if user and user.username == session["user_username"]: 
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback.add(title, content, user.username)
            db.session.add(new_feedback)
            db.session.commit()
            return render_template('secret.html', user=user)
        else:
            raise Unauthorized()
    
    def modify_feedback(current_feedback, form):
        """Validates the user and adds the modified beedback to the database"""
        if current_feedback.username == session["user_username"]:
            current_feedback.title = form.title.data
            current_feedback.content = form.content.data
            db.session.add(current_feedback)
            db.session.commit()
            return redirect(f'/users/{current_feedback.username}')
        elif current_feedback.username != session["user_username"]:
            raise Unauthorized()
        
    def eliminate_feedback(feedback_id):
        """Checks the session user is the same owner of the post 
        and eliminates the feedback from the database"""
        current_feedback = Feedback.query.get_or_404(feedback_id)
        if current_feedback.username == session["user_username"]:
            db.session.delete(current_feedback)
            db.session.commit()
            return redirect(f'/users/{current_feedback.username}')
        else:
            raise Unauthorized()



    



            